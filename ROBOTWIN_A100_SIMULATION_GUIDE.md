# RoboTwin 在 A100-Server4 上启动仿真：通用操作手册

适用范围：当前 `/mnt/ceph2/srg/RoboTwin` 仓库中已有的 RoboTwin 任务，使用自动 expert 运行仿真并可选择采集数据。本手册的命令从**自己电脑登录服务器**开始，按实际执行顺序排列。服务器依赖路径是本机现状；换服务器时需重新核对。

## 先看：每次运行需要输入什么

下面的命令会**逐项提示你输入**，不需要修改命令正文。每次要决定的只有四个值：

| 输入项 | 输入什么 | 何时输入 |
| --- | --- | --- |
| `TASK_NAME` | `envs/` 下任务 Python 文件的文件名，**不带 `.py`** | 第 1 步 |
| `CONFIG_NAME` | `env_cfg/task_config/` 下配置文件的文件名，**不带 `.yml`** | 第 1 步 |
| `GPU_INDEX` | 集群允许使用的 GPU 索引；在本集群 `gpu:3` 不是申请 3 张卡 | 第 2 步 |
| `TIME_LIMIT` | 本次申请的最长时间，格式 `时:分:秒` | 第 2 步 |

**不要把任务名和配置名混淆**：任务名决定要做什么；配置名决定用什么机器人、采几条、保存什么数据。配置名也是输出目录的一部分，所以换一个配置名会生成一套新的目录。

## 第 0 步：从自己电脑登录服务器

在 **Windows PowerShell** 输入：

```powershell
ssh A100-Server4
```

以下第 1～7 步都在**服务器终端**输入。第 8 步下载视频时再回到 Windows PowerShell。

## 第 1 步：选择任务与配置；不用 GPU

先列出当前仓库可选的任务文件与配置文件，再运行下面的命令。终端会等待你依次输入任务名和配置名：

```bash
cd /mnt/ceph2/srg/RoboTwin
ls envs/*.py
ls env_cfg/task_config/*.yml
read -r -p '任务名（不带 .py）：' TASK_NAME
read -r -p '配置名（不带 .yml）：' CONFIG_NAME
export TASK_NAME CONFIG_NAME
ls "envs/${TASK_NAME}.py" "env_cfg/task_config/${CONFIG_NAME}.yml"
```

最后一条 `ls` 应显示两个文件。若任务文件不存在，重新输入正确的任务名；若配置文件不存在，可以按下方命令新建。没有确认两个文件都存在前，不要申请 GPU。

如果要新建一份配置，先在上面的提示中输入**没用过的新配置名**，避免覆盖旧实验，再执行：

```bash
cp -n env_cfg/task_config/_config_template.yml "env_cfg/task_config/${CONFIG_NAME}.yml"
nano "env_cfg/task_config/${CONFIG_NAME}.yml"
```

在编辑器里至少检查下面几项。编辑完成后保存退出，再用 `ls "env_cfg/task_config/${CONFIG_NAME}.yml"` 确认。模板默认用 Aloha，**想跑 Franka 必须改 `embodiment`**。

| 配置项 | 用途 | 常见设置 |
| --- | --- | --- |
| `embodiment` | 机器人类型 | 两台 Franka：`[franka-panda, franka-panda, 0.8]`；可用名称见 `env_cfg/task_config/_embodiment_config.yml` |
| `episode_num` | 目标成功演示总条数 | 先用 `1` 测试，批量采集再调大 |
| `use_seed` | 是否只使用已有 seed 列表 | 第一次通常用 `false` |
| `collect_data` | 是否保存正式数据 | 训练数据采集用 `true`；只测试 expert 的规划过程可用 `false` |
| `save_path` | 输出根目录 | 常用 `./data`；相对路径以 RoboTwin 项目目录为准 |
| `render_freq` | 实时 viewer 刷新间隔 | 无图形桌面的 A100 用 `0`；它不影响离线相机视频 |
| `camera`、`data_type` | 相机类型与要保存的数据模态 | 例如 RGB、关节位置、末端位姿；按实验目标调整 |

`collect_data: false` 不生成训练用 HDF5/MP4；再次运行已有成功 seed 的同一配置可能直接跳过规划。想重新测试，可使用新的配置名。当前 A100 会话没有图形桌面，`render_freq` 改成非零也不能直接在你电脑上弹出实时窗口。

## 第 2 步：申请 GPU

运行下面三行命令；前两行会提示你输入 GPU 索引和最长运行时间：

```bash
read -r -p 'GPU 索引：' GPU_INDEX
read -r -p '最长运行时间（时:分:秒）：' TIME_LIMIT
srun --export=ALL --gres=gpu:${GPU_INDEX} --time=${TIME_LIMIT} --pty bash
```

看到 `Granted job allocation ...` 才表示申请成功。`--export=ALL` 将第 1 步设置的 `TASK_NAME`、`CONFIG_NAME` 传入新 shell。进入新 shell 后执行：

```bash
cd /mnt/ceph2/srg/RoboTwin
echo "task=${TASK_NAME}, config=${CONFIG_NAME}"
```

如果 `echo` 后的任务名或配置名为空，先重新执行第 1 步的两行 `export`，再继续。

## 第 3 步：激活已有环境

```bash
source /mnt/ceph2/hjs/miniconda3/etc/profile.d/conda.sh
conda activate /mnt/ceph2/hjs/miniconda3/envs/robotwin
export PYTHONPATH=/mnt/ceph2/srg/tools/curobo-a100/src:/mnt/ceph2/srg/RoboTwin:/mnt/ceph2/srg/RoboTwin/XPolicyLab
```

命令提示符前应出现 `(robotwin)`。`PYTHONPATH` 首项让 Python 优先加载自己目录里为 A100 编译的 CuRobo；每次运行设置一次，不用重新编译，也不修改 hjs 的共享环境。

## 第 4 步：检查 GPU 和视频编码器

```bash
export PATH=/usr/bin:$PATH
which ffmpeg
ffmpeg -hide_banner -encoders 2>/dev/null | grep libx264
/mnt/ceph2/hjs/miniconda3/envs/robotwin/bin/python -c 'import torch; print(torch.cuda.get_device_name(0), torch.cuda.get_device_capability(0))'
```

在本机预期看到 `/usr/bin/ffmpeg`、`libx264`，以及 `NVIDIA A100-SXM4-80GB (8, 0)`。使用 Conda Python 的**绝对路径**，避免把 `/usr/bin` 放在 `PATH` 前面后误调用系统 Python。检查结果不符合预期时先停下排查。

## 第 5 步：启动 RoboTwin 仿真

```bash
/mnt/ceph2/hjs/miniconda3/envs/robotwin/bin/python scripts/collect_data.py "$TASK_NAME" "$CONFIG_NAME"
```

程序按配置先找能完成任务的 seed 和运动轨迹，再按轨迹重放并采集数据（仅当 `collect_data: true`）。`simulate data episode 0 success!` 说明**规划阶段**成功；要等采集、视频及 HDF5 合成全部完成，才算一条数据真正落盘。运行中若看到 `missing pytorch3d`，对当前未启用点云的 RGB 配置不构成已知阻断；启用点云时另查依赖。

## 第 6 步：查找输出文件

当配置的 `save_path: ./data` 时，输出遵循：

```text
/mnt/ceph2/srg/RoboTwin/data/<CONFIG_NAME>/<TASK_NAME>/<机器人目录>/
├── seed.txt
├── _traj_data/
├── instruction/
├── data/episode_0000000.hdf5
└── video/episode_0000000.mp4
```

`<机器人目录>` 由配置里的 `embodiment` 自动生成；如 `[franka-panda, franka-panda, 0.8]` 对应 `franka_panda_franka_panda`。不用猜目录名，可直接查：

```bash
find "./data/${CONFIG_NAME}/${TASK_NAME}" -type f -name '*.hdf5' -print
find "./data/${CONFIG_NAME}/${TASK_NAME}" -type f -name '*.mp4' -print
```

若配置的 `save_path` 不是 `./data`，把两条 `find` 命令开头的 `./data` 换成实际 `save_path`。某条 episode 已有 HDF5 时，脚本会从下一条开始；`episode_num` 是**目标总数**，不是本次再增加的数量。

### 为什么默认 MP4 只有一个相机视角？

当前合成代码只把 `head_camera` 生成默认 MP4。配置启用左右腕相机时，它们的 RGB 保存在 HDF5 的 `vision/cam_left_wrist/colors` 和 `vision/cam_right_wrist/colors`，不会自动成为两个 MP4。要额外导出，在服务器上设置本条 HDF5 路径并运行：

```bash
read -r -p '要导出的 HDF5 路径：' EPISODE_HDF5
PYTHONPATH=/mnt/ceph2/srg/RoboTwin PATH=/usr/bin:/bin /mnt/ceph2/hjs/miniconda3/envs/robotwin/bin/python scripts/export_camera_videos.py "$EPISODE_HDF5"
```

输入第 6 步查到的任一 HDF5 路径即可，例如形如 `./data/配置名/任务名/机器人目录/data/episode_0000000.hdf5`。这会在同一个 `video/` 目录生成带 `cam_left_wrist` 和 `cam_right_wrist` 后缀的 MP4。只需已有 HDF5，**导出视频不需要申请 GPU**。如果当前配置没开腕相机，该命令会报告缺少相机字段。

## 第 7 步：释放 GPU

在 `srun` 打开的 shell 中输入：

```bash
exit
squeue -u $USER
```

自己的作业号不再出现在 `squeue` 中才算释放。若还要退出 SSH，再输入一次 `exit`。

## 第 8 步：在 Windows 下载和观看视频

回到 **Windows PowerShell**。先用第 6 步的 `find` 找到真实的远端 MP4 路径，并在提示出现时粘贴该路径：

```powershell
$remoteVideo = Read-Host '粘贴服务器上的 MP4 绝对路径'
scp "A100-Server4:$remoteVideo" .
Start-Process (Join-Path (Get-Location) ($remoteVideo.Split('/')[-1]))
```

`scp` 末尾的 `.` 表示保存到本机 PowerShell 当前目录。观看腕部视角时，粘贴腕部 MP4 的完整远端路径即可。

## 运行失败时先查这三项

1. `No such task` 或配置文件不存在：核对第 1 步的 `TASK_NAME`、`CONFIG_NAME`，配置名不带 `.yml`。
2. CuRobo CUDA 架构报错：核对第 3 步的 `PYTHONPATH` 首项是否为自己的 `curobo-a100/src`，以及第 4 步是否确实拿到 A100。
3. `Unknown encoder 'libx264'` / `BrokenPipeError`：核对第 4 步 `which ffmpeg` 是否为 `/usr/bin/ffmpeg`；仿真成功不等于最终文件已保存。
