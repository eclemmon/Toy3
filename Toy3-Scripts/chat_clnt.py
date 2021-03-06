#!/usr/bin/env python3

"""
This module builds a simple chat client out of the built-in Tkinter GUI package for python.
"""
##############################################################
__author__ = "Eric Lemmon"
__copyright__ = "Copyright 2020, Eric Lemmon"
__credits__ = "Eric Lemmon"
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Eric Lemmon"
__email__ = "eric.c.lemmon@stonybrook.edu"
__status__ = "Production"
##############################################################

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter


def receive():
    """
    This function handles the receiving of messages in the chat server.
    """
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            msg_list.insert(tkinter.END, msg)
        except OSError:  # Possibly client has left the chat.
            break


def send(event=None):  # event is passed by binders.
    """
    This function handles the sending of messages in the chat server.
    :param event:
    """
    msg = my_msg.get()
    my_msg.set("")  # Clears input field.
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        client_socket.close()
        top.quit()


def on_closing(event=None):
    """
    Sends a commend to close connection to client on call.
    :param event: When command to quit is called.
    """""
    my_msg.set("{quit}")
    send()


top = tkinter.Tk()
top.title("Chatter")
messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()  # For the messages to be sent.
my_msg.set("Type your messages here.")
scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.
# Following will contain the messages.
msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack(fill="both", expand=True)
messages_frame.pack(fill="both", expand=True, padx=(15, 0), pady=10)

entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="Send", command=send)
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)

# ----Now comes the sockets part----
HOST = input('Enter host: ')
PORT = input('Enter port: ')
if not PORT:
    PORT = 33000
else:
    PORT = int(PORT)

BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()  # Starts GUI execution.
