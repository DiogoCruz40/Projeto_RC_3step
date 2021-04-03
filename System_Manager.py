import socket
import getch
from passlib.handlers.sha2_crypt import sha256_crypt
import re
import sys

HEADER = 64
PORT = 9050
FORMAT = 'utf-8' 
DISCONNECT_MSG = '!DISCONNECT'
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

def secure_pass(prompt=''):
    p_s = ''
    proxy_string = [' '] * 64
    while True:
        sys.stdout.write('\x0D' + prompt + ''.join(proxy_string))
        c = getch()
        if c == b'\r':
            break
        elif c == b'\x08':
            p_s = p_s[:-1]
            proxy_string[len(p_s)] = " "
        else:
            proxy_string[len(p_s)] = "*"
            p_s += c.decode()

    sys.stdout.write('\n')
    return p_s


def emailREGEX(pergunta):
    while True:
        email = input(pergunta)
        print(email)
        if re.match('^[a-zA-Z0-9]+[\._]?[a-zA-Z0-9]+\w[@]+[.]\w+$',email):
            return email
        else:
            print("Erro: Insira um email válido \n")
    




#==========================================================================================================#

def read(client):      
    msg_length = client.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        msg = client.recv(msg_length).decode(FORMAT)
    return msg 

def send(msg, client):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length)) #PADDING
    client.send(send_length)
    client.send(message)

#==========================================================================================================#

def login(client):
    while 1:
        #mail = emailREGEX('Mail: ').lower()
        mail=input('Mail: ')
        send(mail,client)
        if read(client) == 'Mail False':
            print('Mail doesnt exist\n')
            continue

        #print("Password: ")
        #password = secure_pass()

        password=input('Password: ')
        send(password, client)
        flagpass=read(client)
        if  flagpass == 'True':
            print('Logged in\n')
            break
        elif flagpass == 'False':
            print('Failed to Login\n')


def signup(client):
    while 1:
       # mail = emailREGEX('Mail: ').lower()
        mail=input('Mail: ')
        send(mail, client)
        if read(client) == 'already exists':
            print('This mail already exists\n')
            continue
        else:
            break

    #print("Password: ")
    #password=secure_pass()
    password=input('Password: ')
    epchave = sha256_crypt.hash(password)
    send(epchave,client)





#==========================================================================================================#

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    print(read(client)) #Read People Menu
    while 1:
        try:
            opt=int(input(' 1) Login\n 2) Sign up\n 3) Exit \n Select: '))
            if opt == 1:
                send(str(opt),client)
                login(client)
            if opt == 2:
                send(str(opt),client)
                signup(client)
            if opt == 3:
                send(str(opt),client)
                return
                
        except Exception as e:
            print(e)

    #print(read(client)) #Read People Menu
    # send(opt) # Send person to talk to
    # opt = input('Password: ')
    # send(opt) #Send content
    # print(read()) #Job
   





