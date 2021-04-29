import socket
import stdiomask
from passlib.handlers.sha2_crypt import sha256_crypt
import re
from os import system
from prettytable import PrettyTable

HEADER = 64
PORT = 8200
FORMAT = 'utf-8' 
DISCONNECT_MSG = '!DISCONNECT'
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
clear = lambda: system('clear')

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

def emailREGEXMANAGER(pergunta):
    while True:
        email = input(pergunta)

        if bool(re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+.[a-zA-Z0-9-.]+$)", email)) or email == '0':
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
        clear()
        print('Login System Manager')
        mail = emailREGEX('Mail: ').lower()
        send(mail,client) #1
        if read(client) == 'Mail False': #2
            print('Mail doesnt exist')
            while 1:
                optionlogin = input('Do you like to try again[y/n]?:').lower()
                if optionlogin == 'y':
                    send('Try again Mail True',client)
                    break
                elif optionlogin == 'n':
                    send('Try again Mail False',client)
                    return
                else:
                    continue
            continue

        password = secure_pass('Password:')
        send(password, client) #3
        flagpass=read(client) #4
        if  flagpass == 'True':
            name=read(client)
            menulogin(client,name)
            break
        elif flagpass == 'False':
            print('Wrong Password')
            while 1:
                optionlogin = input('Do you like to try again[y/n]?:').lower()
                if optionlogin == 'y':
                    send('Try again Pass True',client)
                    break
                elif optionlogin == 'n':
                    send('Try again Pass False',client)
                    return
                else:
                    continue
            continue

def menulogin(client,name):
  
    while 1:

        try:
            clear()
            print(f'Hello {name},')
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
        clear()
        print(f'Hello {name},')
        print('Validation')
        allprofessionals = eval(read(client))
        allsecuritys = eval(read(client))
        table_professionals = PrettyTable()
        table_securitys = PrettyTable()
        table_professionals.title = 'Health Professionals'
        table_professionals.field_names=["Nome do professional","Email do professional","Validado"]
        for professional in allprofessionals:
                table_professionals.add_row(professional)
        table_securitys.title = 'Security Officers'
        table_securitys.field_names=['Nome do agente','Email do agente','Validado']
        for security in allsecuritys:
            table_professionals.add_row(security)
        print(table_professionals)
        print(table_securitys)
        mail = emailREGEXMANAGER('The email of the account you want to validate(0 to exit): ').lower()
        send(mail,client) #1
        if mail == '0':
            return
        flag = read(client)
        if flag == 'Mail False': #2
            print('Mail doesnt exist or already validated')
            input('Pressiona qualquer tecla para continuar...')
            continue
        else:
            while 1:
                optmailconfirm=input('Do you confirm account validation[y/n]?:').lower()
                if optmailconfirm == 'y':
                    send('Mail Confirm True',client)
                    print('Account Validated')
                    input('Pressiona qualquer tecla para continuar...')
                    return 
                elif optmailconfirm == 'n':
                    send('Mail Confirm False',client)
                    return
                else:
                    continue
                
            
#==============Delete an account======================================#
def deleteanaccount(client,name):
    while 1:
        clear()
        print(f'Hello {name},')
        print('Deletion')
        allprofessionals = eval(read(client))
        allsecuritys = eval(read(client))
        table_professionals = PrettyTable()
        table_securitys = PrettyTable()
        table_professionals.title = 'Health Professionals'
        table_professionals.field_names=["Nome do professional","Email do professional","Validado"]
        for professional in allprofessionals:
                table_professionals.add_row(professional)
        table_securitys.title = 'Security Officers'
        table_securitys.field_names=['Nome do agente','Email do agente','Validado']
        for security in allsecuritys:
            table_professionals.add_row(security)
        print(table_professionals)
        print(table_securitys)
        mail = emailREGEXMANAGER('The email of the account you want to validate(0 to exit): ').lower()
        send(mail,client) #1
        if mail == '0':
            return

        if read(client) == 'Mail False': #2
            print('Mail doesnt exist')
            input('Pressiona qualquer tecla para continuar')
            continue
        else:
            while 1:
                optmailconfirm=input('Do you confirm account deletion[y/n]?:').lower()
                if optmailconfirm == 'y':
                    send('Mail Confirm True',client)
                    print('Account Deleted')
                    input('Pressiona qualquer tecla para continuar...')
                    return 
                elif optmailconfirm == 'n':
                    send('Mail Confirm False',client)
                    return
                else:
                    continue
        

#==========================================================================================================#

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    print(read(client)) #Read People Menu
    while 1:
        try:
            clear()
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
    