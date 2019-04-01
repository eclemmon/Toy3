#!/usr/bin/env python3

"""Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM, gethostbyname, getfqdn
from threading import Thread
from multiprocessing import Process, Pool
from Music_Handler3 import *
import pyo
import time


def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("Welcome to the chat! Now type your name and press enter!", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()

def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""

    name = client.recv(BUFSIZ).decode("utf8")
    welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s has joined the chat!" % name
    broadcast(bytes(msg, "utf8"))
    clients[client] = name
    
    while True:
        msg = client.recv(BUFSIZ)
        if msg == bytes("{quit}", "utf8"):
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s has left the chat." % name, "utf8"))
            time.sleep(1)
            break
        else:
            broadcast(msg, name+": ")
            message_water = Water_Drop(msg.decode("utf-8"), water_drop_sf)
            message_water.out()
            print("Message: ", msg.decode("utf-8"))

def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""
    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)


""" BELOW HERE are the global variables """     
clients = {}
addresses = {}


""" Set only HOST and PORT according to your wifi/lan + Client settings"""

#HOST = '127.0.0.1'
HOST = str(gethostbyname(getfqdn()))
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    print(HOST)
    #Start main track here
    s = pyo.Server(sr=48000, nchnls=8, buffersize=512, duplex=1).boot()
    s.start()
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
#    MAIN_TRACK = Thread(target=main_backingtrack())
#    MAIN_TRACK.start()
#    MAIN_TRACK.join()
    ACCEPT_THREAD.join()
    SERVER.close()
    s.stop()
    s.shutdown()