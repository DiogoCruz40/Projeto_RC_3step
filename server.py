import socket
import threading
import os
import psycopg2.extras
from passlib.handlers.sha2_crypt import sha256_crypt

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
 
#===================================================HEALTH PROFESSIONAL========================================================#


def handle_professional(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected")
    connected = True
    while connected:
        send('Health Professional CONNECTED', conn)
        msg = read(conn, addr)
        
        if msg == DISCONNECT_MSG:
            connected = False
              
    conn.close()

#=======================================================SYSTEM MANAGER===========================================================#

def handle_manager(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected")
    connected = True
    while connected:
        send('System Manager CONNECTED', conn)
        opt = int(read(conn, addr))
        if opt == 1:
            loginverify(conn, addr)
        if opt == 2:
            signupverify(conn, addr)
        if opt == 3:
            connected = False         
    conn.close()

def loginverify(conn, addr):
   
    connDB = psycopg2.connect("host=localhost dbname=postgres user=postgres password=postgres")
    cur = connDB.cursor(cursor_factory=psycopg2.extras.DictCursor)
    while 1:
        mail = read(conn, addr)
        cur.execute("SELECT pass FROM gestor_sistema WHERE email_g=%s",(mail,))
        if cur.rowcount == 1:
            password = cur.fetchone()[0]
            password_login = read(conn,addr)
            verifypass=sha256_crypt.verify(password_login, password)
            if verifypass:
                send('True', conn)
                break
            send('False', conn)
            continue
        send('False', conn)
    
    connDB.close()
    cur.close()
    return

def signupverify(conn, addr):
    connDB = psycopg2.connect("host=localhost dbname=postgres user=postgres password=postgres")
    cur = connDB.cursor(cursor_factory=psycopg2.extras.DictCursor)
    while 1:
        mail = read(conn, addr)
        cur.execute("SELECT email_g FROM gestor_sistema WHERE email_g=%s",(mail,))
        if cur.rowcount > 0:
            send('already exists',conn)
            
        else:
            send('Nao existe',conn)
            password = read(conn,addr)
            cur.execute("INSERT INTO gestor_sistema(email_g, pass) VALUES (%s,%s)",(mail,password))
            connDB.commit()
            break
        
    connDB.close()
    cur.close()
    return



    
#===========================================================SECURITY OFFICER======================================================#

def handle_security(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected")
    connected = True
    while connected:
        send('Security Officer CONNECTED', conn)
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