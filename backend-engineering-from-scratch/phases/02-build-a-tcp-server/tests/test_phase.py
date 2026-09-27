"""
Integration test for Lesson 02: Build a TCP Server.
Connects a real TCP client socket to the server and verifies echo response.
"""

import socket
import pytest
import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
CODE_FILE = os.path.join(os.path.dirname(CURRENT_DIR), "code", "main.py")
mod_name = os.path.basename(os.path.dirname(CURRENT_DIR)).replace("-", "_")

import importlib.util
spec = importlib.util.spec_from_file_location(mod_name, CODE_FILE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
globals().update({k: getattr(mod, k) for k in dir(mod) if not k.startswith("__")})

def test_tcp_server_echo():
    server = SimpleTCPServer()
    port = server.start()
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(("127.0.0.1", port))
        
        client.sendall(b"Hello World")
        data = client.recv(1024)
        assert data == b"ECHO:Hello World"
        
        client.close()
    finally:
        server.stop()

def test_tcp_server_eof_on_close():
    server = SimpleTCPServer()
    port = server.start()
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(("127.0.0.1", port))
        client.close()  # Immediately sends FIN packet
    finally:
        server.stop()
