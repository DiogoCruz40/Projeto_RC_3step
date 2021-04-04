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
    send('Health Professional CONNECTED', conn)
    while connected:

        try:
            opt = read(conn, addr)
            if opt == '1':
                loginverifyprofessional(conn, addr)
            if opt == '2':
                signupverifyprofessional(conn, addr)
            if opt == '3':
                connected = False      

        except Exception as e:
            print(e)
   
    conn.close()

def loginverifyprofessional(conn, addr):
   
    connDB = psycopg2.connect("host=localhost dbname=postgres user=postgres password=postgres")
    cur = connDB.cursor(cursor_factory=psycopg2.extras.DictCursor)
    while 1:
        mail = read(conn, addr) #1
        cur.execute("SELECT pass FROM profissional_de_saude WHERE email_p=%s",(mail,))
        if cur.rowcount == 1:
            send('Mail True',conn) #2
            password = cur.fetchone()[0]
            password_login = read(conn,addr) #3
            verifypass=sha256_crypt.verify(password_login, password)
            if verifypass:
                send('True', conn) #4
                break
            else:
                send('False', conn) #4
                continue
        else:
            send('Mail False', conn) #2
            continue
    
    connDB.close()
    cur.close()
    return

def signupverifyprofessional(conn, addr):
    
    connDB = psycopg2.connect("host=localhost dbname=postgres user=postgres password=postgres")
    cur = connDB.cursor(cursor_factory=psycopg2.extras.DictCursor)
    while 1:
        mail = read(conn, addr) #1
        cur.execute("SELECT email_p FROM profissional_de_saude WHERE email_p=%s",(mail,))
        if cur.rowcount != 0:
            send('already exists',conn) #2
            continue
        else:
            send('doesnt exist',conn) #2
            password = read(conn,addr) #3
            cur.execute("INSERT INTO profissional_de_saude(email_p, pass) VALUES (%s,%s)",(mail,password))
            connDB.commit()
            break
    connDB.close()
    cur.close()
    return

#=======================================================SYSTEM MANAGER===========================================================#

def handle_manager(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected")
    connected = True
    send('System Manager CONNECTED', conn)
    while connected:

        try:
            opt = read(conn, addr)
            if opt == '1':
                loginverifymanager(conn, addr)
            if opt == '2':
                signupverifymanager(conn, addr)
            if opt == '3':
                connected = False      

        except Exception as e:
            print(e)
   
    conn.close()

def loginverifymanager(conn, addr):
   
    connDB = psycopg2.connect("host=localhost dbname=postgres user=postgres password=postgres")
    cur = connDB.cursor(cursor_factory=psycopg2.extras.DictCursor)
    while 1:
        mail = read(conn, addr) #1
        cur.execute("SELECT pass FROM gestor_sistema WHERE email_g=%s",(mail,))
        if cur.rowcount == 1:
            send('Mail True',conn) #2
            password = cur.fetchone()[0]
            password_login = read(conn,addr) #3
            verifypass=sha256_crypt.verify(password_login, password)
            if verifypass:
                send('True', conn) #4
                break
            else:
                send('False', conn) #4
                continue
        else:
            send('Mail False', conn) #2
            continue
    
    connDB.close()
    cur.close()
    return

def signupverifymanager(conn, addr):

    connDB = psycopg2.connect("host=localhost dbname=postgres user=postgres password=postgres")
    cur = connDB.cursor(cursor_factory=psycopg2.extras.DictCursor)
    while 1:
        mail = read(conn, addr) #1
        cur.execute("SELECT email_g FROM gestor_sistema WHERE email_g=%s",(mail,))
        if cur.rowcount != 0:
            send('already exists',conn) #2
            continue
        else:
            send('doesnt exist',conn) #2
            password = read(conn,addr) #3
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
    send('Security officer CONNECTED', conn)
    while connected:

        try:
            opt = read(conn, addr)
            if opt == '1':
                loginverifysecurity(conn, addr)
            if opt == '2':
                signupverifysecurity(conn, addr)
            if opt == '3':
                connected = False      

        except Exception as e:
            print(e)
   
    conn.close()

def loginverifysecurity(conn, addr):
   
    connDB = psycopg2.connect("host=localhost dbname=postgres user=postgres password=postgres")
    cur = connDB.cursor(cursor_factory=psycopg2.extras.DictCursor)
    while 1:
        mail = read(conn, addr) #1
        cur.execute("SELECT pass FROM agente_seguranca WHERE email_a=%s",(mail,))
        if cur.rowcount == 1:
            send('Mail True',conn) #2
            password = cur.fetchone()[0]
            password_login = read(conn,addr) #3
            verifypass=sha256_crypt.verify(password_login, password)
            if verifypass:
                send('True', conn) #4
                break
            else:
                send('False', conn) #4
                continue
        else:
            send('Mail False', conn) #2
            continue
    
    connDB.close()
    cur.close()
    return

def signupverifysecurity(conn, addr):

    connDB = psycopg2.connect("host=localhost dbname=postgres user=postgres password=postgres")
    cur = connDB.cursor(cursor_factory=psycopg2.extras.DictCursor)
    while 1:
        mail = read(conn, addr) #1
        cur.execute("SELECT email_a FROM agente_seguranca WHERE email_a=%s",(mail,))
        if cur.rowcount != 0:
            send('already exists',conn) #2
            continue
        else:
            send('doesnt exist',conn) #2
            password = read(conn,addr) #3
            cur.execute("INSERT INTO agente_seguranca(email_a, pass) VALUES (%s,%s)",(mail,password))
            connDB.commit()
            break
    connDB.close()
    cur.close()
    return

#============================================================================================================================#

def start(PORT, SERVER):
    ADDR =  (SERVER, PORT)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f'[LISTENING] Server is listening on {SERVER}')
    while True:
        (conn,addr) = server.accept()
        if PORT == 8100:
            thread = threading.Thread(target=handle_professional, args=(conn, addr))
        elif PORT == 8200:
            thread = threading.Thread(target=handle_manager, args=(conn, addr))
        elif PORT == 8300:
            thread = threading.Thread(target=handle_security , args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


def main(SERVER):
    print("[STARTING] server is starting...")
    pid = os.fork()
    
    if pid == 0 :
        print('Health Professional')
        start(8100, SERVER)

    else:
        pid2 = os.fork()
        if pid2 == 0:
            print('System Manager')
            start(8200, SERVER)
    
        else:
            print('Security Officer')
            start(8300, SERVER)
       


if __name__ == "__main__":
    main(SERVER)