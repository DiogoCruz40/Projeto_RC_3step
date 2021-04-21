import socket
import stdiomask
from passlib.handlers.sha2_crypt import sha256_crypt
import re

HEADER = 64
PORT = 8200
FORMAT = 'utf-8' 
DISCONNECT_MSG = '!DISCONNECT'
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

def secure_pass():

    while True:
        password = stdiomask.getpass()

        if not password or " " in password:
          print("Não pode ter espaços!")
          continue

        break

    return password


def emailREGEX(pergunta):
    while True:
        email = input(pergunta)

        if bool(re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+.[a-zA-Z0-9-.]+$)", email)):
            return str(email)
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
        mail = emailREGEX('Mail: ').lower()
        send(mail,client) #1
        if read(client) == 'Mail False': #2
            print('Mail doesnt exist\n')
            continue

        password = secure_pass()
        send(password, client) #3
        flagpass=read(client) #4
        if  flagpass == 'True':
            print('Logged in\n')
            break
        elif flagpass == 'False':
            print('Failed to Login\n')

#==========================================================================================================#

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    print(read(client)) #Read People Menu
    while 1:
        try:
            opt=input(' 1) Login\n 2) Exit \n Select: ')
            if opt == '1':
                send(opt,client)
                login(client)
            if opt == '2':
                send(opt,client)
                return
                
        except Exception as e:
            print(e)
    