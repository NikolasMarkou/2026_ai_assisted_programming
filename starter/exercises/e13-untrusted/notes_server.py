"""Dummy server for the E13 drill. It writes one marker file and exits.

A tool that trusts this folder starts it from .mcp.json. Nothing else happens: no
network, no credentials, no file outside the folder it is started in.
"""
from pathlib import Path

Path("MCP_STARTED.txt").write_text("a project MCP server was started by the tool\n")
