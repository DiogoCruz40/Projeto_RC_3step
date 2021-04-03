import socket
import threading
import os

HEADER = 64
SERVER = socket.gethostbyname(socket.gethostname())
#SERVER = '192.168.1.70'
FORMAT = 'utf-8' 
DISCONNECT_MSG = '!DISCONNECT'


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
 
#============================================================================================================================#


def handle_professional(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected")
    connected = True
    while connected:
        send('Health Professional', conn)
        msg = read(conn, addr)
        
        if msg == DISCONNECT_MSG:
            connected = False
              
    conn.close()


def handle_manager(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected")
    connected = True
    while connected:
        send('System Manager', conn)
        msg = read(conn, addr)
        
        if msg == DISCONNECT_MSG:
            connected = False
                  
    conn.close()


def handle_security(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected")
    connected = True
    while connected:
        send('Security Officer', conn)
        msg = read(conn, addr)
        
        if msg == DISCONNECT_MSG:
            connected = False
                 
    conn.close()


#============================================================================================================================#

def start(PORT, SERVER):
    ADDR =  (SERVER, PORT)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f'[LISTENING] Server is listening on {SERVER}')
    while True:
        conn, addr = server.accept()
        if PORT == 5050:
            thread = threading.Thread(target=handle_professional, args=(conn, addr))
        elif PORT == 9050:
            thread = threading.Thread(target=handle_manager, args=(conn, addr))
        elif PORT == 9000:
            thread = threading.Thread(target=handle_security , args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


def main(SERVER):
    print("[STARTING] server is starting...")
    pid = os.fork()
    
    if pid == 0 :
        print('Health Professional')
        start(5050, SERVER)

    else:
        pid2 = os.fork()
        if pid2 == 0:
            print('System Manager')
            start(9050, SERVER)
    
        else:
            print('Security Officer')
            start(9000, SERVER)
       


if __name__ == "__main__":
    main(SERVER)