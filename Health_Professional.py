import socket
import stdiomask
from passlib.handlers.sha2_crypt import sha256_crypt
import re

HEADER = 64
PORT = 8100
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
        print('\nLogin Health Professional')
        mail = emailREGEX('Mail: ').lower()
        send(mail,client) #1
        if read(client) == 'Mail False': #2
            print('Mail doesnt exist')
            continue

        password = secure_pass('Password:')
        send(password, client) #3
        flagpass=read(client) #4
        if  flagpass == 'True':
            menulogin(client,mail)
            break
        elif flagpass == 'False':
            print('Failed to Login')


def menulogin(client,mail):
    while 1:
        try:
            print('\nHello',mail,',')
            option=input('1) Create occurrence\n 2) Change profile\n 3) Erase account\n 4) Exit \n Select: ')
            if option == '1':
                continue
            elif option == '2':
                changeprofile(client,mail)
            elif option == '3':
                eraseaccount(client,mail)
            elif option == '4':
                return
                
        except Exception as e:
            print(e)

#==============Change profile====================================#

def changeprofile(client,mail):
     while 1:
        try:
            print('\nHello',mail,',')
            option=input('1) Change email\n 2) Change password\n 3) Exit \n Select: ')
            if option == '1':
                changemail(client,mail)
            elif option == '2':
                changepassword(client,mail)
            elif option == '3':
                return
                
        except Exception as e:
            print(e)

def changemail(client,email):
    while 1:
        print('\nHello',mail,',')
        password = secure_pass('Password:')
        send(password, client) 
        if read(client) == 'True Password':
            newmail = emailREGEX('New Mail: ').lower()
            send(newmail, client) #1
            if read(client) == 'already exists': #2
                print('This mail already exists')
                continue
            else:
                send(newmail,client)
                return
        else:
            print('Wrong password')
            continue
    

def changepassword(client,email):
    while 1:
        print('\nHello',mail,',')
        password = secure_pass('Current Password:')
        send(password, client) 
        if read(client) == 'True Password':
            newpassword = secure_pass('New password:')
            send(newpassword, client)
        else:
            print('Wrong password')
            continue
    

#==============Erase account======================================#


#==========================================Signup==========================================================#
def signup(client):
    while 1:
        print('\nSignup Health Professional')
        mail = emailREGEX('Mail: ').lower()
        send(mail, client) #1
        if read(client) == 'already exists': #2
            print('This mail already exists')
            continue
        else:
            password = secure_pass('Password:')
            epchave = sha256_crypt.hash(password)
            send(epchave,client) #3
            break


#==========================================================================================================#

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    print(read(client)) #Read People Menu
    while 1:
        try:
            print('Menu Health Professional')
            opt=input(' 1) Login\n 2) Sign up\n 3) Exit \n Select: ')
            if opt == '1':
                send(opt,client)
                login(client)
            elif opt == '2':
                send(opt,client)
                signup(client)
            elif opt == '3':
                send(opt,client)
                return
                
        except Exception as e:
            print(e)
    





