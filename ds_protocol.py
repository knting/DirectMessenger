"""ds_protocol.py"""

# Karissa Ting
# knting@uci.edu
# 38208762

import json
from collections import namedtuple

DataTuple = namedtuple('DataTuple', ['type', 'message', 'token'])
MessageTuple = namedtuple('MessageTuple', ['type', 'message', 'messages', 'token'])


def extract_json(json_msg: str) -> DataTuple:
    """converts server message"""
    try:
        json_obj = json.loads(json_msg)  # converts string into dict
        response_info = json_obj['response']
        response_type = response_info['type']
        message = response_info['message']
        token = response_info.get('token', None)
        return DataTuple(response_type, message, token)
    except json.JSONDecodeError:
        print("Json cannot be decoded.")
        return DataTuple('', '', None)


def extract_messages(json_msg: str):
    """converts JSON messages to list"""
    try:
        list_messages = []
        json_obj = json.loads(json_msg)
        response_info = json_obj['response']
        # response_type = json_obj['response']['type']
        # message = response_info.get('message', None)
        # message = response_info['message']
        messages = response_info.get('messages', None)
        # token = response_info.get('token', None)
        if messages:
            # the_message = json_obj['response']['messages'][0]['message']
            # the_from = json_obj['response']['messages'][0]['from']
            # timestamp = json_obj['response']['messages'][0]['timestamp']
            for message in messages:
                list_messages.append(message)
        return list_messages
        # return MessageTuple(response_type, message, messages, token)
    except json.JSONDecodeError:
        print("Json cannot be decoded.")
        return None
