#!/usr/bin/env python3
"""
Script to create and run a customized RStudio Docker Compose setup based on rocker/rstudio
"""

import argparse
import os
import subprocess
import sys
import pwd
import grp
import socket
import logging
from pathlib import Path
import yaml

try:
    from jinja2 import Template
except ImportError:
    print("Error: jinja2 is not installed. Please install it using 'pip install jinja2'")
    sys.exit(1)

try:
    from colorama import init, Fore, Back, Style
    init()  # Initialize colorama
except ImportError:
    print("Warning: colorama is not installed. Install it using 'pip install colorama' for colored output.")
    # Define dummy color classes if colorama is not available
    class DummyColor:
        RED = ''
        GREEN = ''
        YELLOW = ''
        BLUE = ''
        MAGENTA = ''
        CYAN = ''
        WHITE = ''
        RESET = ''
    Fore = DummyColor()
    Back = DummyColor()
    Style = DummyColor()


def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('rstudio_setup.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(__name__)


def check_docker_compose():
    """Check if Docker and Docker Compose are installed and accessible"""
    logger = logging.getLogger(__name__)
    
    # Check if docker is installed and accessible
    try:
        result = subprocess.run(['docker', '--version'], 
                                capture_output=True, text=True, check=True)
        logger.info(f"Docker version: {result.stdout.strip()}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        logger.error("Docker is not installed or not accessible. Please install Docker.")
        return False

    # Check if docker-compose is installed and accessible
    try:
        result = subprocess.run(['docker-compose', '--version'], 
                                capture_output=True, text=True, check=True)
        logger.info(f"Docker Compose version: {result.stdout.strip()}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        try:
            # For newer Docker versions with docker compose (not docker-compose)
            result = subprocess.run(['docker', 'compose', 'version'], 
                                    capture_output=True, text=True, check=True)
            logger.info(f"Docker Compose version: {result.stdout.strip()}")
        except (subprocess.CalledProcessError, FileNotFoundError):
            logger.error("Docker Compose is not installed or not accessible. Please install Docker Compose.")
            return False

    # Check if user has permissions to run Docker
    try:
        result = subprocess.run(['docker', 'ps'], 
                                capture_output=True, text=True, check=True)
        logger.info("Docker permissions OK")
    except (subprocess.CalledProcessError, FileNotFoundError):
        logger.error("User doesn't have permission to run Docker. Add user to docker group: sudo usermod -aG docker $USER")
        return False

    return True


def check_port(port):
    """Check if a port is available"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('localhost', port))
            return True
        except OSError:
            return False


def get_available_port(start_port=50000):
    """Find an available port starting from start_port"""
    port = start_port
    while port < 65535:
        if check_port(port):
            return port
        port += 1
    return None


def get_current_user_info():
    """Get current user's UID, GID, username, and home directory"""
    user_info = pwd.getpwuid(os.getuid())
    group_info = grp.getgrgid(user_info.pw_gid)
    
    return {
        'username': user_info.pw_name,
        'uid': user_info.pw_uid,
        'gid': user_info.pw_gid,
        'groupname': group_info.gr_name,
        'home_dir': user_info.pw_dir
    }


def load_template(template_path):
    """Load a Jinja2 template from file"""
    with open(template_path, 'r') as f:
        return Template(f.read())


def create_dockerfile(user='rstudio', base_user='rstudio_user', template_path='docker_templates/Dockerfile.j2'):
    """Create a Dockerfile from template with the specified parameters"""
    template = load_template(template_path)
    return template.render(user=user, base_user=base_user)


def create_compose_file(container_name, image_name, port, password, userid, groupid, home_dir, volumes, template_path='docker_templates/docker-compose.yml.j2'):
    """Create a docker-compose.yml from template with the specified parameters"""
    # Process volumes
    processed_volumes = []
    for volume in volumes:
        parts = volume.split(':')
        if len(parts) == 2:
            host_path, container_path = parts
            processed_volumes.append(f"{host_path}:{container_path}:rw")
        else:
            # If no container path specified, use same path in container
            processed_volumes.append(f"{parts[0]}:{parts[0]}:rw")
    
    template = load_template(template_path)
    return template.render(
        container_name=container_name,
        image_name=image_name,
        port=port,
        password=password,
        userid=userid,
        groupid=groupid,
        home_dir=home_dir,
        volumes=processed_volumes
    )


class ColoredArgumentParser(argparse.ArgumentParser):
    def format_help(self):
        # Print the custom header with colors
        print(f"{Fore.BLUE}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}RStudio Docker Setup Script{Style.RESET_ALL}")
        print(f"{Fore.BLUE}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Create and run a customized RStudio Docker Compose setup{Style.RESET_ALL}")
        print(f"{Fore.CYAN}based on rocker/rstudio:4 image{Style.RESET_ALL}")
        print()
        
        # Get the default help text
        help_text = super().format_help()
        
        # Apply colorization to various sections
        lines = help_text.split('\n')
        colored_lines = []
        
        for line in lines:
            # Colorize section headers
            if line.strip().endswith(':') and not any(col in line for col in [Fore.MAGENTA, Fore.GREEN, Fore.CYAN]):
                colored_lines.append(f"{Fore.MAGENTA}{line}{Style.RESET_ALL}")
            # Colorize option names
            elif line.lstrip().startswith('--') or line.lstrip().startswith('-'):
                # Find option names and help text
                if '  ' in line:  # Has help text after option
                    parts = line.split('  ', 1)  # Split on first occurrence of 2 spaces
                    if len(parts) == 2:
                        option_part = parts[0]
                        help_part = parts[1]
                        colored_line = f"{Fore.CYAN}{option_part}{Style.RESET_ALL}  {Fore.GREEN}{help_part}{Style.RESET_ALL}"
                        colored_lines.append(colored_line)
                    else:
                        colored_lines.append(f"{Fore.CYAN}{line}{Style.RESET_ALL}")
                else:
                    colored_lines.append(f"{Fore.CYAN}{line}{Style.RESET_ALL}")
            else:
                colored_lines.append(line)
        
        result = '\n'.join(colored_lines)
        result += f"\n{Fore.YELLOW}Examples:{Style.RESET_ALL}\n"
        result += f"  {Fore.WHITE}# Basic usage (auto-detects user info, finds available port){Style.RESET_ALL}\n"
        result += f"  {Fore.GREEN}python3 create_rstudio.py{Style.RESET_ALL}\n"
        result += f"\n"
        result += f"  {Fore.WHITE}# Using current configuration (for jzhang user){Style.RESET_ALL}\n"
        result += f"  {Fore.GREEN}python3 create_rstudio.py --user jz --uid 1006 --gid 1001 --password zj109965{Style.RESET_ALL}\n"  
        result += f"  {Fore.GREEN}  --port 50006 --home-dir /home/jzhang --container-name zj-rstudio-server{Style.RESET_ALL}\n"
        result += f"  {Fore.GREEN}  --image-name zj-rstudio-image:latest --volumes \"/data/jzhang:/data/jzhang\"{Style.RESET_ALL}\n"
        result += f"  {Fore.GREEN}  \"/home/jzhang:/home/jzhang\" \"/data/jzhang/rstudio/jzhang:/home/jzhang\"{Style.RESET_ALL}\n"
        result += f"\n{Fore.BLUE}{'='*60}{Style.RESET_ALL}"
        
        return result


def main():
    logger = setup_logging()
    
    parser = ColoredArgumentParser(
        description='',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=''
    )
    
    # Main configuration options
    general_group = parser.add_argument_group('User Configuration')
    general_group.add_argument('--user', type=str, default='rstudio', 
                             help='Username for RStudio (default: rstudio)')
    general_group.add_argument('--uid', type=int, 
                             help='User ID (default: current user ID)')
    general_group.add_argument('--gid', type=int, 
                             help='Group ID (default: current group ID)')
    general_group.add_argument('--password', type=str, default='rstudio', 
                             help='Password for RStudio (default: rstudio)')
    general_group.add_argument('--home-dir', type=str, 
                             help='Home directory in container (default: current user home)')

    # Server configuration options
    server_group = parser.add_argument_group('Server Configuration')
    server_group.add_argument('--port', type=int, 
                            help='Port to expose RStudio (default: finds available port starting from 50000)')
    server_group.add_argument('--container-name', type=str, 
                            help='Container name (default: rstudio-[username]-server)')
    server_group.add_argument('--image-name', type=str, 
                            help='Image name (default: [username]-rstudio-image:latest)')

    # Volumes and file system options
    volume_group = parser.add_argument_group('Volume Configuration')
    volume_group.add_argument('--volumes', nargs='*', default=[], 
                            help='Volumes to mount in format host_path[:container_path] (default: current directory)')

    # Advanced options
    advanced_group = parser.add_argument_group('Advanced Options')
    advanced_group.add_argument('--no-run', action='store_true', 
                              help='Only generate files, do not run Docker Compose')
    advanced_group.add_argument('--base-user', type=str, default='rstudio_user', 
                              help='Base user to remove in Dockerfile (default: rstudio_user)')
    advanced_group.add_argument('--workdir', type=str, default='.', 
                              help='Working directory for Docker build context (default: current directory)')
    advanced_group.add_argument('--dockerfile-template', type=str, default='docker_templates/Dockerfile.j2', 
                              help='Path to Dockerfile template (default: docker_templates/Dockerfile.j2)')
    advanced_group.add_argument('--compose-template', type=str, default='docker_templates/docker-compose.yml.j2', 
                              help='Path to docker-compose.yml template (default: docker_templates/docker-compose.yml.j2)')
    
    # If no arguments provided, show help
    if len(sys.argv) == 1:
        parser.print_help()
        return
    
    args = parser.parse_args()
    
    logger.info("Starting RStudio Docker setup process...")
    
    # Check Docker and Docker Compose availability
    if not check_docker_compose():
        logger.error("Docker or Docker Compose requirements not met. Exiting.")
        sys.exit(1)
    
    logger.info("Docker and Docker Compose are properly installed and accessible.")
    
    # Get current user info if not provided
    current_user_info = get_current_user_info()
    
    # Set defaults based on current user if not provided
    if args.uid is None:
        args.uid = current_user_info['uid']
    if args.gid is None:
        args.gid = current_user_info['gid']
    if args.home_dir is None:
        args.home_dir = current_user_info['home_dir']
    if args.container_name is None:
        args.container_name = f"rstudio-{args.user}-server"
    if args.image_name is None:
        args.image_name = f"{args.user}-rstudio-image:latest"
    
    # Find available port if not provided
    if args.port is None:
        logger.info("Finding available port starting from 50000...")
        port = get_available_port(50000)
        if port is None:
            logger.error("No available ports found!")
            sys.exit(1)
        args.port = port
        logger.info(f"Using port: {args.port}")
    else:
        if not check_port(args.port):
            logger.error(f"Port {args.port} is already in use!")
            sys.exit(1)
    
    # Set default volumes if none provided
    if not args.volumes:
        args.volumes = [f"{os.getcwd()}:{os.getcwd()}"]
    
    # Create Dockerfile from template
    logger.info("Creating Dockerfile from template...")
    dockerfile_content = create_dockerfile(args.user, args.base_user, args.dockerfile_template)
    with open(os.path.join(args.workdir, 'dockerfile'), 'w') as f:
        f.write(dockerfile_content)
    
    # Create Docker Compose file from template
    logger.info("Creating docker-compose.yml from template...")
    compose_content = create_compose_file(
        args.container_name,
        args.image_name,
        args.port,
        args.password,
        args.uid,
        args.gid,
        args.home_dir,
        args.volumes,
        args.compose_template
    )
    
    with open(os.path.join(args.workdir, 'docker-compose.yml'), 'w') as f:
        f.write(compose_content)
    
    logger.info("Dockerfile and docker-compose.yml created successfully!")
    logger.info(f"Container name: {args.container_name}")
    logger.info(f"Image name: {args.image_name}")
    logger.info(f"Port: {args.port}")
    logger.info(f"User: {args.user} (UID: {args.uid}, GID: {args.gid})")
    logger.info(f"Home directory: {args.home_dir}")
    logger.info(f"Volumes: {args.volumes}")
    
    if not args.no_run:
        logger.info("Building and running Docker Compose...")
        try:
            # Build and run Docker Compose
            result = subprocess.run(['docker-compose', '-f', os.path.join(args.workdir, 'docker-compose.yml'), 'up', '-d'], 
                                  capture_output=True, text=True, check=True)
            logger.info(f"RStudio server is now running at http://localhost:{args.port}")
            logger.info(f"Container logs available with: docker logs {args.container_name}")
            logger.info("RStudio container setup completed successfully!")
            print(f"\n{Fore.GREEN}RStudio container is now running!{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Access RStudio at: {Fore.YELLOW}http://localhost:{args.port}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Container name: {Fore.YELLOW}{args.container_name}{Style.RESET_ALL}")
            print(f"\n{Fore.BLUE}Common operations:{Style.RESET_ALL}")
            print(f"  {Fore.WHITE}Stop container: {Fore.GREEN}docker-compose -f docker-compose.yml down{Style.RESET_ALL}")
            print(f"  {Fore.WHITE}View logs: {Fore.GREEN}docker logs {args.container_name}{Style.RESET_ALL}")
            print(f"  {Fore.WHITE}Execute in container: {Fore.GREEN}docker exec -it {args.container_name} /bin/bash{Style.RESET_ALL}")
            print(f"  {Fore.WHITE}Check status: {Fore.GREEN}docker ps | grep {args.container_name}{Style.RESET_ALL}")
        except subprocess.CalledProcessError as e:
            logger.error(f"Error running Docker Compose: {e}")
            logger.error(f"Command output (stderr): {e.stderr}")
            sys.exit(1)
    else:
        logger.info("Files generated successfully. Start with: docker-compose -f docker-compose.yml up -d")


if __name__ == '__main__':
    main()