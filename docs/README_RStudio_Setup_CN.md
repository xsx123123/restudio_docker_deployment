# RStudio Docker 部署设置

此目录包含使用 Docker Compose 创建和运行自定义 RStudio 环境的脚本。

## 文件

- `create_rstudio.py`: 主要 Python 脚本，用于生成 Dockerfile 和 docker-compose.yml（包含彩色帮助！）
- `run_rstudio.sh`: 用于简化执行的包装 shell 脚本
- `rstudio_ops.sh`: 通用 RStudio 容器操作脚本
- `rstudio_manage.sh`: 用于管理当前容器的特定操作脚本
- `docker_templates/`: Docker 配置模板
  - `Dockerfile.j2`: Dockerfile 模板
  - `docker-compose.yml.j2`: docker-compose 文件模板

## 功能

- 自动检测当前用户的 UID/GID 和主目录
- 自动查找可用端口（或使用指定端口）
- 可自定义用户名、密码和容器/镜像名称
- 灵活的卷挂载选项
- 支持所有 rocker/rstudio:4 功能
- **新增**: 彩色帮助输出，增强可用性！
- **新增**: Docker Compose 和权限检查
- **新增**: 包含文件输出的全面日志记录
- **新增**: 用于简化操作的容器管理脚本
- **新增**: 自动生成的成功消息和后续步骤

## 使用方法

```bash
# 基本用法（自动检测用户信息，查找可用端口）
python3 create_rstudio.py

# 或使用包装脚本
./run_rstudio.sh

# 显示彩色帮助信息
python3 create_rstudio.py --help

# 使用自定义参数
python3 create_rstudio.py --user myuser --password mypass --port 8787 --volumes "/path1:/path1" "/path2:/path2"

# 使用当前配置（针对 jzhang 用户）
python3 create_rstudio.py --user jz --uid 1006 --gid 1001 --password zj109965 --port 50006 --home-dir /home/jzhang --container-name zj-rstudio-server --image-name zj-rstudio-image:latest --volumes "/data/jzhang:/data/jzhang" "/home/jzhang:/home/jzhang" "/data/jzhang/rstudio/jzhang:/home/jzhang"

# 仅生成文件而不运行
python3 create_rstudio.py --no-run --user myuser --port 8787

# 使用自定义模板文件
python3 create_rstudio.py --dockerfile-template my_custom_dockerfile.j2 --compose-template my_custom_compose.j2
```

## 容器操作

启动 RStudio 容器后，使用这些管理脚本：

```bash
# 通用操作
./rstudio_ops.sh start    # 启动容器
./rstudio_ops.sh stop     # 停止容器
./rstudio_ops.sh restart  # 重启容器
./rstudio_ops.sh logs     # 查看日志
./rstudio_ops.sh exec     # 在容器中打开 shell
./rstudio_ops.sh status   # 检查状态

# 当前容器的特定操作
./rstudio_manage.sh start     # 启动当前容器
./rstudio_manage.sh logs      # 查看当前容器日志
./rstudio_manage.sh exec      # 在容器中打开 root shell
./rstudio_manage.sh shell     # 在容器中打开用户 shell
./rstudio_manage.sh status    # 检查当前容器状态
```

## 选项

- `--user`: RStudio 的用户名（默认：rstudio）
- `--uid`: 用户 ID（默认：当前用户 ID）
- `--gid`: 组 ID（默认：当前组 ID）
- `--password`: RStudio 的密码（默认：rstudio）
- `--port`: 暴露 RStudio 的端口（默认：从 50000 开始查找可用端口）
- `--home-dir`: 容器中的主目录（默认：当前用户主目录）
- `--container-name`: 容器名称（默认：rstudio-[用户名]-server）
- `--image-name`: 镜像名称（默认：[用户名]-rstudio-image:latest）
- `--volumes`: 以 host_path[:container_path] 格式挂载的卷（默认：当前目录）
- `--no-run`: 仅生成文件，不运行 Docker Compose
- `--base-user`: 在 Dockerfile 中要删除的基用户（默认：rstudio_user）
- `--workdir`: Docker 构建上下文的工作目录（默认：当前目录）
- `--dockerfile-template`: Dockerfile 模板路径（默认：docker_templates/Dockerfile.j2）
- `--compose-template`: docker-compose.yml 模板路径（默认：docker_templates/docker-compose.yml.j2）

## 日志记录

脚本在 `rstudio_setup.log` 中生成日志，用于故障排除和审计目的。

## 文档

- [English Documentation](../README_RStudio_Setup.md)
- [中文文档](README_RStudio_Setup_CN.md)