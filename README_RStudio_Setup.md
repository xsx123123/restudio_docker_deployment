# RStudio Docker Setup

This directory contains scripts to create and run a customized RStudio environment using Docker Compose.

## Documentation

- [English Documentation](README_RStudio_Setup.md)
- [中文文档](docs/README_RStudio_Setup_CN.md)

## Files

- `create_rstudio.py`: Main Python script to generate Dockerfile and docker-compose.yml (with colorful help!)
- `run_rstudio.sh`: Wrapper shell script for easier execution
- `rstudio_ops.sh`: General RStudio container operations script
- `rstudio_manage.sh`: Specific operations for managing current container
- `docker_templates/`: Templates for Docker configuration
  - `Dockerfile.j2`: Template for Dockerfile
  - `docker-compose.yml.j2`: Template for docker-compose file

## Features

- Automatically detects current user's UID/GID and home directory
- Finds available ports automatically (or use specified port)
- Customizable username, password, and container/image names
- Flexible volume mounting options
- Supports all rocker/rstudio:4 features
- **NEW**: Colorful help output with enhanced usability!
- **NEW**: Docker Compose and permissions checking
- **NEW**: Comprehensive logging with file output
- **NEW**: Container management scripts for easy operations
- **NEW**: Auto-generated success messages with next steps

## Usage

```bash
# Basic usage (auto-detects user info, finds available port)
python3 create_rstudio.py

# Or using the wrapper script
./run_rstudio.sh

# Show colorful help information
python3 create_rstudio.py --help

# With custom parameters
python3 create_rstudio.py --user myuser --password mypass --port 8787 --volumes "/path1:/path1" "/path2:/path2"

# Using current configuration (for jzhang user)
python3 create_rstudio.py --user jz --uid 1006 --gid 1001 --password zj109965 --port 50006 --home-dir /home/jzhang --container-name zj-rstudio-server --image-name zj-rstudio-image:latest --volumes "/data/jzhang:/data/jzhang" "/home/jzhang:/home/jzhang" "/data/jzhang/rstudio/jzhang:/home/jzhang"

# Generate files without running
python3 create_rstudio.py --no-run --user myuser --port 8787

# Use custom template files
python3 create_rstudio.py --dockerfile-template my_custom_dockerfile.j2 --compose-template my_custom_compose.j2
```

## Container Operations

After starting your RStudio container, use these management scripts:

```bash
# General operations
./rstudio_ops.sh start    # Start container
./rstudio_ops.sh stop     # Stop container  
./rstudio_ops.sh restart  # Restart container
./rstudio_ops.sh logs     # View logs
./rstudio_ops.sh exec     # Open shell in container
./rstudio_ops.sh status   # Check status

# Specific operations for current container
./rstudio_manage.sh start     # Start current container
./rstudio_manage.sh logs      # View current container logs
./rstudio_manage.sh exec      # Open root shell in container
./rstudio_manage.sh shell     # Open user shell in container
./rstudio_manage.sh status    # Check current container status
```

## Options

- `--user`: Username for RStudio (default: rstudio)
- `--uid`: User ID (default: current user ID)
- `--gid`: Group ID (default: current group ID)
- `--password`: Password for RStudio (default: rstudio)
- `--port`: Port to expose RStudio (default: finds available port starting from 50000)
- `--home-dir`: Home directory in container (default: current user home)
- `--container-name`: Container name (default: rstudio-[username]-server)
- `--image-name`: Image name (default: [username]-rstudio-image:latest)
- `--volumes`: Volumes to mount in format host_path[:container_path] (default: current directory)
- `--no-run`: Only generate files, do not run Docker Compose
- `--base-user`: Base user to remove in Dockerfile (default: rstudio_user)
- `--workdir`: Working directory for Docker build context (default: current directory)
- `--dockerfile-template`: Path to Dockerfile template (default: docker_templates/Dockerfile.j2)
- `--compose-template`: Path to docker-compose.yml template (default: docker_templates/docker-compose.yml.j2)

## Logging

The script generates logs in `rstudio_setup.log` for troubleshooting and audit purposes.