# Python program to implement server side of chat room.
import socket
import select
import sys
from _thread import *

# Skapa server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Kontrollera om rätt antal argument har tillhandahållits
if len(sys.argv) != 3:
    print("Correct usage: script, IP address, port number")
    exit()

# Ta emot IP-adress och portnummer från kommandoraden
IP_address = str(sys.argv[1])
Port = 12345

# Binda servern till IP-adressen och portnumret
server.bind((IP_address, Port))

# Lyssna på upp till 100 anslutningar
server.listen(100)

list_of_clients = []


def clientthread(conn, addr):
    # Skicka välkomstmeddelande till klienten
    conn.send("Welcome to this chatroom!".encode())

    while True:
        try:
            message = conn.recv(2048).decode()
            if message:
                print(f"<{addr[0]}> {message}")

                # Skicka meddelandet till alla andra klienter
                message_to_send = f"<{addr[0]}> {message}"
                broadcast(message_to_send, conn)
            else:
                remove(conn)
        except:
            continue


def broadcast(message, connection):
    for clients in list_of_clients:
        if clients != connection:
            try:
                clients.send(message.encode())
            except:
                clients.close()
                remove(clients)


def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)


while True:
    conn, addr = server.accept()
    list_of_clients.append(conn)
    print(f"{addr[0]} connected")

    start_new_thread(clientthread, (conn, addr))

conn.close()
server.close()
