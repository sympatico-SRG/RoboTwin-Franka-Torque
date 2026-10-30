# Franka 关节传递力矩观测与下一步动作预测

## 研究问题

比较两个离线行为克隆模型：

1. 基线：头部 RGB 图像 + 两臂实测关节角、关节速度 + 夹爪状态。
2. 力矩模型：上述输入 + 两臂各 7 维关节传递力矩。

两个模型都预测下一采样帧的两臂关节**驱动目标**和两侧夹爪目标，共 16 维。`beat_block_hammer` 场景有两台 Franka，因此每台 7 维、总共 14 维力矩；即使某一条演示只动一只手，也同时记录两臂。

## 信号来源与限制

采集时调用 SAPIEN 3 的 `PhysxArticulation.get_link_incoming_joint_forces()`，从每个 Franka 旋转关节的子链接读取 joint-frame X（twist）轴传递扭矩，单位 N·m。该值是 **PhysX 中关节承受的传递载荷**，不是电机电流推算的实机力矩，也不是独立的关节力矩传感器输出。`get_qf()` 对应外加广义力，不能直接拿来代替位置驱动器的力矩。训练和报告中应保留 `transmitted_torque` 这个名称。

本任务的原始 `state/*_arm_joint_states` 来自驱动目标角；新增 `state/*_arm_measured_qpos` 和 `state/*_arm_measured_qvel` 才来自仿真的实际关节运动。模型以当前帧的观测预测下一帧驱动目标，避免把未来力矩放进当前输入。

## HDF5 字段

配置 `env_cfg/task_config/franka_torque.yml` 中 `data_type.joint_torque: true` 开启采集。每条 HDF5 中新增：

```text
state/left_arm_measured_qpos          (T, 7), rad
state/left_arm_measured_qvel          (T, 7), rad/s
state/left_arm_transmitted_torque     (T, 7), N m
state/right_arm_measured_qpos         (T, 7), rad
state/right_arm_measured_qvel         (T, 7), rad/s
state/right_arm_transmitted_torque    (T, 7), N m
```

原有 `vision/cam_head/colors` 与 `action/*` 保持 RoboTwin 格式。每条原始 episode 有 `T+1` 帧，HDF5 用前 `T` 帧作当前状态，后 `T` 帧作动作目标。

## 采集与初步训练

先按 [RoboTwin A100 仿真手册](ROBOTWIN_A100_SIMULATION_GUIDE.md) 激活环境、设置 A100 CuRobo 的 `PYTHONPATH` 和系统 ffmpeg，然后使用 `franka_torque` 配置：

```bash
cd /mnt/ceph2/srg/RoboTwin-torque-dev
/mnt/ceph2/hjs/miniconda3/envs/robotwin/bin/python scripts/collect_data.py beat_block_hammer franka_torque
```

配置中的 `episode_num` 是该配置目录下的**目标总条数**，已有 HDF5 会跳过。需要比较模型时，至少采两条不同 episode 才能按 episode 分出训练和验证；少量 episode 的结果仅用于验证流程。训练命令：

```bash
cd /mnt/ceph2/srg/RoboTwin-torque-dev
/mnt/ceph2/hjs/miniconda3/envs/robotwin/bin/python scripts/train_torque_bc.py \
  --data-root data/franka_torque/beat_block_hammer \
  --output-dir result/torque_bc \
  --epochs 20
```

训练脚本在**相同的 episode 划分**上依次训练 `baseline` 和 `with_torque`，输出两个权重文件及 `metrics.json`。指标是留出 episode 上的下一步关节目标角平均绝对误差（rad）和夹爪误差；它不能替代在仿真中闭环执行的任务成功率。只有收集足够多且覆盖左右臂、不同物体位置的演示，再进行多种随机种子重复和闭环评估，才能判断力矩观测是否真的改进策略。

## 2026-10-30 首次烟测

在隔离工作树 `/mnt/ceph2/srg/RoboTwin-torque-dev` 上采集 8 条演示，使用 6 条训练、2 条验证；验证 episode 2 使用左臂，episode 4 使用右臂。两组模型各训练 20 轮，最佳检查点结果如下：

| 模型 | 左臂目标角 MAE (rad) | 右臂目标角 MAE (rad) | 夹爪 MAE |
| --- | ---: | ---: | ---: |
| 图像＋关节状态（基线） | 0.02144 | 0.02395 | 0.03457 |
| 图像＋关节状态＋传递力矩 | 0.02164 | 0.02262 | 0.04420 |

力矩模型的两臂平均角度误差约 0.02213 rad，基线约 0.02269 rad；夹爪误差反而增加。样本量很小，结果只用于证明采集、对齐和训练链路可运行，**不能据此声称力矩输入提高了任务成功率**。检查点和完整指标在测试工作树的 `result/torque_bc/`，训练数据在其 `data/franka_torque/`；这些目录被 Git 忽略。
