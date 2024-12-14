"""ds_client.py"""

# Karissa Ting
# knting@uci.edu
# 38208762

import socket
import time
from ds_protocol import extract_json, extract_messages


def send(server: str, port: int, username: str, password: str, message: str, recipient: str):
    """sends a message"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((server, port))
            # s = connect(server, port)
            send = s.makefile('w')
            recv = s.makefile('r')
            join_msg = join_message(username, password)
            send.write(join_msg + '\r\n')
            send.flush()
            resp = recv.readline()
            tuple_server_output = extract_json(resp)
            if message != "":
                if tuple_server_output.type == 'ok':
                    # checks if joining to server is okay
                    user_token = tuple_server_output.token
                    dm = direct_message(user_token, message, recipient)
                    send.write(dm + '\r\n')
                    send.flush()
                    resp = recv.readline()
                    tuple_server_output = extract_json(resp)
                    if tuple_server_output.type == 'ok':
                        print(f'Message "{message}" sent!')

                        unread_messages = req_unread(user_token)
                        send.write(unread_messages + '\r\n')
                        send.flush()
                        resp = recv.readline()
                        new_dm_output = extract_messages(resp)
                        print(f'NEW DMS: {new_dm_output}')

                        all_messages = req_all(user_token)
                        send.write(all_messages + '\r\n')
                        send.flush()
                        resp = recv.readline()
                        all_dm_output = extract_messages(resp)
                        print(f'ALL DMS: {all_dm_output}')
                        return True
                    elif tuple_server_output.type == 'error':
                        print(f'ERROR: {tuple_server_output.message}')
                        return False
                elif tuple_server_output.type == 'error':
                    print(f'TError sending to the server. {tuple_server_output.message}')
                    return False
                else:
                    print('ERROR')
                    return False
            else:
                print('Message must not be empty or just whitespace.')
                return False
    except socket.error:
        print(f'Socket error: {socket.error}')
        return False
    except TypeError:
        print('JSON object must be str or bites. Check the parameter types.')
        return False
    except NameError:
        print('Please check parameter values/types and try again.')
        return False
    except Exception as e:
        print(e)
        return False


def connect(server, port: int):
    """connects to server"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((server, port))
    return s


def join_message(username, password):
    """joins server"""
    join_msg = '{"join": {"username": "' + username +\
               '", "password": "' + password + '", "token": ""}}'
    return join_msg


def direct_message(user_token, message, recipient):
    """sends a dm"""
    dm = '{"token":"' + user_token + '", "directmessage": {"entry": "' + message\
        + '","recipient":"' + recipient + '", "timestamp": "' + str(time.time()) + '"}}'
    return dm


def req_unread(user_token):
    """requests unread messages"""
    unread_msgs = '{"token":"' + user_token + '", "directmessage": "new"}'
    return unread_msgs


def req_all(user_token):
    """requests all messages"""
    all_msgs = '{"token":"' + user_token + '", "directmessage": "all"}'
    return all_msgs


# server = "168.235.86.101"
# port = 3021
# username = "beep"
# password = "boooo"
# message = "hi!!!!"
# recipient = "idkkkk9"
# send(server, port, username, password, message, recipient)
