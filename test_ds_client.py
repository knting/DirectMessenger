"""test ds message protocol"""
import unittest
from ds_client import send, join_message, req_unread, req_all


class TestClient(unittest.TestCase):
    """tests ds_client.py"""
    def test_client(self):
        """tests if function works"""
        server = "168.235.86.101"
        port = 3021
        username = "beep"
        password = "boooo"
        message = "hi beep"
        recipient = "kar54"
        x = send(server, port, username, password, message, recipient)
        assert x is True

    def test_join(self):
        """tests join message"""
        join_msg = join_message("beep", "boooo")
        assert join_msg == '{"join": {"username": "beep", "password": ' \
                           '"boooo", "token": ""}}'

    def test_unread_messages(self):
        """Tests unread message"""
        token = "caea27c8-d5f9-4db9-970b-7607a583cf91"
        unread = req_unread(token)
        expected = '{"token":"' + token + '", "directmessage": "new"}'
        assert unread == expected

    def test_all_messages(self):
        """Tests all message"""
        token = "caea27c8-d5f9-4db9-970b-7607a583cf91"
        all_m = req_all(token)
        expected = '{"token":"' + token + '", "directmessage": "all"}'
        assert all_m == expected
