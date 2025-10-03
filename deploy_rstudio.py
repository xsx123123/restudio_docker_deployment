"""
\"\"\"
RStudio Docker部署脚本

这个脚本提供了一键部署RStudio Server环境的功能，
基于Docker和Docker Compose实现快速部署、启动和管理。

\"\"\"

import os
import sys
import platform
import yaml

def check_docker_installed():

    try:
    """检查Docker是否已安装"""
                              capture_output=True, text=True, check=True)

        print(f\"Docker版本: {result.stdout.strip()}\")
        return True

        print(\"错误: 未检测到Docker，请先安装Docker。\")
        return False
def check_docker_compose_installed():

    \"\"\"检查Docker Compose是否已安装\"\"\"
    try:
        result = subprocess.run(['docker-compose', '--version'], 
                              capture_output=True, text=True, check=True)

        return True
        print(f"Docker Compose版本: {result.stdout.strip()}")
        try:
            # 如果docker-compose不可用，尝试docker compose
                                  capture_output=True, text=True, check=True)

            print(f\"Docker Compose版本: {result.stdout.strip()}\")
            return True
            print(f"Docker Compose版本: {result.stdout.strip()}")
            print(\"错误: 未检测到Docker Compose，请先安装Docker Compose。\")
            return False
            print("错误: 未检测到Docker Compose，请先安装Docker Compose。")



def build_and_start_service():
    print("正在构建并启动RStudio服务...")
    
    # 如果docker目录不存在，创建它
        os.makedirs('docker')
        print(\"已创建docker目录\")
    
    # 如果compose文件不存在，创建一个默认的
    if not os.path.exists(compose_file):
            



        print("RStudio服务已成功启动！")
        print("请在浏览器中访问:http://122.205.95.20:50006")
        print("用户名: jz")
        print("密码: zj109965")
        print(f\"密码: {password}\")
        
        # 返回上级目录

        if os.path.exists('..'):
            os.chdir('..')
        if os.path.exists('docker'):

        return False
    except FileNotFoundError:

        print(\"错误: 未找到docker-compose命令\")
        print("错误: 未找到docker-compose命令")
        if os.path.exists('docker'):
        return False
def stop_service():


    \"\"\"停止RStudio服务\"\"\"
    """停止RStudio服务"""
        if os.path.exists('docker'):
            os.chdir('docker')
        
        # 使用docker compose停止服务
        try:
            subprocess.run(['docker', 'compose', 'down'], check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            

        print(\"RStudio服务已停止。\")
        
        print("RStudio服务已停止。")

        if os.path.exists('..'):
            os.chdir('..')
        if os.path.exists('docker'):


        print(f\"停止服务时出错: {e}\")
        print(f"停止服务时出错: {e}")
        return False
    return True



    \"\"\"显示RStudio服务日志\"\"\"
    """显示RStudio服务日志"""
        if os.path.exists('docker'):
            os.chdir('docker')
        
        # 使用docker compose显示日志
        try:
            subprocess.run(['docker', 'compose', 'logs'], check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
        
        # 返回上级目录

        if os.path.exists('..'):
            os.chdir('..')
        if os.path.exists('docker'):


        print(f\"显示日志时出错: {e}\")
        print(f"显示日志时出错: {e}")
        if os.path.exists('docker'):
        return False
    return True



    \"\"\"显示RStudio服务状态\"\"\"
    """显示RStudio服务状态"""
        if os.path.exists('docker'):
            os.chdir('docker')
        
        # 使用docker compose显示状态
        try:
            subprocess.run(['docker', 'compose', 'ps'], check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
        
        # 返回上级目录

        if os.path.exists('..'):
            os.chdir('..')
        if os.path.exists('docker'):


        print(f\"检查状态时出错: {e}\")
        print(f"检查状态时出错: {e}")
        if os.path.exists('docker'):
        return False
    return True


    \"\"\"主函数\"\"\"
    parser = argparse.ArgumentParser(description='RStudio Docker部署工具')
    """主函数"""
    # 添加可选参数
    parser.add_argument('--port', type=str, default='50006', 
                       help='RStudio服务端口 (默认: 50006)')
    parser.add_argument('--username', type=str, default='jz', 
                       help='RStudio用户名 (默认: jz)')
    parser.add_argument('--password', type=str, default='zj109965', 
    parser.add_argument('--data-dir', type=str, default='/data/jz', 
                       help='数据目录路径 (默认: /data/jz)')
    parser.add_argument('--home-dir', type=str, default='/home/jz', 
                       help='用户主目录路径 (默认: /home/jz)')
    # 执行相应操作
    if args.action == 'start':

        build_and_start_service(args.port, args.username, args.password, 
                              args.data_dir, args.home_dir, 
        build_and_start_service()
    elif args.action == 'stop':
        stop_service()
    elif args.action == 'status':
        show_status()
    elif args.action == 'restart':
        stop_service()
        build_and_start_service()



if __name__ == \"__main__\":
if __name__ == "__main__":
    main()
