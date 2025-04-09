"""
Main entry point for scanpy-mcp package.
This allows running the server directly with 'python -m scanpy_mcp'
"""

import asyncio
from .server import run

if __name__ == "__main__":
    print("Starting scanpy-mcp server...")
    asyncio.run(run())