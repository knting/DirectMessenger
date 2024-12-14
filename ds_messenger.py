"""ds_messenger.py"""
import pathlib
import socket
import time
from ds_protocol import extract_json, extract_messages
from Profile import Profile


class DirectMessage:
    """Direct Message class"""
    def __init__(self, recipient, message):
        self.recipient = recipient
        self.message = message
        self.timestamp = time.time()


class DirectMessenger:
    """Direct Messenger Class"""
    def __init__(self, dsuserver=None, username=None, password=None):
        self.token = None
        self.dsuserver = dsuserver
        self.username = username
        self.password = password
        self.socket_send = None
        self.socket_recv = None
        self.profile = Profile(self.dsuserver, self.username, self.password)

    def send(self, message: str, recipient: str) -> bool:
        """sends dm"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.dsuserver, 3021))
                self.socket_send = s.makefile('w')
                self.socket_recv = s.makefile('r')
                join_msg = '{"join": {"username": "' + self.username +\
                           '", "password": "' + self.password +\
                           '", "token": ""}}'
                self.socket_send.write(join_msg + '\r\n')
                self.socket_send.flush()
                resp = self.socket_recv.readline()
                tuple_server_output = extract_json(resp)
                if message != "":
                    if tuple_server_output.type == 'ok':
                        self.token = tuple_server_output.token
                        dm = ('{"token":"' + self.token +
                              '", "directmessage": {"entry": "' +
                              message + '","recipient":"' + recipient +
                              '", "timestamp": "' +
                              str(time.time()) + '"}}')
                        self.socket_send.write(dm + '\r\n')
                        self.socket_send.flush()
                        resp = self.socket_recv.readline()
                        tuple_server_output = extract_json(resp)
                        base_path = pathlib.Path.cwd()
                        path = f"{base_path}/{self.username}.dsu"
                        self.profile.load_profile(path)
                        msg_to_append = {"message": message,
                                         "recipient": recipient,
                                         "timestamp": str(time.time())}
                        self.profile.sent_messages.append(msg_to_append)
                        # print(self.profile.sent_messages)
                        if recipient not in self.profile.friends:
                            self.profile.add_friend(recipient)
                        self.profile.save_profile(path)
                        if tuple_server_output.type == 'ok':
                            print(f'Message "{message}" sent!')
                            return True
                        if tuple_server_output.type == 'error':
                            print(f'ERROR: {tuple_server_output.message}')
                            return False
                else:
                    return False
        except socket.error as se:
            print(f'Socket error: {se}')
            return False
        except AttributeError as ae:
            print(f'Attribute error: {ae}')
            return False
        # except Exception as e:
        #     print(e)
        #     return False

    def retrieve_new(self) -> list:
        """"Retrieves new unread messages"""
        try:
            s = self.connect()
            with s.makefile('w') as send, s.makefile('r') as recv:
                join_msg = self.join_message(self.username, self.password)
                send.write(join_msg + '\r\n')
                send.flush()
                resp = recv.readline()
                tuple_server_output = extract_json(resp)
                token = tuple_server_output.token
                if tuple_server_output.type == 'error':
                    print(tuple_server_output.message)
                elif token:
                    new_msg = self.req_new(token)
                    send.write(new_msg + '\r\n')
                    send.flush()
                    resp = recv.readline()
                    new_dm_output = extract_messages(resp)  # list of messages
                    # print(f'this is new: {new_dm_output}')
                list_new_message_objs = []  # storing list of dict in profile
                base_path = pathlib.Path.cwd()
                path = f"{base_path}/{self.username}.dsu"
                try:
                    self.profile.load_profile(path)
                    self.profile.new_messages = []
                    if new_dm_output is not None:
                        for new_message in new_dm_output:
                            recipient = new_message['from']
                            message = new_message["message"]
                            my_obj = DirectMessage(recipient, message)
                            list_new_message_objs.append(my_obj)
                            self.profile.new_messages.append(new_message)
                            # sender = new_message.get('from')
                            # if sender not in self.profile.friends:
                            #     self.profile.add_friend(sender)
                        self.profile.save_profile(path)
                except FileNotFoundError:
                    self.profile.create_profile(path)
                s.close()
                return list_new_message_objs  # list of direct message objs
                # return new_dm_output
        except OSError as oe:
            print(f'OS Error: {oe}')
        except AttributeError:
            print('Attribute Error')
        except UnboundLocalError:
            print(f'Unbound Local Error: {tuple_server_output.message}')
        # except Exception as e:
        #     print(e)

    def retrieve_all(self) -> list:
        """"Retrieves all messages"""
        # must return a list of DirectMessage objects containing all messages
        try:
            s = self.connect()
            with s.makefile('w') as send, s.makefile('r') as recv:
                join_msg = self.join_message(self.username, self.password)
                send.write(join_msg + '\r\n')
                send.flush()
                resp = recv.readline()
                tuple_server_output = extract_json(resp)
                token = tuple_server_output.token
                if token is not None:
                    all_msg = self.req_all(token)
                    send.write(all_msg + '\r\n')
                    send.flush()
                    resp = recv.readline()
                    all_dm_output = extract_messages(resp)
                list_all_message_objs = []
                base_path = pathlib.Path.cwd()
                path = f"{base_path}/{self.username}.dsu"
                try:
                    self.profile.load_profile(path)
                    for dm in all_dm_output:
                        recipient = dm['from']
                        message = dm["message"]
                        my_obj = DirectMessage(recipient, message)
                        list_all_message_objs.append(my_obj)
                        # self.profile.all_messages.append(my_obj)
                        if dm not in self.profile.all_messages:
                            self.profile.all_messages.append(dm)
                        if recipient not in self.profile.friends:
                            self.profile.add_friend(recipient)
                    self.profile.save_profile(path)
                except FileNotFoundError:
                    self.profile.create_profile(path)
                s.close()
                # print(all_dm_output)
                # return all_dm_output
                # print(list_all_messages)
                return list_all_message_objs
        except OSError as oe:
            print(f'OS Error: {oe}')
        except UnboundLocalError:
            print(f'Unbound Local Error: {tuple_server_output.message}')
        # except Exception as e:
        #     print(e)

    def connect(self):
        """connects to server"""
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.dsuserver, 3021))
        return s

    @staticmethod
    def join_message(username, password):
        """join message"""
        join_msg = '{"join": {"username": "' + username +\
                   '", "password": "' + password + '", "token": ""}}'
        return join_msg

    @staticmethod
    def direct_message(user_token, message, recipient):
        """direct message"""
        dm = '{"token":"' + user_token + '", "directmessage": {"entry": "' +\
             message + '","recipient":"' + recipient + '", "timestamp": "' +\
             str(time.time()) + '"}}'
        return dm

    @staticmethod
    def req_new(user_token):
        """req new messages"""
        req_new = '{"token":"' + user_token + '", "directmessage": "new"}'
        return req_new

    @staticmethod
    def req_all(user_token):
        """req all messages"""
        req_all = '{"token":"' + user_token + '", "directmessage": "all"}'
        return req_all

    def publish(self, message: str):
        """publishes to server"""
        try:
            s = self.connect()
            with s.makefile('w') as send, s.makefile('r') as recv:
                join_msg = self.join_message(self.username, self.password)
                send.write(join_msg + '\r\n')
                send.flush()
                resp = recv.readline()
                tuple_server_output = extract_json(resp)
                if message != "":
                    if tuple_server_output.type == 'ok':
                        user_token = tuple_server_output.token
                        post = '{"token":"' + user_token + '", "post": ' +\
                               '{"entry": "' + message + '", "timestamp": "' +\
                               str(time.time()) + '"}}'
                        send.write(post + '\r\n')
                        send.flush()
                    elif tuple_server_output.type == 'error':
                        output_msg = tuple_server_output.message
                        print(f'Error sending to server. {output_msg}')
                else:
                    print('Message can not be blank.')
        except socket.error:
            print(f'Socket error: {socket.error}')
        except TypeError:
            print('JSON object must be str or bites. Check parameter types.')
        except NameError:
            print('Please check parameter values/types and try again.')


# direct_message = DirectMessenger(dsuserver="168.235.86.101",
# username="beep", password="boooo")
# direct_message = DirectMessenger(dsuserver="168.235.86.101",
#                  username="kar54", password="password")

# knt8, pass
# direct_message.send("p", "idkkkk9")

# all = direct_message.retrieve_all()
# for x in all:
#     print(f'{x.recipient} : {x.message}')
