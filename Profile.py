"""Profile.py"""

import json
import time
from pathlib import Path


class DsuFileError(Exception):
    """
DsuFileError is custom exception handler that you should catch in your own
code. Raised when trying to load/save Profile objects to file the system.
    """


class DsuProfileError(Exception):
    """
DsuProfileError is custom exception handler that you catch in your own code
Raised when attempting to deserialize a dsu file to a Profile object.
    """


class Post(dict):
    """

    Post class responsible for working w individual user posts. It supports
    2 features: timestamp property that is set upon instantiation and
    when entry object set & an entry property that stores the post message.

    """
    def __init__(self, entry: str = None, timestamp: float = 0):
        self._timestamp = timestamp
        self.set_entry(entry)

        # Subclass dict to expose Post properties for serialization
        # Don't worry about this!
        dict.__init__(self, entry=self._entry, timestamp=self._timestamp)

    def set_entry(self, entry):
        """sets entry"""
        self._entry = entry
        dict.__setitem__(self, 'entry', entry)

        # If timestamp has not been set, generate a new from time module
        if self._timestamp == 0:
            self._timestamp = time.time()

    def get_entry(self):
        """gets entry"""
        return self._entry

    def set_time(self, time: float):
        """sets time"""
        self._timestamp = time
        dict.__setitem__(self, 'timestamp', time)

    def get_time(self):
        """gets time"""
        return self._timestamp

    """
    The property method is used to support get and set capability for entry and
    time values. When value for entry is changed or set, timestamp field is
    updated to the current time.
    """
    entry = property(get_entry, set_entry)
    timestamp = property(get_time, set_time)


class Profile:
    """
    Profile class exposes properties required to join ICS 32 DSU server. You
    need to use this class to manage the info provided by each new user
    created within your program for a2. Pay attention to the properties and
    functions in this class as you need to use each of them in your program.

    When creating program you need to collect user input for the properties
    exposed by this class. A Profile class should ensure a username & password
    are set, but contains no conventions to do. Make sure that your code
    verifies that required properties are set.

    """

    def __init__(self, dsuserver=None, username=None, password=None):
        self.dsuserver = dsuserver  # REQUIRED
        self.username = username  # REQUIRED
        self.password = password  # REQUIRED
        self.bio = ''            # OPTIONAL
        self._posts = []         # OPTIONAL
        self.all_messages = []  # added this
        self.new_messages = []
        self.sent_messages = []
        self.friends = []  # i added this

    def add_post(self, post: Post) -> None:
        """
    add_post accepts a Post object as parameter and appends it to posts list.
    Posts are stored in a list object in the order they are added. If multiple
    Posts objects are created, but added to the Profile in a different order,
    it's possible for list to not be sorted by Post.timestamp property.
    So take caution as to how you implement your add_post code.
        """
        self._posts.append(post)

    def del_post(self, index: int) -> bool:
        """
    del_post removes a Post at a given index and returns True if successful
    and False if an invalid index was supplied.

    To determine which post to delete you must implement your own search
    operation on the posts returned from the get_posts function to find
    correct index.
        """
        try:
            del self._posts[index]
            return True
        except IndexError:
            return False

    def get_posts(self) -> list[Post]:
        """
    get_posts returns list object containing all posts added to
    the Profile object
        """
        return self._posts

    def save_profile(self, path: str) -> None:
        """
    save_profile accepts an existing dsu file to save the current instance
    of Profile to the file system.
        """
        p = Path(path)

        if p.exists() and p.suffix == '.dsu':
            try:
                with open(p, 'w', encoding="utf-8") as f:
                    json.dump(self.__dict__, f)
            except Exception as ex:
                raise DsuFileError("Error attempting to process DSU file.", ex)
        else:
            raise DsuFileError("Invalid DSU file path or type")

    def load_profile(self, path: str) -> None:
        """
    load_profile will populate the current instance of Profile with data
    stored in a DSU file.
    Raises DsuProfileError, DsuFileError
        """
        p = Path(path)
        if p.exists() and p.suffix == '.dsu':
            try:
                f = open(p, 'r', encoding="utf-8")
                obj = json.load(f)
                self.username = obj['username']
                self.password = obj['password']
                self.dsuserver = obj['dsuserver']
                self.bio = obj.get('bio', "")
                self.friends = obj.get('friends', [])
                self.all_messages = obj.get('all_messages', [])
                self.new_messages = obj.get('new_messages', [])
                self.sent_messages = obj.get('sent_messages', [])
                for post_obj in obj['_posts']:
                    post = Post(post_obj['entry'], post_obj['timestamp'])
                    self._posts.append(post)
                f.close()
            except FileNotFoundError:
                self.create_profile(path)
            except Exception as ex:
                self.create_profile(path)
                # raise DsuProfileError(ex)
        else:
            self.create_profile(path)
            # raise DsuFileError()

    def add_message(self, message):
        """adds messages to profile list"""
        self.all_messages.append(message)

    def add_friend(self, friend_username):
        """add friends to profile"""
        self.friends.append(friend_username)

    def create_profile(self, path):
        """creates profile for dsu file"""
        default_profile = {"dsuserver": self.dsuserver,
                           "username": self.username,
                           "password": self.password,
                           "bio": self.bio,
                           "_posts": self._posts,
                           "all_messages": self.all_messages,
                           "new_messages": self.new_messages,
                           "sent_messages": self.sent_messages,
                           "friends": self.friends}
        with open(path, "w", encoding="utf-8") as f:
            json.dump(default_profile, f, indent=4)
