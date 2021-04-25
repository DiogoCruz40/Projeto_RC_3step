import socket
import stdiomask
from os import system
from passlib.handlers.sha2_crypt import sha256_crypt
import re
from prettytable import PrettyTable
import time
from datetime import datetime
import datetime

HEADER = 64
PORT = 8300
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
            print("Erro: Insira um email válido \n")
    

def wordsREGEX(pergunta):
    while True:
        words = input(pergunta)
        if bool(re.match('[a-zA-Z,;\s]+$', words)):
            return str(words)
        else:
            print("Erro: Insira apenas palavras \n")


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

#==========================================================================================================#

def login(client):
    while 1:
        print('\nLogin Security Officer')
        mail = emailREGEX('Mail: ').lower()
        send(mail,client) #1
        if read(client) == 'Mail False': #2
            print('Mail doesnt exist or not validated yet')
            continue

        password = secure_pass('Password:')
        send(password, client) #3
        flagpass=read(client) #4
        if  flagpass == 'True':
            name=read(client)
            menulogin(client,mail,name)
            break
        elif flagpass == 'False':
            print('Failed to Login')


def menulogin(client,mail,name):

    delete = False    
    while 1:
        clear()
        if delete == True:
            break

        try:
            print(f'\nHello {name},')
            option=input(' 1) Consult occurence\n 2) Change profile\n 3) Erase account\n 4) Exit \n Select: ')
            if option == '1':
                send(option,client) #1
                occurenceview(client,mail,name)
            elif option == '2':
                send(option,client)
                profile = changeprofile(client,mail,name)
                mail = profile[0]
                name = profile[1]
            elif option == '3':
                send(option,client)
                delete = eraseaccount(client,mail,name)
            elif option == '4':
                send(option,client)
                return
                
        except Exception as e:
            print(e)


#==============Consult Occurence====================================#
def occurenceview(client,mail,name):
    
    while 1:
        try:
            clear()
            print(f'\nHello {name},')
            print('\n   >> Consulta de Ocorrências \n\n')
            printall(client,mail,name)
            option=input(' 1) Pesquisar por palavra na descrição  \n 2) Pesquisar por data  \n 3) Pesquisar por localidade \n 4) Pesquisar por profisisonal de saude  \n 5) Exit \n Select: ')
            if option == '1':
                send(option, client)
                word = wordsREGEX(" Qual a palavra para pesquisar?\n >>")
                send(word, client)
                clear()
                printall(client,mail,name)
                result = input("\n Prima qualquer tecla para voltar atrás\n")
            elif option == '2':
                send(option, client)
                while 1:
                    date = input(" Qual a data para pesquisar?\n >>")
                    try:
                        datetime.datetime.strptime(date, "%Y-%m-%d")             
                        send(date,client)
                        break 
                    except:                    
                        result = input("O formato da data está errado. Deverá ser YYYY-MM-DD\n Prima qualquer tecla para voltar a inserir\n")
                        continue;
                clear()
                printall(client,mail,name)
                result = input("\n Prima qualquer tecla para voltar atrás\n")
            elif option == '3':
                send(option, client)
                word = wordsREGEX(" Qual a localidade para pesquisar?\n >>")
                send(word, client)
                clear()
                printall(client,mail,name)
                result = input("\n Prima qualquer tecla para voltar atrás\n")
            elif option == '4':
                send(option, client)
                while 1:
                    id_cl = input(" Qual o ID do profissional de saude que pretende pesquisar?\n >>")
                    result = id_cl.isdigit()    
                    if result == True:
                        send(id_cl,client)
                        break
                    else:
                        result = input("Introduza um numero válido\n Prima qualquer tecla para voltar a inserir\n")
                        continue;
                clear()
                printall(client,mail,name)
                result = input("\n Prima qualquer tecla para voltar atrás\n")
            elif option == '5':
                break
        except Exception as e:
            print(e)
        break
     
def printall(client, mail, name):
    endofdata = 'False'
    tableelements=[]
    while 1:
        nrofoccurences = read(client)   #2
        send('testing', client)  #3
        nrofoccurences = int(nrofoccurences)
        if(nrofoccurences == 0):
            print("Não tem ocorrencias disponíveis para visualização de momento\n")
        else:
            try:
                #Creation of table by parts
                #part 1 - get the title
                tittle = gettabletittle(client, mail, name)
                table = PrettyTable() 
                table.field_names = tittle  
                send('Ready', client)    #5
                element = 0
                while read(client) != 'Start':  #6
                    continue
                while nrofoccurences>0:
                    while element != 'Stop':
                        element = read(client)
                        if element == 'Stop':
                            send('next', client)
                            break
                        else:
                            tableelements.append(element)
                        send('next', client) 
                    nrofoccurences = nrofoccurences-1
                    table.add_row(tableelements)
                    tableelements=[]
                    element=0   
                print(table)
            except Exception as e:
                print(e)
        endofdata=read(client)
        while endofdata != 'True':
            continue
        break
    
def gettabletittle(client, mail, name):
    try:
        tittleelements=[]
        while read(client)!= 'TitleStart':   #4
            continue
        send('Ready', client)    #5
        element = 0
        while element!= 'Stop': 
            element = read(client)
            if element == 'Stop':
                continue
            else:
                tittleelements.append(element)  #6
            send('next', client)    #7
           
    except Exception as e:
                print(e)

    return tittleelements

#==============Change profile=======================================#

def changeprofile(client,mail,name):
     while 1:
        try:
            print(f'\nHello {name},')
            option=input(' 1) Change email\n 2) Change password\n 3) Change name \n 4) Exit \n Select: ')
            if option == '1':
                send(option,client)
                mail = changemail(client,mail,name)
            elif option == '2':
                send(option,client)
                changepassword(client,mail,name)
            elif option == '3':
                send(option,client)
                name = changename(client,mail,name)
            elif option == '4':
                send(option,client)
                return [mail, name]
                
        except Exception as e:
            print(e)

def changemail(client,email,name):
    while 1:
        print(f'\nHello {name},')
        password = secure_pass('Password:')
        send(password, client) 
        if read(client) == 'True Password':
            while 1:
                newmail = emailREGEX('New Mail: ').lower()
                send(newmail, client) 
                if read(client) == 'already exists': 
                    print('This mail already exists')
                    continue
                else:
                    print('Email alterado com sucesso!')
                    return newmail
        else:
            print('Wrong password')
            continue
    

def changepassword(client,email,name):
    while 1:
        print(f'\nHello {name},')
        password = secure_pass('Current Password:')
        send(password, client) 
        if read(client) == 'True Password':
            newpassword = secure_pass('New password:')
            epchave = sha256_crypt.hash(newpassword)
            send(epchave, client)
            print('Password alterada com sucesso!')
            return
        else:
            print('Wrong password')
            continue

def changename(client,email,name):
    while 1:
        print(f'\nHello {name},')
        password = secure_pass('Password:')
        send(password, client) 
        if read(client) == 'True Password':
            while 1:
                newname = input('New Name: ')
                if not isNotBlank(newname):
                    print('Insert a valid name')
                    continue
                else:
                    newname=AjustContent(newname)
                    send(newname, client)
                    print('Nome alterado com sucesso!')
                    break
            return newname
        else:
            print('Wrong password')
            continue


#==============Erase account======================================#
def eraseaccount(client,email,name):
    while 1:
        print(f'\nHello {name},')
        password = secure_pass('Password:')
        send(password, client) 
        if read(client) == 'True Password':
            while 1:
                delete = input('Sure you want to delete account[y/n]?: ').lower()

                if delete == 'y':
                    send(delete, client)
                    print('Conta eliminada com sucesso!')
                    return True

                elif delete == 'n':
                    send(delete, client)
                    return False

                else:
                    continue
        else:
            print('Wrong password')
            continue

#==========================================Signup==========================================================#
def signup(client):
    while 1:
        print('\nSignup Security Officer')
        name = input('Name: ')
        if not isNotBlank(name):
            print('Insert a valid name')
            continue
        else:
            name=AjustContent(name)
            send(name, client)
            break

    while 1:
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
            print('Menu Security Officer')
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
    
