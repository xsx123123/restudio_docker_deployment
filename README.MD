使用 Docker 快速部署 RStudio Server
本文档旨在指导用户如何使用提供的 docker-compose.yml 和 Dockerfile 文件，通过 Docker 快速部署一个个人专属的 RStudio Server 服务。

通过 Docker 进行部署，可以为您提供一个独立、便携且易于管理的数据分析环境。

依赖条件
在开始之前，请确保您的服务器上已经安装了以下软件：

Docker

Docker Compose

文件结构
您需要准备以下两个文件，并将它们放置在同一个目录下。

.
├── docker-compose.yml  # 定义服务配置，如端口、密码、数据卷等
└── Dockerfile          # 定义镜像构建过程，如基础镜像、用户名等
配置说明
在部署之前，您必须根据自己的需求和服务器环境，修改以下两个文件中的配置项。

1. 设置用户名 (Dockerfile)
打开 Dockerfile 文件，修改 DEFAULT_USER 环境变量为您想要的登录用户名。

Dockerfile

# 1. 基于 rocker/verse:4 镜像
FROM rocker/verse:4

# 2. 设置环境变量，指定要创建的新用户名
#    将下面的 "jz" 修改为您自己的用户名
ENV DEFAULT_USER=你的用户名

# 3. 执行脚本来创建新用户
#    - 首先检查是否存在 UID 为 1000 的用户，如果存在则删除
#    - 然后运行 rocker 镜像自带的脚本来创建 new_user
RUN if grep -q ":1000:" /etc/passwd; then \
        userdel --remove "$(id -un 1000)"; \
    fi && \
    /rocker_scripts/default_user.sh
2. 设置密码、端口和数据卷 (docker-compose.yml)
打开 docker-compose.yml 文件，进行以下关键修改：

YAML

services:
  rstudio:
    build:
      context: .
      dockerfile: dockerfile
    ports:
      # 【必须修改】将 "50006" 修改为您服务器上一个未被占用的端口
      - "50006:8787"
    environment:
      # 【必须修改】将 "zj109965" 修改为您自己的强密码
      PASSWORD: 你的强密码
    volumes:
      # 【必须修改】以下所有 ":" 左边的路径，都必须修改为您服务器上的【绝对路径】
      # 作用：将服务器本地的目录挂载到容器中，以实现数据持久化
      # 示例： - /your/server/path/data:/data/jzhang:rw

      # 挂载数据目录 (请修改为你自己的)
      - /data/jzhang:/data/jzhang:rw
      # 挂载用户主目录 (请修改为你自己的)
      - /home/jzhang:/home/jzhang:rw
      # 挂载RStudio的配置目录，用于保存界面设置等 (请修改为你自己的)
      - /home/jzhang/rstudio/.rstudio_config:/home/rstudio/.config/rstudio
      # 挂载RStudio的工作区目录 (请修改为你自己的)
      - /home/jzhang/rstudio/workspace:/home/rstudio/workspace
修改项详解:

ports:

"50006:8787" 中，冒号左边的 50006 是您服务器对外暴露的端口。如果该端口已被占用，请务必修改为一个未被使用的端口。

冒号右边的 8787 是容器内部 RStudio Server 的默认端口，请勿修改。

environment.PASSWORD:

这里设置的是 RStudio Server 的登录密码，请务必修改为一个安全的强密码。

volumes:

数据卷用于实现数据的持久化。它将您服务器上的目录（宿主机目录）映射到 Docker 容器内部。

您必须将每一行中冒号（:）左边的路径（如 /data/jzhang）修改为您自己服务器上的绝对路径。

在启动服务前，请确保这些在服务器上的目录已经被创建。

部署步骤
准备文件:
将修改好的 docker-compose.yml 和 Dockerfile 放置在服务器的同一个目录下。

创建挂载目录:
根据您在 docker-compose.yml 中设置的 volumes 路径，在服务器上提前创建好这些目录。例如：

Bash

# 以下路径请替换为您自己设置的路径
mkdir -p /data/jzhang
mkdir -p /home/jzhang
mkdir -p /home/jzhang/rstudio/.rstudio_config
mkdir -p /home/jzhang/rstudio/workspace
启动服务:
在存放 docker-compose.yml 文件的目录下，执行以下命令：

Bash

docker-compose up -d
该命令会根据 Dockerfile 构建镜像，然后以后台守护模式 (-d) 启动服务。首次执行会需要一些时间来下载基础镜像和构建。

检查状态:
您可以使用以下命令查看服务是否成功启动：

Bash

docker-compose ps
如果看到 State 为 Up，则表示启动成功。

访问和使用
打开浏览器: 在您的浏览器中，输入 http://<服务器IP地址>:<您设置的端口>。

例如：http://192.168.1.100:50006

登录:

Username: 输入您在 Dockerfile 中设置的用户名。

Password: 输入您在 docker-compose.yml 中设置的密码。

开始使用: 登录成功后，您就可以开始使用 RStudio Server 了。您在 volumes 中挂载的服务器目录会出现在 RStudio 右下角的文件浏览器中。

维护服务
停止服务
如果您想停止 RStudio 服务，请在 docker-compose.yml 所在的目录下执行：

Bash

docker-compose down
该命令会停止并移除容器。由于您的数据和配置都通过数据卷挂载在服务器本地，所有工作都不会丢失。

重启服务
若要重新启动，只需再次执行：

Bash

docker-compose up -d