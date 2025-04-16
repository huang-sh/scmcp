"""
Command-line interface for scanpy-mcp.
This module provides a CLI entry point for the scanpy-mcp package.
"""

import asyncio
import argparse
import os
import sys


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='SCMCP Server')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Add run subcommand
    run_parser = subparsers.add_parser('run', help='Start Scanpy MCP Server')
    run_parser.add_argument('--log-file', type=str, default=None, 
                        help='log file, if None use stdout')
    run_parser.add_argument('--data', type=str, default=None, help='h5ad file path')
    run_parser.add_argument('-m', "--module", type=str, default="all", 
                        choices=["io", "pp", "pl", "tl", "all", "util"],
                        help='Specify modules to load. Options: io, pp, pl, tl, util, all. Default: all')
    run_parser.add_argument('-t', "--transport", type=str, default="stdio",
                        choices=["stdio", "sse"],
                        help='Specify transport type. Options: stdio, sse. Default: stdio')
    run_parser.add_argument('-p', "--port", type=int, default=8000,
                        help='Port for SSE transport. Default: 8000')
    run_parser.add_argument('--host', type=str, default="127.0.0.1",
                        help='Host address for SSE transport. Default: 127.0.0.1')
    
    # Set default subcommand to run
    parser.set_defaults(command='run')
    
    return parser.parse_args()

def run_cli():
    """CLI entry point function"""
    args = parse_arguments()
    
    # Ensure command is 'run'
    if args.command == 'run':
        # Check for log_file attribute
        log_file = getattr(args, 'log_file', None)
        data = getattr(args, 'data', None)
        module = getattr(args, 'module', "all")
        transport = getattr(args, 'transport', "stdio")
        port = getattr(args, 'port', 8000)
        host = getattr(args, 'host', "127.0.0.1")
        
        if log_file is not None:
            os.environ['SCMCP_LOG_FILE'] = log_file
        else:
            os.environ['SCMCP_LOG_FILE'] = ""
            
        if data is not None:
            os.environ['SCMCP_DATA'] = data
        else:
            os.environ['SCMCP_DATA'] = ""

        os.environ['SCMCP_TRANSPORT'] = transport
        os.environ['SCMCP_HOST'] = host
        os.environ['SCMCP_PORT'] = str(port)
            
        # Set module environment variable
        os.environ['SCMCP_MODULE'] = module
        
        try:
            if transport == "stdio":
                from .server import run_stdio
                asyncio.run(run_stdio())
            elif transport == "sse":
                # For SSE transport, get application and run with uvicorn
                from .server import create_sse_app
                import uvicorn
                app = create_sse_app(port=port)
                uvicorn.run(app, host="0.0.0.0", port=port)
            else:
                print(f"Unsupported transport type: {transport}")
                sys.exit(1)
        except KeyboardInterrupt:
            print("\nServer stopped")
            sys.exit(0)
        except Exception as e:
            print(f"Server error: {e}")
            sys.exit(1)
    else:
        print(f"Unknown command: {args.command}")
        sys.exit(1)
