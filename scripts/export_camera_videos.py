"""Export the RGB camera streams stored in one RoboTwin HDF5 episode.

Run from a RoboTwin checkout with its Python environment active, for example:
    python scripts/export_camera_videos.py data/.../data/episode_0000000.hdf5

The HDF5 stores state/action pairs, so its camera streams have one fewer frame
than the MP4 produced directly from the original per-frame collection cache.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import h5py


ROBOTWIN_ROOT = Path(__file__).resolve().parents[1]
if str(ROBOTWIN_ROOT) not in sys.path:
    sys.path.insert(0, str(ROBOTWIN_ROOT))

from data.decode_image_bit import decode_image_bit
from envs.utils.images_to_video import images_to_video


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("hdf5", type=Path, help="Path to episode_XXXXXXX.hdf5")
    parser.add_argument(
        "--views",
        nargs="+",
        default=["cam_left_wrist", "cam_right_wrist"],
        help="Camera group names under HDF5 /vision",
    )
    args = parser.parse_args()

    video_dir = args.hdf5.parent.parent / "video"
    video_dir.mkdir(exist_ok=True)

    with h5py.File(args.hdf5, "r") as hdf5:
        for view in args.views:
            dataset_path = f"vision/{view}/colors"
            if dataset_path not in hdf5:
                raise KeyError(f"Camera stream is missing: {dataset_path}")
            rgb_frames = decode_image_bit(hdf5[dataset_path][:])
            output = video_dir / f"{args.hdf5.stem}_{view}.mp4"
            images_to_video(rgb_frames, out_path=str(output))


if __name__ == "__main__":
    main()
