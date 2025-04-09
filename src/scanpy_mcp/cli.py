"""
Command-line interface for scanpy-mcp.
This module provides a CLI entry point for the scanpy-mcp package.
"""

import asyncio
import argparse
import os
import sys


def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='Scanpy MCP 服务器')
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # 添加 run 子命令
    run_parser = subparsers.add_parser('run', help='启动 Scanpy MCP 服务器')
    run_parser.add_argument('--log-file', type=str, default=None, 
                        help='log file, if None use stdout')
    run_parser.add_argument('--data', type=str, default=None, help='h5ad file path')
    run_parser.add_argument('-m', "--module", type=str, default="all", 
                        choices=["io", "pp", "pl", "tl", "all", "util"],
                        help='Specify modules to load. Options: io, pp, pl, tl, util, all. Default: all')
    
    # 设置默认子命令为 run
    parser.set_defaults(command='run')
    
    return parser.parse_args()

def run_cli():
    """CLI 入口点函数"""
    args = parse_arguments()
    
    # 确保命令是 'run'
    if args.command == 'run':
        # 检查是否有 log_file 属性
        log_file = getattr(args, 'log_file', None)
        data = getattr(args, 'data', None)
        module = getattr(args, 'module', "all")
        
        if log_file is not None:
            os.environ['SCANPY_MCP_LOG_FILE'] = log_file
        else:
            os.environ['SCANPY_MCP_LOG_FILE'] = ""
            
        if data is not None:
            os.environ['SCANPY_MCP_DATA'] = data
        else:
            os.environ['SCANPY_MCP_DATA'] = ""
            
        # 设置要加载的模块环境变量
        os.environ['SCANPY_MCP_MODULE'] = module
        
        try:
            from .server import run
            asyncio.run(run())
        except KeyboardInterrupt:
            print("\n服务器已停止")
            sys.exit(0)
        except Exception as e:
            print(f"服务器运行出错: {e}")
            sys.exit(1)
    else:
        print(f"未知命令: {args.command}")
        sys.exit(1)

# 这是 pyproject.toml 中定义的入口点
def run():
    """入口点函数，由 scmcp 命令调用"""
    run_cli()

if __name__ == "__main__":
    run_cli()