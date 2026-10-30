# RoboTwin 中文说明

[English](README.md) | 中文

<h1 align="center">
  <a href="https://robotwin-benchmark.github.io"><b>RoboTwin</b> 双臂机器人操作平台<br></a>
</h1>
<h2 align="center">最新版本：RoboTwin 2.0<br>🤲 <a href="https://robotwin-platform.github.io/">项目主页</a> | <a href="https://robotwin-platform.github.io/doc/">官方文档</a> | <a href="https://arxiv.org/abs/2506.18088">论文</a> | <a href="https://robotwin-platform.github.io/doc/community/index.html">社区</a> | <a href="https://robotwin-platform.github.io/leaderboard">排行榜</a></h2>

https://private-user-images.githubusercontent.com/88101805/463126988-e3ba1575-4411-4a36-ad65-f0b2f49890c3.mp4

**RoboTwin 2.0**（*ICML 2026*）— [项目主页](https://robotwin-platform.github.io/) · [文档](https://robotwin-platform.github.io/doc) · [论文](https://arxiv.org/abs/2506.18088) · [报告视频](https://www.bilibili.com/video/BV18p3izYE63/?spm_id_from=333.337.search-card.all.click) · [机器之心报道](https://mp.weixin.qq.com/s/SwORezmol2Qd9YdrGYchEA) · [排行榜](https://robotwin-platform.github.io/leaderboard)

<details>
<summary>早期论文与挑战赛报告</summary>

- **1.0 / 早期版本** — RoboTwin: Dual-Arm Robot Benchmark with Generative Digital Twins · *CVPR 2025 Highlight* [PDF](https://arxiv.org/pdf/2504.13059) / [arXiv](https://arxiv.org/abs/2504.13059) · *ECCV Workshop 2024 最佳论文* [PDF](https://arxiv.org/pdf/2409.02920) / [arXiv](https://arxiv.org/abs/2409.02920)
- **CVPR 2025 MEIS 挑战赛报告** — [PDF](https://arxiv.org/pdf/2506.23351) / [arXiv](https://arxiv.org/abs/2506.23351) · [量子位报道](https://mp.weixin.qq.com/s/qxqs9vvvHsAJ-0hoYANYzQ)

</details>

# 📚 概览

> 本 README 用于快速入门；完整操作说明请优先参考 [RoboTwin 官方文档](https://robotwin-platform.github.io/doc/)。

RoboTwin 2.0 与 [RoboDojo](https://github.com/RoboDojo-Benchmark/RoboDojo) 通过 [XPolicyLab](https://github.com/XPolicyLab/XPolicyLab) 共用策略部署与评估体系，支持单任务、多 GPU 以及远程策略服务器加本地仿真器等方式。

**默认分支：**[`main`](https://github.com/RoboTwin-Platform/RoboTwin/tree/main)（RoboTwin 2.0）。

<details>
<summary>其他分支（旧版本或特定用途）</summary>

- [IsaacLab-Arena](https://github.com/RoboTwin-Platform/RoboTwin/tree/IsaacLab-Arena) · [RLinf_support](https://github.com/RoboTwin-Platform/RoboTwin/tree/RLinf_support) · [WBCD-2026](https://github.com/RoboTwin-Platform/RoboTwin/tree/WBCD-2026)
- [RoboTwin-1.0](https://github.com/RoboTwin-Platform/RoboTwin/tree/RoboTwin-1.0) / [early_version](https://github.com/RoboTwin-Platform/RoboTwin/tree/early_version) · [gpt](https://github.com/RoboTwin-Platform/RoboTwin/tree/gpt)
- [Challenge-Cup-2025](https://github.com/RoboTwin-Platform/RoboTwin/tree/Challenge-Cup-2025) · [CVPR-Challenge-2025-Round1](https://github.com/RoboTwin-Platform/RoboTwin/tree/CVPR-Challenge-2025-Round1) / [Round2](https://github.com/RoboTwin-Platform/RoboTwin/tree/CVPR-Challenge-2025-Round2)

</details>

# 🐣 更新记录

- **2026/08/03**：加入基于 [XPolicyLab](https://github.com/XPolicyLab/XPolicyLab) 的策略评估，支持单任务评估、多任务多 GPU 调度，以及远程策略服务器与本地仿真器分离部署。
- **2026/03/03**：发布基于 RoboTwin 2.0 的记忆依赖型操作基准 [RMBench](https://github.com/RoboTwin-Platform/RMBench)。
- **2026/02/20**：在适合 VLA 开发的 [StarVLA](https://github.com/starVLA/starVLA) 代码库中提供使用支持。
- **2026/01/23**：更新 IsaacLab-Arena 和 [RLinf](https://github.com/RLinf/RLinf) 支持（由 RLinf 团队贡献）。
- **2025/08/28**：更新 RoboTwin 2.0 [论文](https://arxiv.org/pdf/2506.18088)。
- **2025/08/25**：修复 ACT 部署代码并更新[排行榜](https://robotwin-platform.github.io/leaderboard)。
- **2025/08/06**：发布 RoboTwin 2.0 [排行榜](https://robotwin-platform.github.io/leaderboard)。
- **2025/07/23**：RoboTwin 2.0 获 ChinaSI 2025 杰出海报（排名第一）。
- **2025/07/19**：修复 DP3 评估代码错误，并计划更新 RoboTwin 2.0 论文。
- **2025/07/09**：更新末端位姿控制模式，详见[机器人控制文档](https://robotwin-platform.github.io/doc/usage/control-robot.html)。
- **2025/07/08**：上传第十九届挑战杯分支 [Challenge-Cup-2025](https://github.com/RoboTwin-Platform/RoboTwin/tree/Challenge-Cup-2025)。
- **2025/07/02**：修复 Piper 腕部问题（[issue #104](https://github.com/RoboTwin-Platform/RoboTwin/issues/104)）；需要重新下载对应的机器人资产。
- **2025/07/01**：发布 RoboTwin 双臂协作挑战赛（CVPR 2025 MEIS Workshop）[技术报告](https://arxiv.org/abs/2506.23351)。
- **2025/06/21**：发布 [RoboTwin 2.0](https://robotwin-platform.github.io/)。
- **2025/04/11**：RoboTwin 论文获评 CVPR Highlight。
- **2025/02/27**：RoboTwin 被 CVPR 2025 接收。
- **2024/09/30**：RoboTwin 早期版本获 ECCV Workshop 最佳论文奖。
- **2024/09/20**：RoboTwin 正式发布。

# 🛠️ 安装

安装方法见 [RoboTwin 2.0 文档：安装与下载](https://robotwin-platform.github.io/doc/usage/robotwin-install.html)。官方给出的安装时间约为 20 分钟。

XPolicyLab 作为 Git 子模块包含在仓库中。首次克隆时递归获取子模块：

```bash
git clone --recurse-submodules https://github.com/RoboTwin-Platform/RoboTwin.git
cd RoboTwin
```

如果已有仓库，初始化 RoboTwin 当前固定的 XPolicyLab 版本：

```bash
git submodule update --init --recursive XPolicyLab
```

若要拉取 XPolicyLab 所配置的 `main` 分支最新提交，并更新 RoboTwin 中的子模块版本指针：

```bash
bash scripts/update_xpolicylab.sh
# 可选：暂存版本指针并重新安装可编辑包
bash scripts/update_xpolicylab.sh --stage --install
```

# 🤷‍♂️ 任务信息

各任务说明见 [RoboTwin 2.0 任务文档](https://robotwin-platform.github.io/doc/tasks/index.html)。

<p align="center">
  <img src="./assets/files/50_tasks.gif" width="100%">
</p>

# 🧑🏻‍💻 使用方法

## 官方文档

> 完整说明见 [RoboTwin 官方文档](https://robotwin-platform.github.io/doc/)，建议从[使用指南](https://robotwin-platform.github.io/doc/usage/index.html)开始。如文档与本 README 不一致，以官方文档为准。

## 获取数据

开源的 [RoboTwin 数据集](https://huggingface.co/datasets/TianxingChen/RoboTwin2.0/tree/main/dataset)提供超过 10 万条预采集轨迹。官方建议优先下载预采集数据（第 1 步），可直接用于训练；需要自定义任务配置、域随机化或机器人配置时，再自行采集（第 2 步）。

> **图像解码始终使用 `decode_image_bit`，编码始终使用 `encode_image_bit`。** 下载和自行采集的 episode 都将相机图像保存为编码后的字节。存量数据有两种字节格式，自行实现解码可能在其中一种格式上正确、在另一种格式上颠倒颜色通道。本仓库的 [`data/decode_image_bit.py`](data/decode_image_bit.py) 提供了与 `XPolicyLab.utils.process_data` 相同的函数；若 XPolicyLab 可用，优先从那里导入：
>
> ```python
> from XPolicyLab.utils.process_data import decode_image_bit, encode_image_bit
> rgb = decode_image_bit(image_bits)  # 所有数据版本都返回 RGB
> ```
>
> | 格式 | 写入方式 | 常规解码器读取时的结果 |
> | --- | --- | --- |
> | **legacy（旧格式）** | 把 RGB 数组直接传给按 BGR 解释输入的 `cv2.imencode` | 红蓝通道颠倒；字节相对 JPEG 标准的通道顺序是反的，而 `cv2.imdecode` 会再反转一次 |
> | **standard（标准格式）** | `encode_image_bit` 先转换为 BGR，并写入内容为 `XPL-RGB1` 的 JPEG `COM` 标记 | 颜色正确 |
>
> 旧数据不会被迁移，因为 JPEG 无法无损交换颜色通道；两种格式会长期并存，甚至出现在同一次训练中。新采集的 episode 使用标准格式。`decode_image_bit` 能识别两者并统一返回 RGB，因此**不要**再追加 `cv2.cvtColor(..., COLOR_BGR2RGB)`。官方 LeRobot 转换脚本已经调用这个函数；自定义的 HDF5 训练数据加载器也必须如此。采集时不要用裸 `cv2.imencode` 替代 `encode_image_bit`，否则会缺少标记并导致读取时通道颠倒。评估时策略服务器收到的已经是解码后的 RGB，`model.py` 不应重复解码。详见 [XPolicyLab 图像解码说明](https://github.com/XPolicyLab/XPolicyLab#decode-only-through-decode_image_bit)。

<img src="./assets/files/domain_randomization.png" alt="域随机化示意图" style="display: block; margin: auto; width: 100%;">

## 1. 下载 XPolicyLab 格式数据（推荐）

从 Hugging Face 下载并解压所有可用的 XPolicyLab 格式轨迹：

```bash
bash scripts/download_xpolicylab_data.sh
```

只下载指定任务时，将任务名作为参数：

```bash
bash scripts/download_xpolicylab_data.sh adjust_bottle beat_block_hammer
```

下载与解压均可并行执行，默认各使用 8 个工作进程。每个任务的 ZIP 下载完就会开始解压，无需等待其他任务。可调整并行度：

```bash
# 下载工作进程数；解压默认跟随 HF_MAX_WORKERS
HF_MAX_WORKERS=8 HF_EXTRACT_WORKERS=16 bash scripts/download_xpolicylab_data.sh
```

下载的数据位于 `data/demo_clean/<task_name>/aloha_agilex/data/`。自行采集的数据则位于 `data/<task_config>/...`。

## 2. 运行任务与采集数据（按需）

需要自定义任务配置、域随机化或机器人配置时，可以自行采集。以下命令会先为目标采集数量搜索随机种子，再重放这些种子进行采集：

```bash
bash collect_data.sh ${task_name} ${task_config} ${gpu_id}
# 示例：bash collect_data.sh beat_block_hammer demo_randomized 0
```

演示数据直接保存为 XPolicyLab 轨迹格式，无需再次转换：

```text
data/<task_config>/<task_name>/<embodiment>/data/episode_0000000.hdf5
```

`<embodiment>` 由任务配置中的 `embodiment` 字段决定；默认 `aloha-agilex` 对应目录名 `aloha_agilex`。

## 3. 转换为 LeRobot 数据集（按需）

许多 XPolicyLab 策略使用 LeRobot 数据集训练。取得 `data/<task_config>/<task>/<embodiment>/data/` 下的 XPolicyLab 格式 HDF5 后，可使用 `XPolicyLab/scripts/` 中的通用脚本转换。这些脚本已经通过 `decode_image_bit` 解码；如需修改脚本，不要换成 `cv2.imdecode` 或 PIL。两种图像字节格式只有 `decode_image_bit` 能正确区分。

数据选择模式为 `<task_config>.<task>.<embodiment>`，可使用 `*` 通配符；模式对应 RoboTwin 根目录旁的 `data/`，例如 `demo_clean.*.aloha_agilex`。`--data_type` 保持默认值 `RoboDojo`，因为 RoboTwin 的 XPolicyLab 轨迹采用相同的 HDF5 布局。

转换环境须安装匹配版本的 LeRobot（v2.1 或 v3.0）。结果写入 `HF_LEROBOT_HOME`，默认是 `~/.cache/huggingface/lerobot`；请将其指向空间充足的磁盘：

```bash
export HF_LEROBOT_HOME=/path/with/enough/space/lerobot

# LeRobot v2.1：转换所有 demo_clean 任务
python XPolicyLab/scripts/transform_lerobot_v21_format.py \
  "demo_clean.*.aloha_agilex" \
  --repo_id robotwin_demo_clean_aloha_agilex \
  --max_episode 50

# LeRobot v3.0：转换同一批任务
python XPolicyLab/scripts/transform_lerobot_v30_format.py \
  "demo_clean.*.aloha_agilex" \
  --repo_id robotwin_demo_clean_aloha_agilex_v30 \
  --max_episode 50

# 单个任务
python XPolicyLab/scripts/transform_lerobot_v21_format.py \
  "demo_clean.beat_block_hammer.aloha_agilex" \
  --repo_id beat_block_hammer_demo_clean
```

常用参数：`--repo_id` 指定输出数据集名；`--max_episode` 限制每个任务及机器人配置的 episode 数；`--resolution HxW` 或 `--image_height` / `--image_width` 指定分辨率（默认自动检测；RoboTwin 常见值为 `240x320`）。输出目录为 `${HF_LEROBOT_HOME}/<repo_id>`。

## 4. 修改任务配置

详见 [RoboTwin 2.0 任务配置文档](https://robotwin-platform.github.io/doc/usage/configurations.html)。`demo_clean` 和 `demo_randomized` 等配置位于 `env_cfg/task_config/`。

## 5. 通过 XPolicyLab 评估策略

所有评估都通过 `scripts/eval_policy.sh` 进行。策略适配器必须位于 `XPolicyLab/policy/<policy_name>/`；可参阅 [XPolicyLab 策略列表](https://github.com/XPolicyLab/XPolicyLab/tree/main/policy)。

`--env-cfg-type` 选择 XPolicyLab 的动作配置（对照 `XPolicyLab/utils/robot/_robot_info.json` 验证；`arx_x5` 对应 RoboTwin 默认的 aloha-agilex 布局），仿真器使用的机器人配置仍由 `--task-config` 控制。

**本地评估（多任务、多 GPU）：**调度器会在 GPU 池中为每个任务启动策略服务器与仿真器。任务列表和 GPU 设置位于 `env_cfg/eval/all_tasks.yml`；如只评估一个任务，可将 `tasks` 精简为一项：

```bash
bash scripts/eval_policy.sh multitask \
  --config env_cfg/eval/all_tasks.yml \
  --policy-name <policy_name> \
  --ckpt-name <checkpoint> \
  --env-cfg-type arx_x5 \
  --policy-conda-env <policy_env> \
  --eval-env-conda-env <robotwin_env> \
  --action-type <action_type>
```

加上 `--dry-run` 可以只验证调度计划，不启动任务。结果默认写入 `eval_result/multitask/`。

**分离部署（远程策略服务器 + 本地仿真器）：**先在策略服务器所在主机启动服务池，再让仿真主机上的调度器连接它：

```bash
# 在策略服务器主机运行，先填写占位参数：
bash scripts/eval_policy.sh serve --config env_cfg/eval/remote_server.yml

# 在仿真器主机运行：
bash scripts/eval_policy.sh multitask \
  --config env_cfg/eval/all_tasks.yml \
  --policy-name <policy_name> \
  --env-cfg-type arx_x5 \
  --eval-env-conda-env <robotwin_env> \
  --enable-remote \
  --policy-server-ip <server_ip> --policy-server-port <port>
```

`--policy-server-ip` / `--policy-server-port` 可重复指定以使用服务器池；也可以在评估配置中设置 `enable_remote`、`policy_server_ip`、`policy_server_port`。

# 🏄‍♂️ 实验与排行榜

RoboTwin 平台适合研究：

1. 单任务微调能力
2. 视觉鲁棒性
3. 语言多样性鲁棒性（语言条件）
4. 多任务能力
5. 跨机器人配置性能

完整排行榜和评估设置见 [RoboTwin 排行榜](https://robotwin-platform.github.io/leaderboard)。

# 💽 预采集的大规模数据集

见 Hugging Face 上的 [RoboTwin 2.0 数据集](https://huggingface.co/datasets/TianxingChen/RoboTwin2.0/tree/main/dataset)。

# 🎯 官方基准模型检查点

见 Hugging Face 上的 [RoboTwin 2.0 检查点](https://huggingface.co/datasets/TianxingChen/RoboTwin2.0/tree/main/cotrain_ckpt)。

# 👍 引用

如果本项目对你的研究有帮助，请考虑引用以下论文。

**RoboTwin 2.0：**A Scalable Data Generator and Benchmark with Strong Domain Randomization for Robust Bimanual Robotic Manipulation

```bibtex
@article{chen2025robotwin,
  title={Robotwin 2.0: A scalable data generator and benchmark with strong domain randomization for robust bimanual robotic manipulation},
  author={Chen, Tianxing and Chen, Zanxin and Chen, Baijun and Cai, Zijian and Liu, Yibin and Li, Zixuan and Liang, Qiwei and Lin, Xianliang and Ge, Yiheng and Gu, Zhenyu and others},
  journal={arXiv preprint arXiv:2506.18088},
  year={2025}
}
```

**RoboTwin：**Dual-Arm Robot Benchmark with Generative Digital Twins，CVPR 2025 Highlight

```bibtex
@InProceedings{Mu_2025_CVPR,
    author    = {Mu, Yao and Chen, Tianxing and Chen, Zanxin and Peng, Shijia and Lan, Zhiqian and Gao, Zeyu and Liang, Zhixuan and Yu, Qiaojun and Zou, Yude and Xu, Mingkun and Lin, Lunkai and Xie, Zhiqiang and Ding, Mingyu and Luo, Ping},
    title     = {RoboTwin: Dual-Arm Robot Benchmark with Generative Digital Twins},
    booktitle = {Proceedings of the Computer Vision and Pattern Recognition Conference (CVPR)},
    month     = {June},
    year      = {2025},
    pages     = {27649-27660}
}
```

**挑战赛报告：**Benchmarking Generalizable Bimanual Manipulation: RoboTwin Dual-Arm Collaboration Challenge at CVPR 2025 MEIS Workshop

```bibtex
@article{chen2025benchmarking,
  title={Benchmarking Generalizable Bimanual Manipulation: RoboTwin Dual-Arm Collaboration Challenge at CVPR 2025 MEIS Workshop},
  author={Chen, Tianxing and Wang, Kaixuan and Yang, Zhaohui and Zhang, Yuhao and Chen, Zanxin and Chen, Baijun and Dong, Wanxi and Liu, Ziyuan and Chen, Dong and Yang, Tianshuo and others},
  journal={arXiv preprint arXiv:2506.23351},
  year={2025}
}
```

**RoboTwin 早期版本：**Dual-Arm Robot Benchmark with Generative Digital Twins，ECCV Workshop 2024 最佳论文

```bibtex
@article{mu2024robotwin,
  title={RoboTwin: Dual-Arm Robot Benchmark with Generative Digital Twins (early version)},
  author={Mu, Yao and Chen, Tianxing and Peng, Shijia and Chen, Zanxin and Gao, Zeyu and Zou, Yude and Lin, Lunkai and Xie, Zhiqiang and Luo, Ping},
  journal={arXiv preprint arXiv:2409.02920},
  year={2024}
}
```

# 😺 致谢

**软件支持：**D-Robotics；**硬件支持：**AgileX Robotics；**AIGC 支持：**Deemos。

如有疑问或建议，请联系 [Tianxing Chen](https://tianxingchen.github.io)。

# 🏷️ 许可证

本仓库使用 MIT 许可证，详见 [LICENSE](./LICENSE)。
