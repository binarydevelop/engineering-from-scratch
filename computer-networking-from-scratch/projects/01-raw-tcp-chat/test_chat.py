#!/usr/bin/env python3
"""
projects/01-raw-tcp-chat/test_chat.py
Automated test suite verifying the multi-user TCP chat server.
"""

import socket
import threading
import time
import os
import sys
import unittest
sys.path.insert(0, os.path.dirname(__file__))
from chat_server import ChatServer


class TestChatServer(unittest.TestCase):
    def setUp(self):
        self.server = ChatServer(host="127.0.0.1", port=9099)
        self.server_thread = threading.Thread(target=self.server.run, daemon=True)
        self.server_thread.start()
        time.sleep(0.1)

    def tearDown(self):
        self.server.close()
        time.sleep(0.05)

    def test_multiclient_chat_broadcast(self):
        # Client 1 connects
        c1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        c1.connect(("127.0.0.1", 9099))
        welcome1 = c1.recv(1024).decode()
        self.assertIn("Welcome to the Chat", welcome1)

        # Client 2 connects
        c2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        c2.connect(("127.0.0.1", 9099))
        welcome2 = c2.recv(1024).decode()
        self.assertIn("Welcome to the Chat", welcome2)

        # Drain join notifications
        time.sleep(0.1)
        c1.setblocking(False)
        try:
            c1.recv(1024)
        except BlockingIOError:
            pass

        # Client 1 sends a message
        test_message = "Hello from Client 1!\n"
        c1.sendall(test_message.encode())
        time.sleep(0.1)

        # Client 2 should receive the broadcast
        c2.settimeout(1.0)
        received_at_c2 = c2.recv(1024).decode()
        self.assertIn("Hello from Client 1!", received_at_c2)

        c1.close()
        c2.close()


if __name__ == "__main__":
    unittest.main()
