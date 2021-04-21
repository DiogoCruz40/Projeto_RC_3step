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

def secure_pass(param):

    while True:
        password = stdiomask.getpass(prompt=param)

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
            print("Erro: Insira um email válido")


def remove_accents(data):
    return unicodedata.normalize('NFD', data).encode('ascii', 'ignore').decode("utf-8")


def isNotBlank(mystring):
    if mystring and mystring.strip():  # se nao for null e se tiver algo la dentro a nao ser espacos devolve true
        return True

    return False


def AjustContent(text):  # primeira letra de cada palavra maiuscula

    text = text.strip()
    separatext = re.split('([.!?,/ ' '] *)', text)
    final = ''.join([i.capitalize() for i in separatext])

    return final

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

#==========================================Login============================================================#

def login(client):
    while 1:
        print('\nLogin System Manager')
        mail = emailREGEX('Mail: ').lower()
        send(mail,client) #1
        if read(client) == 'Mail False': #2
            print('Mail doesnt exist')
            continue

        password = secure_pass('Password:')
        send(password, client) #3
        flagpass=read(client) #4
        if  flagpass == 'True':
            name=read(client)
            menulogin(client,name)
            break
        elif flagpass == 'False':
            print('Failed to Login')


def menulogin(client,name):
  
    while 1:

        try:
            print(f'\nHello {name},')
            option=input(' 1) Validate an account\n 2) Delete an account\n 3) Exit \n Select: ')
            if option == '1':
                send(option,client)
                validateanaccount(client,name)
            elif option == '2':
                send(option,client)
                deleteanaccount(client,name)
            elif option == '3':
                send(option,client)
                return
                
        except Exception as e:
            print(e)

#==============Validate an account======================================#
def validateanaccount(client,name):
    while 1:
        print(f'\nHello {name},')
        mail = emailREGEX('The email of the account you want to validate: ').lower()
        send(mail,client) #1
        if read(client) == 'Mail False': #2
            print('Mail doesnt exist or already validated')
            continue
        else:
            print('Account Validated')
            return
        

#==============Delete an account======================================#
def deleteanaccount(client,name):
    while 1:
        print(f'\nHello {name},')
        mail = emailREGEX('The email of the account you want to delete: ').lower()
        send(mail,client) #1
        if read(client) == 'Mail False': #2
            print('Mail doesnt exist')
            continue
        else:
            print('Account deleted')
            return
        

#==========================================================================================================#

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    print(read(client)) #Read People Menu
    while 1:
        try:
            print('Menu System Manager')
            opt=input(' 1) Login\n 2) Exit \n Select: ')
            if opt == '1':
                send(opt,client)
                login(client)
            if opt == '2':
                send(opt,client)
                return
                
        except Exception as e:
            print(e)
    