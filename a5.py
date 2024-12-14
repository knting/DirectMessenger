"""a5.py"""

import tkinter as tk
from tkinter import ttk, simpledialog
import pathlib
import ttkthemes
from ds_messenger import DirectMessenger


class Body(tk.Frame):
    """Initializes the Body instance."""
    def __init__(self, root, recipient_selected_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._contacts = [str]
        self._select_callback = recipient_selected_callback
        # After all initialization is complete,
        # call the _draw method to pack the widgets
        # into the Body instance
        self._draw()

    def node_select(self, event):
        """Handle the selection of a node (contact) in the Treeview."""
        index = int(self.posts_tree.selection()[0])
        entry = self._contacts[index]
        if self._select_callback is not None:
            self._select_callback(entry)

    def insert_contact(self, contact: str):
        """Insert a contact into the contact list."""
        self._contacts.append(contact)
        the_id = len(self._contacts) - 1
        self._insert_contact_tree(the_id, contact)

    def _insert_contact_tree(self, the_id, contact: str):
        """Insert a contact into the Treeview widget."""
        if len(contact) > 25:
            entry = contact[:24] + "..."
        the_id = self.posts_tree.insert('', the_id, the_id, text=contact)

    def insert_user_message(self, message: str):
        """insert user message"""
        self.entry_editor.insert(tk.END, message + '\n', 'entry-right')

    def insert_contact_message(self, message: str):
        """inserts message from friend on left"""
        self.entry_editor.insert(tk.END, message + '\n', 'entry-left')

    def get_text_entry(self) -> str:
        """gets message ur sending in text box"""
        return self.message_editor.get('1.0', 'end').rstrip()

    def set_text_entry(self, text: str):
        """when sending a message after u send, sets back to blank"""
        self.message_editor.delete(1.0, tk.END)
        self.message_editor.insert(1.0, text)

    def _draw(self):
        """draws body instance"""
        posts_frame = tk.Frame(master=self, width=250, bg="pink")
        posts_frame.pack(fill=tk.BOTH, side=tk.LEFT)

        self.posts_tree = ttk.Treeview(posts_frame)
        self.posts_tree.bind("<<TreeviewSelect>>", self.node_select)
        self.posts_tree.pack(fill=tk.BOTH, side=tk.TOP,
                             expand=True, padx=5, pady=5)

        entry_frame = tk.Frame(master=self, bg="")
        entry_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

        editor_frame = tk.Frame(master=entry_frame, bg="red")
        editor_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        scroll_frame = tk.Frame(master=entry_frame, bg="blue", width=10)
        scroll_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)

        message_frame = tk.Frame(master=self, bg="yellow")
        message_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=False)

        self.message_editor = tk.Text(message_frame, width=0, height=5)
        self.message_editor.pack(fill=tk.BOTH, side=tk.LEFT,
                                 expand=True, padx=0, pady=0)

        self.entry_editor = tk.Text(editor_frame, width=0, height=5)
        self.entry_editor.tag_configure('entry-right', justify='right',
                                        foreground='#B1ABEC', font=20)  # 7BF7EA
        self.entry_editor.tag_configure('entry-left', justify='left',
                                        foreground='#B5FFC9', font=20)
        self.entry_editor.pack(fill=tk.BOTH, side=tk.LEFT,
                               expand=True, padx=0, pady=0)

        entry_editor_scrollbar = tk.Scrollbar(master=scroll_frame,
                                              command=self.entry_editor.yview)
        self.entry_editor['yscrollcommand'] = entry_editor_scrollbar.set
        entry_editor_scrollbar.pack(fill=tk.Y, side=tk.LEFT,
                                    expand=False, padx=0, pady=0)

    def clear_editor(self):
        """clears message editor"""
        self.entry_editor.delete('1.0', tk.END)


class Footer(tk.Frame):
    """initializes footer instance"""
    def __init__(self, root, send_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._send_callback = send_callback
        self._draw()

    def send_click(self):
        """Handle the click event of the send button."""
        if self._send_callback is not None:
            self._send_callback()

    def _draw(self):
        """draws footer instance"""
        save_button = tk.Button(master=self, text="Send", width=15,
                                command=self.send_click)
        # You must implement this.
        # Here you must configure the button to bind its click to
        # the send_click() function.
        save_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=15, pady=15)

        # self.footer_label = tk.Label(master=self, text="Ready.")
        # self.footer_label.pack(fill=tk.BOTH, side=tk.LEFT, padx=5)


class NewContactDialog(tk.simpledialog.Dialog):
    """Initialize the NewContactDialog instance."""
    def __init__(self, root, title=None, user=None, pwd=None, server=None):
        self.root = root
        self.server = server
        self.user = user
        self.pwd = pwd
        super().__init__(root, title)

    def body(self, frame):
        """creates body of dialog window"""
        self.server_label = tk.Label(frame, width=30, text="DS Server Address")
        self.server_label.pack()
        self.server_entry = tk.Entry(frame, width=30)
        # self.server_entry.insert(tk.END, self.server)
        self.server_entry.pack()

        self.username_label = tk.Label(frame, width=30, text="Username")
        self.username_label.pack()
        self.username_entry = tk.Entry(frame, width=30)
        # self.username_entry.insert(tk.END, self.user)
        self.username_entry.pack()

        self.password_label = tk.Label(frame, width=30, text="Password")
        self.password_label.pack()
        self.password_entry = tk.Entry(frame, width=30)
        # self.password_entry.insert(tk.END, self.pwd)
        self.password_entry.pack()
        self.password_entry['show'] = '*'
        try:
            if self.server:
                self.server_entry.insert(tk.END, self.server)
            if self.user:
                self.username_entry.insert(tk.END, self.user)
            if self.pwd:
                self.password_entry.insert(tk.END, self.pwd)
        except AttributeError as ae:
            print(ae)

    def apply(self):
        self.user = self.username_entry.get()
        self.pwd = self.password_entry.get()
        self.server = self.server_entry.get()


class MainApp(tk.Frame):
    """initialize MainApp"""
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root
        self.username = None
        self.password = None
        self.server = None
        self.recipient = None
        # self.body = Body(self.root, self.recipient_selected)

        # You must implement this! You must configure and
        # instantiate your DirectMessenger instance after this line.
        self.base_path = pathlib.Path.cwd()
        self.configure_server()
        self.direct_messenger = DirectMessenger(dsuserver=self.server,
                                                username=self.username,
                                                password=self.password)

        self.path = f"{self.base_path}/{self.username}.dsu"
        self.direct_messenger.profile.load_profile(self.path)

        # After all initialization is complete,
        # call the _draw method to pack the widgets
        # into the root frame
        self._draw()
        # self.direct_messenger.retrieve_all()
        for contact in self.direct_messenger.profile.friends:
            self.body.insert_contact(contact)

    def send_message(self):
        """sends message in text box"""
        message = self.body.get_text_entry()
        # Check if recipient is selected
        # self.recipient_selected(self.recipient)

        if self.recipient is not None:
            self.direct_messenger.send(message, self.recipient)
            self.direct_messenger.profile.save_profile(self.path)
            # Clear the message entry after sending
            self.body.set_text_entry("")
            self.body.insert_user_message(message)
        else:
            # Notify the user to select a recipient
            print("Please select a recipient before sending.")

    def add_contact(self):
        """adds new contact"""
        # Hint: check how to use tk.simpledialog.askstring to retrieve
        # the name of the new contact, and then use one of the body
        # methods to add the contact to your contact list
        new_contact = tk.simpledialog.askstring("Add Contact",
                                                "Enter the name of the new contact:")
        if new_contact:
            # Add the contact to the contact list in the Body widget
            self.body.insert_contact(new_contact)

    def recipient_selected(self, recipient):
        """when you click on a recipient"""
        self.recipient = recipient
        print(f'this is recipient in recipient selected: {self.recipient}')
        # self.body.delete('1.0', tk.END)
        self.body.clear_editor()
        self.direct_messenger.retrieve_all()
        all_messages = self.direct_messenger.profile.all_messages
        sent_messages = self.direct_messenger.profile.sent_messages
        # for message in all_messages:  # [::-1}
        #     if message['from'] == recipient:
        #         self.body.insert_contact_message(message['message'])
        # for message in sent_messages:
        #     if message['recipient'] == recipient:
        #         self.body.insert_user_message(message['message'])

        all_and_sent = all_messages + sent_messages
        all_messages_sorted = sorted(all_and_sent, key=lambda x: x['timestamp'])
        # all_messages_sorted.reverse()
        for message in all_messages_sorted:
            if 'from' in message and message['from'] == recipient:
                self.body.insert_contact_message(message['message'])
            elif 'recipient' in message and message['recipient'] == recipient:
                self.body.insert_user_message(message['message'])

    def configure_server(self):
        """configure server"""
        ud = NewContactDialog(self.root, "Configure Account",
                              self.username, self.password, self.server)
        self.username = ud.user
        self.password = ud.pwd
        self.server = ud.server
        # You must configure and instantiate your
        # DirectMessenger instance after this line.
        if self.server and self.username and self.password:
            self.direct_messenger = DirectMessenger(dsuserver=self.server,
                                                    username=self.username,
                                                    password=self.password)
        new_path = f'{self.base_path}/{self.username}.dsu'
        self.direct_messenger.profile.load_profile(new_path)
        print(new_path)

    def other_configure_server(self):
        """configure server after initial one"""
        ud = NewContactDialog(self.root, "Configure Account",
                              self.username, self.password, self.server)
        self.username = ud.user
        self.password = ud.pwd
        self.server = ud.server

        self.body.clear_editor()
        self.body.message_editor.delete('1.0', tk.END)

        # need to remove previous contacts
        # the messages are not in order for the next user
        print(self.username)
        if self.server and self.username and self.password:
            self.direct_messenger = DirectMessenger(dsuserver=self.server,
                                                    username=self.username,
                                                    password=self.password)
        new_path = f"{self.base_path}/{self.username}.dsu"
        self.direct_messenger.profile.load_profile(new_path)
        print(new_path)
        # self.reset_application()

        # when u configure server again, needs to reboot whole thing to show other friends/messages

        self.recipient_selected(self.recipient)
        all_messages = self.direct_messenger.profile.all_messages
        sent_messages = self.direct_messenger.profile.sent_messages
        print(f'friends: {self.direct_messenger.profile.friends}')
        print(f'all: {all_messages}')
        print(f'sent: {sent_messages}')

        if self.body:
            self.body.destroy()
        # Reinitialize the body
        self.body = Body(self.root, recipient_selected_callback=self.recipient_selected)
        self.body.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        self.direct_messenger.retrieve_all()
        for contact in self.direct_messenger.profile.friends:
            self.body.insert_contact(contact)

    def publish(self, message: str):
        """publishes to the server"""
        # You must implement this!
        self.direct_messenger.publish(message)

    def check_new(self):
        """checks if new message"""
        new_messages = self.direct_messenger.retrieve_new()
        print(f'new: {self.direct_messenger.profile.new_messages}')
        print(self.direct_messenger.profile.friends)
        if new_messages is not None:
            for new in new_messages:
                the_message = new.message
                recipient = new.recipient
                if recipient not in self.direct_messenger.profile.friends:
                    self.body.insert_contact(recipient)
                    self.direct_messenger.profile.add_friend(recipient)
                if recipient == self.recipient:
                    self.body.insert_contact_message(the_message)
                # if new friend, adds contact on the side if they send message
            self.root.after(1000, self.check_new)

    def _draw(self):
        # Build a menu and add it to the root frame.
        menu_bar = tk.Menu(self.root)
        self.root['menu'] = menu_bar
        # menu_file = tk.Menu(menu_bar)
        #
        # menu_bar.add_cascade(menu=menu_file, label='File')
        # menu_file.add_command(label='New')
        # menu_file.add_command(label='Open...')
        # menu_file.add_command(label='Close')

        settings_file = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=settings_file, label='Settings')
        settings_file.add_command(label='Add Contact',
                                  command=self.add_contact)
        # settings_file.add_command(label='Configure DS Server',
        #                           command=self.other_configure_server)

        # configure_server_button = tk.Button(self.root, text="Configure Server", fg="#7E1976",
        # command=self.configure_server)
        # configure_server_button.pack(side=tk.BOTTOM, padx=5, pady=5, anchor=tk.SW)

        # added an add contact and configure server button
        # add_contact_button = tk.Button(self.root, text="Add Contact", command=self.add_contact)
        # add_contact_button.pack(side=tk.BOTTOM, anchor=tk.W, padx=10, pady=10)
        # add_contact_button.pack(fill=tk.BOTH, side=tk.LEFT, padx=5)
        # save_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)

        # The Body and Footer classes must be initialized and
        # packed into the root window.

        self.body = Body(self.root,
                         recipient_selected_callback=self.recipient_selected)
        self.body.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        self.footer = Footer(self.root, send_callback=self.send_message)
        self.footer.pack(fill=tk.BOTH, side=tk.BOTTOM)


if __name__ == "__main__":
    # All Tkinter programs start with a root window. We will name ours 'main'.
    # main = tk.Tk()

    main = ttkthemes.ThemedTk()

    # Set the theme
    # main.set_theme("kroc")
    main.set_theme("equilux")
    # main.tk_setPalette(background='#2F302F', foreground='white')

    # 'title' assigns a text value to the Title Bar area of a window.
    main.title("ICS 32 Distributed Social Messenger")

    # This is just an arbitrary starting point. You can change the value
    # around to see how the starting size of the window changes.
    main.geometry("720x480")

    # adding this option removes some legacy behavior with menus that
    # some modern OSes don't support. If you're curious, feel free to comment
    # out and see how the menu changes.
    main.option_add('*tearOff', False)

    # Initialize the MainApp class, which is the starting point for the
    # widgets used in the program. All the classes that we use,
    # subclass Tk.Frame, since our root frame is main, we initialize
    # the class with it.
    app = MainApp(main)

    # When update is called, we finalize the states of all widgets that
    # have been configured within the root frame. Here, update ensures that
    # we get an accurate width and height reading based on the types of widgets
    # we have used. minsize prevents the root window from resizing too small.
    # Feel free to comment it out and see how the resizing
    # behavior of the window changes.
    main.update()
    main.minsize(main.winfo_width(), main.winfo_height())
    _id = main.after(2000, app.check_new)
    print(_id)
    # And finally, start up the event loop for the program (you can find
    # more on this in lectures of week 9 and 10).
    main.mainloop()
