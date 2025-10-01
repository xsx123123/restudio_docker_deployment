#!/usr/bin/env python3
"""
RStudio Docker部署脚本

这个脚本提供了一键部署RStudio Server环境的功能，
基于Docker和Docker Compose实现快速部署、启动和管理。
"""

import os
import sys
import subprocess
import argparse
import platform

def check_docker_installed():
    """检查Docker是否已安装"""
    try:
        result = subprocess.run(['docker', '--version'], 
                              capture_output=True, text=True, check=True)
        print(f"Docker版本: {result.stdout.strip()}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("错误: 未检测到Docker，请先安装Docker。")
        return False

def check_docker_compose_installed():
    """检查Docker Compose是否已安装"""
    try:
        # 首先尝试 docker-compose 命令
        result = subprocess.run(['docker-compose', '--version'], 
                              capture_output=True, text=True, check=True)
        print(f"Docker Compose版本: {result.stdout.strip()}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        try:
            # 如果docker-compose不可用，尝试docker compose
            result = subprocess.run(['docker', 'compose', 'version'], 
                                  capture_output=True, text=True, check=True)
            print(f"Docker Compose版本: {result.stdout.strip()}")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("错误: 未检测到Docker Compose，请先安装Docker Compose。")
            return False

def build_and_start_service():
    """构建并启动RStudio服务"""
    print("正在构建并启动RStudio服务...")
    try:
        # 切换到docker目录
        os.chdir('docker')
        
        # 使用docker compose构建并启动服务
        subprocess.run(['docker', 'compose', 'up', '-d', '--build'], check=True)
        print("RStudio服务已成功启动！")
        print("请在浏览器中访问: http://localhost:50006")
        print("用户名: jz")
        print("密码: zj109965")
        
        # 返回上级目录
        os.chdir('..')
    except subprocess.CalledProcessError as e:
        print(f"启动服务时出错: {e}")
        os.chdir('..')
        return False
    except FileNotFoundError:
        print("错误: 未找到docker-compose命令")
        os.chdir('..')
        return False
    return True

def stop_service():
    """停止RStudio服务"""
    print("正在停止RStudio服务...")
    try:
        # 切换到docker目录
        os.chdir('docker')
        
        # 使用docker compose停止服务
        subprocess.run(['docker', 'compose', 'down'], check=True)
        print("RStudio服务已停止。")
        
        # 返回上级目录
        os.chdir('..')
    except subprocess.CalledProcessError as e:
        print(f"停止服务时出错: {e}")
        os.chdir('..')
        return False
    return True

def show_logs():
    """显示RStudio服务日志"""
    print("正在显示RStudio服务日志...")
    try:
        # 切换到docker目录
        os.chdir('docker')
        
        # 使用docker compose显示日志
        subprocess.run(['docker', 'compose', 'logs'], check=True)
        
        # 返回上级目录
        os.chdir('..')
    except subprocess.CalledProcessError as e:
        print(f"显示日志时出错: {e}")
        os.chdir('..')
        return False
    return True

def show_status():
    """显示RStudio服务状态"""
    print("正在检查RStudio服务状态...")
    try:
        # 切换到docker目录
        os.chdir('docker')
        
        # 使用docker compose显示状态
        subprocess.run(['docker', 'compose', 'ps'], check=True)
        
        # 返回上级目录
        os.chdir('..')
    except subprocess.CalledProcessError as e:
        print(f"检查状态时出错: {e}")
        os.chdir('..')
        return False
    return True

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='RStudio Docker部署工具')
    parser.add_argument('action', choices=['start', 'stop', 'logs', 'status', 'restart'], 
                       help='要执行的操作: start(启动), stop(停止), logs(查看日志), status(查看状态), restart(重启)')
    
    args = parser.parse_args()
    
    # 检查系统要求
    if not check_docker_installed() or not check_docker_compose_installed():
        sys.exit(1)
    
    print(f"当前操作系统: {platform.system()}")
    print(f"当前工作目录: {os.getcwd()}")
    
    # 执行相应操作
    if args.action == 'start':
        build_and_start_service()
    elif args.action == 'stop':
        stop_service()
    elif args.action == 'logs':
        show_logs()
    elif args.action == 'status':
        show_status()
    elif args.action == 'restart':
        stop_service()
        build_and_start_service()

if __name__ == "__main__":
    main()