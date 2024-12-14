"""test ds messenger"""
import unittest
from ds_messenger import DirectMessenger, DirectMessage


class TestDSMessenger(unittest.TestCase):
    """tests DirectMessenger class"""
    def test_send_dm(self):
        """tests sending dm"""
        direct_messenger = DirectMessenger("168.235.86.101", "beep", "boooo")
        assert direct_messenger.send("test", "idkkkk9") is True

    def test_retrieve_new(self):
        """tests retrieving new messages"""
        beep = DirectMessenger("168.235.86.101", "beep", "boooo")
        kar54 = DirectMessenger("168.235.86.101", "kar54", "password")
        beep.send("hi", "kar54")
        lst = kar54.retrieve_new()
        msg = lst[-1].message
        assert msg == 'hi'
        assert isinstance(lst, list)
        for x in lst:
            assert isinstance(x, DirectMessage)

    def test_retrieve_all(self):
        """tests retrieving all messages"""
        beep = DirectMessenger("168.235.86.101", "beep", "boooo")
        kar54 = DirectMessenger("168.235.86.101", "kar54", "password")
        beep.send("last msg", "kar54")
        lst = kar54.retrieve_new()
        msg = lst[-1].message
        assert msg == 'last msg'
        assert isinstance(lst, list)
        for x in lst:
            assert isinstance(x, DirectMessage)

    def test_retrieve_no_connection(self):
        """tests retrieving friends and message list w no connection"""
        direct_messenger = DirectMessenger("168.235.86.101", "beep", "boooo")
        assert isinstance(direct_messenger.profile.friends, list)
        assert isinstance(direct_messenger.profile.all_messages, list)
        assert isinstance(direct_messenger.profile.new_messages, list)
        assert isinstance(direct_messenger.profile.sent_messages, list)
