"""Train and compare vision/proprioception BC with and without joint torque.

Each HDF5 episode is kept entirely in either train or validation. The target
is RoboTwin's *next drive target* (two 7-DOF arms and two grippers), not an
applied torque. Run from the RoboTwin root with its Python environment.
"""

from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path

import cv2
import h5py
import numpy as np
import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from data.decode_image_bit import decode_image_bit


def read_episode(path: Path, image_size: int) -> dict[str, np.ndarray]:
    with h5py.File(path, "r") as hdf5:
        def array(name: str) -> np.ndarray:
            if name not in hdf5:
                raise KeyError(f"{path}: missing {name}; collect with joint_torque: true")
            return np.asarray(hdf5[name][:], dtype=np.float32)

        rgb = decode_image_bit(hdf5["vision/cam_head/colors"][:])
        rgb = np.stack(
            [cv2.resize(frame, (image_size, image_size)) for frame in rgb]
        ).astype(np.uint8)
        baseline = np.concatenate(
            [array(f"state/{arm}_arm_measured_qpos") for arm in ("left", "right")]
            + [array(f"state/{arm}_arm_measured_qvel") for arm in ("left", "right")]
            + [array(f"state/{arm}_ee_joint_states") for arm in ("left", "right")],
            axis=1,
        )
        torque = np.concatenate(
            [array(f"state/{arm}_arm_transmitted_torque") for arm in ("left", "right")],
            axis=1,
        )
        target = np.concatenate(
            [array(f"action/{arm}_arm_joint_states") for arm in ("left", "right")]
            + [array(f"action/{arm}_ee_joint_states") for arm in ("left", "right")],
            axis=1,
        )
        count = len(target)
        if rgb.shape != (count, image_size, image_size, 3):
            raise ValueError(f"{path}: unexpected RGB shape {rgb.shape}")
        if baseline.shape != (count, 30) or torque.shape != (count, 14) or target.shape != (count, 16):
            raise ValueError(f"{path}: unexpected state/action dimensions")
        if not all(np.isfinite(x).all() for x in (baseline, torque, target)):
            raise ValueError(f"{path}: nonfinite observations or targets")
        return {"image": rgb, "baseline": baseline, "torque": torque, "target": target}


class VisionBC(nn.Module):
    def __init__(self, proprio_dim: int):
        super().__init__()
        self.visual = nn.Sequential(
            nn.Conv2d(3, 16, 5, stride=2, padding=2), nn.ReLU(),
            nn.Conv2d(16, 32, 3, stride=2, padding=1), nn.ReLU(),
            nn.Conv2d(32, 64, 3, stride=2, padding=1), nn.ReLU(),
            nn.AdaptiveAvgPool2d(1), nn.Flatten(),
        )
        self.head = nn.Sequential(
            nn.Linear(64 + proprio_dim, 128), nn.ReLU(),
            nn.Linear(128, 128), nn.ReLU(),
            nn.Linear(128, 16),
        )

    def forward(self, image: torch.Tensor, proprio: torch.Tensor) -> torch.Tensor:
        return self.head(torch.cat((self.visual(image), proprio), dim=1))


def concatenate(episodes: list[dict[str, np.ndarray]], key: str) -> np.ndarray:
    return np.concatenate([episode[key] for episode in episodes], axis=0)


def normalize(train: np.ndarray, val: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    mean = train.mean(axis=0).astype(np.float32)
    std = train.std(axis=0).astype(np.float32)
    std = np.maximum(std, 1e-3)
    return (train - mean) / std, (val - mean) / std, mean, std


def make_loader(image: np.ndarray, proprio: np.ndarray, target: np.ndarray,
                batch_size: int, shuffle: bool) -> DataLoader:
    tensors = TensorDataset(
        torch.from_numpy(image).permute(0, 3, 1, 2).float().div_(255),
        torch.from_numpy(proprio).float(),
        torch.from_numpy(target).float(),
    )
    return DataLoader(tensors, batch_size=batch_size, shuffle=shuffle)


@torch.no_grad()
def evaluate(model: VisionBC, loader: DataLoader, device: torch.device,
             target_mean: np.ndarray, target_std: np.ndarray) -> dict[str, float]:
    model.eval()
    mean = torch.as_tensor(target_mean, device=device)
    std = torch.as_tensor(target_std, device=device)
    error_sum = torch.zeros(16, device=device)
    count = 0
    for image, proprio, target in loader:
        image, proprio, target = image.to(device), proprio.to(device), target.to(device)
        prediction = model(image, proprio)
        error_sum += ((prediction - target) * std).abs().sum(dim=0)
        count += len(target)
    error = (error_sum / count).cpu().numpy()
    return {
        "left_arm_mae_rad": float(error[:7].mean()),
        "right_arm_mae_rad": float(error[7:14].mean()),
        "gripper_mae": float(error[14:].mean()),
    }


def train_one(name: str, train_episodes: list[dict[str, np.ndarray]],
              val_episodes: list[dict[str, np.ndarray]], args: argparse.Namespace,
              device: torch.device) -> dict[str, float]:
    train_image = concatenate(train_episodes, "image")
    val_image = concatenate(val_episodes, "image")
    train_baseline = concatenate(train_episodes, "baseline")
    val_baseline = concatenate(val_episodes, "baseline")
    if name == "with_torque":
        train_baseline = np.concatenate((train_baseline, concatenate(train_episodes, "torque")), axis=1)
        val_baseline = np.concatenate((val_baseline, concatenate(val_episodes, "torque")), axis=1)
    train_state, val_state, state_mean, state_std = normalize(train_baseline, val_baseline)
    train_target, val_target, target_mean, target_std = normalize(
        concatenate(train_episodes, "target"), concatenate(val_episodes, "target")
    )
    train_loader = make_loader(train_image, train_state, train_target, args.batch_size, True)
    val_loader = make_loader(val_image, val_state, val_target, args.batch_size, False)

    torch.manual_seed(args.seed)
    model = VisionBC(train_state.shape[1]).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=args.learning_rate)
    best_score = float("inf")
    best_metrics = {}
    output = args.output_dir / f"{name}.pt"
    for epoch in range(1, args.epochs + 1):
        model.train()
        train_loss = 0.0
        for image, proprio, target in train_loader:
            image, proprio, target = image.to(device), proprio.to(device), target.to(device)
            optimizer.zero_grad(set_to_none=True)
            prediction = model(image, proprio)
            loss = nn.functional.smooth_l1_loss(prediction, target)
            loss.backward()
            optimizer.step()
            train_loss += float(loss) * len(target)
        metrics = evaluate(model, val_loader, device, target_mean, target_std)
        score = metrics["left_arm_mae_rad"] + metrics["right_arm_mae_rad"]
        if score < best_score:
            best_score, best_metrics = score, {"epoch": epoch, **metrics}
            torch.save({
                "model": model.state_dict(), "proprio_dim": train_state.shape[1],
                "state_mean": state_mean, "state_std": state_std,
                "target_mean": target_mean, "target_std": target_std,
                "image_size": args.image_size, "name": name,
            }, output)
        print(f"{name} epoch {epoch}/{args.epochs}: train_loss={train_loss / len(train_target):.5f} "
              f"val_arm_mae_rad={score / 2:.5f}", flush=True)
    return best_metrics


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-root", type=Path, required=True,
                        help="Directory containing torque-enabled episode HDF5 files")
    parser.add_argument("--output-dir", type=Path, default=Path("result/torque_bc"))
    parser.add_argument("--epochs", type=int, default=20)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--image-size", type=int, default=64)
    parser.add_argument("--learning-rate", type=float, default=1e-3)
    parser.add_argument("--val-fraction", type=float, default=0.25)
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()
    if args.epochs < 1 or args.batch_size < 1 or not 0 < args.val_fraction < 1:
        parser.error("epochs and batch-size must be positive; val-fraction must be in (0, 1)")
    paths = sorted(args.data_root.rglob("episode_*.hdf5"))
    if len(paths) < 2:
        parser.error("at least two independent torque-enabled episodes are needed for episode-level validation")
    random.seed(args.seed)
    np.random.seed(args.seed)
    episodes = [read_episode(path, args.image_size) for path in paths]
    order = np.random.default_rng(args.seed).permutation(len(paths))
    n_val = max(1, int(round(len(paths) * args.val_fraction)))
    val_indices = set(order[:n_val])
    train_episodes = [ep for i, ep in enumerate(episodes) if i not in val_indices]
    val_episodes = [ep for i, ep in enumerate(episodes) if i in val_indices]
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    print(f"train episodes={len(train_episodes)}, validation episodes={len(val_episodes)}, device={device}")
    results = {
        name: train_one(name, train_episodes, val_episodes, args, device)
        for name in ("baseline", "with_torque")
    }
    (args.output_dir / "metrics.json").write_text(
        json.dumps({"episodes": len(paths), "validation_indices": [int(i) for i in sorted(val_indices)],
                    "results": results}, indent=2), encoding="utf-8"
    )
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
