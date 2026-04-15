"""
Clawra MCP Server Module

Usage:
    python -m clawra.mcp.server

Claude Code MCP Configuration:
    在 .claude/mcp.json 中添加:
    {
        "mcpServers": {
            "clawra": {
                "command": "python",
                "args": ["-m", "clawra.mcp.server"],
                "cwd": "/path/to/clawra-engine"
            }
        }
    }
"""

from .server import ClawraMCPServer, main

__all__ = ["ClawraMCPServer", "main"]
