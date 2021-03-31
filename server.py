import socket
import threading
import os
import json

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
#SERVER = '192.168.1.70'
ADDR =  (SERVER, PORT)
FORMAT = 'utf-8' 
DISCONNECT_MSG = '!DISCONNECT'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def send(msg, conn):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length)) #PADDING
    conn.send(send_length)
    conn.send(message)   

def read(conn, addr):      
    msg_length = conn.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        msg = conn.recv(msg_length).decode(FORMAT)
        return msg
 

def handle_client(conn, addr, users):
    print(f"[NEW CONNECTION] {addr} connected")
    users[str(addr)] = str(len(users) + 1)
    with open('data.json', 'w') as fp:
        json.dump(users, fp, sort_keys=True, indent=4)
    connected = True

    while connected:
        send(str(users.values()), conn)
        msg = read(conn, addr)
        
        if msg == DISCONNECT_MSG:
            connected = False
            users.pop(str(addr))

        
            
    conn.close()

def start():
    server.listen()
    print(f'[LISTENING] Server is listening on {SERVER}')
    try:
        with open('data.json', 'r') as fp:
            users = json.load(fp)
    except json.decoder.JSONDecodeError:
        users = {}
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr, users))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")



print("[STARTING] server is starting...")
start()


