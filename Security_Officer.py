from passlib.utils import saslprep
from server import handle_alarm
import socket
import threading
import stdiomask
from os import system, truncate
from passlib.handlers.sha2_crypt import sha256_crypt
import re
from prettytable import PrettyTable
import time
from datetime import datetime
import datetime
import select
import unicodedata
HEADER = 64
PORT = 8300
FORMAT = 'utf-8' 
DISCONNECT_MSG = '!DISCONNECT'
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
clear = lambda: system('clear')
alarm=False
time_to_exit = False

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
    

def emailREGEXMANAGER(pergunta):
    while True:
        email = input(pergunta)

        if bool(re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+.[a-zA-Z0-9-.]+$)", email)) or email == '0':
            return str(email)
        else:
            print("Erro: Insira um email válido")

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


def representsint(a):  # ve se e inteiro
    try:
        int(a)
        return True
    except ValueError:
        return False


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
        print('Login Security Officer')
        mail = emailREGEX('Mail: ').lower()
        send(mail,client) #1
        if read(client) == 'Mail False': #2
            print('Mail doesnt exist or not validated yet')
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
            thread=threading.Thread(target=handle_alarme_security,args=(SERVER,8400))
            thread.start()
            menulogin(client,mail,name)
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


def menulogin(client,mail,name):
    global alarm
    delete = False    
    while 1:

        if delete == True:
            break

        try:
            clear()
            print(f'Hello {name},')
            
            if alarm == True:
                print('\nALARM ACTIVATED!!!\n')
            option=input(' 1) Consult occurrence\n 2) Change profile\n 3) Erase account\n 4) Consult Alarms\n 5) Help\n 6) Exit \n Select: ')
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
                alarmconsult(client,mail,name)
            elif option == '6':
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
            global alarm
            if alarm == True:
                print('\nALARM ACTIVATED!!!\n')
            option=input(' 1) Pesquisar por palavra na descrição  \n 2) Pesquisar por data  \n 3) Pesquisar por localidade \n 4) Pesquisar por profisisonal de saude  \n 5) Exit \n Select: ')
            if option == '1':
                send(option, client)   #2
                word = wordsREGEX(" Qual a palavra para pesquisar?\n >>")
                send(word, client)
                clear()
                print(f'\nHello {name},')
                print('\n   >> Consulta de Ocorrências por ' + word + ' na descrição \n\n')
                printall(client,mail,name)
                result = input("\n Prima qualquer tecla para voltar atrás\n")
                break
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
                print(f'\nHello {name},')
                print('\n   >> Consulta de Ocorrências pela data ' + date + ' \n\n')
                printall(client,mail,name)
                result = input("\n Prima qualquer tecla para voltar atrás\n")
                break
            elif option == '3':
                send(option, client)
                word = wordsREGEX(" Qual a localidade para pesquisar?\n >>")
                send(word, client)
                clear()
                print(f'\nHello {name},')
                print('\n   >> Consulta de Ocorrências pela localidade ' + word + ' \n\n')
                printall(client,mail,name)
                result = input("\n Prima qualquer tecla para voltar atrás\n")
                break
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
                print(f'\nHello {name},')
                print('\n   >> Consulta de Ocorrências por utilizador com ID ' + str(id_cl) + ' \n\n')
                printall(client,mail,name)
                result = input("\n Prima qualquer tecla para voltar atrás\n")
                break
            elif option == '5':
                send(option, client)
                break
        
            else:
               send('6',client)
               continue

        except Exception as e:
            print(e)

        
     
def printall(client, mail, name):
    endofdata = 'False'
    while 1:
        nrofoccurences = read(client)  #1
        #print(nrofoccurences)
        send('testing', client)  #2
        nrofoccurences = int(nrofoccurences)
        if(nrofoccurences == 0):
            print("Não tem ocorrencias disponíveis para visualização de momento\n")
            return
        else:
            try:
                #Creation of table by parts
                #part 1 - get the title
                tittle = gettabletittle(client, mail, name)
                #print(tittle)
                table = PrettyTable() 
                table.field_names = tittle  
                send('Ready', client)    #8
                
                while read(client) != 'Start':  #9
                    continue
                while nrofoccurences>0:     

                    nrofoccurences = nrofoccurences-1
                    table.add_row(read(client).split(","))

                    send("next", client)

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
        while read(client)!= 'TitleStart':   #3
            continue
        send('Ready', client)    #4
        element = 0
        while element!= 'Stop': 
            element = read(client)  #5    #7
            if element == 'Stop':
                continue
            else:
                tittleelements.append(element)  
            send('next', client)    #6
           
    except Exception as e:
                print(e)

    return tittleelements

#==============Change profile=======================================#

def changeprofile(client,mail,name):
     while 1:
        try:
            clear()
            print(f'Hello {name},')
            print('\nProfile')
            global alarm
            if alarm == True:
                print('\nALARM ACTIVATED!!!\n')
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
        clear()
        print(f'Hello {name},')
        print('Mail change')
        global alarm
        if alarm == True:
            print('\nALARM ACTIVATED!!!\n')
        password = secure_pass('Password:')
        send(password, client) 
        if read(client) == 'True Password':
            while 1:
                newmail = emailREGEX('New Mail: ').lower()
                send(newmail, client) 
                if read(client) == 'already exists': 
                    print('This mail already exists')
                    while 1:
                        optmail=input('Sure you want to try again[y/n]?:').lower()
                        if optmail == 'y':
                            send('Try again Mail True',client)
                            break
                        elif optmail == 'n':
                            send('Try again Mail False',client)
                            return email
                        else:
                            continue
                    continue
                else:
                    while 1:
                        optmailconfirm=input('Do you confirm mail change[y/n]?:').lower()
                        if optmailconfirm == 'y':
                            send('Mail Change True',client)
                            print('Email alterado com sucesso!')
                            input('Pressiona qualquer tecla para continuar...')
                            return newmail
                        elif optmailconfirm == 'n':
                            send('Mail Change False',client)
                            return email
                        else:
                            continue
                    
        else:
            print('Wrong password')
            while 1:
                optpass=input('Sure you want to try again[y/n]?:').lower()
                if optpass == 'y':
                    send('Try again Pass True',client)
                    break
                elif optpass == 'n':
                    send('Try again Pass False',client)
                    return email
                else:
                    continue
            continue
    

def changepassword(client,email,name):
    while 1:
        clear()
        print(f'Hello {name},')
        print('Password change')
        global alarm
        if alarm == True:
            print('\nALARM ACTIVATED!!!\n')
        password = secure_pass('Current Password:')
        send(password, client) 
        if read(client) == 'True Password':
            newpassword = secure_pass('New password:')
            epchave = sha256_crypt.hash(newpassword)
            send(epchave, client)
            while 1:
                optpassconfirm =input('Do you confirm pass change[y/n]?:').lower()
                if optpassconfirm == 'y':
                    send('Pass Change True',client)
                    print('Password alterada com sucesso!')
                    input('Pressiona qualquer tecla para continuar...')
                    return 
                elif optpassconfirm == 'n':
                    send('Pass Change False',client)
                    return
                else:
                    continue
        else:
            print('Wrong password')
            while 1:
                optpass=input('Sure you want to try again[y/n]?:').lower()
                if optpass == 'y':
                    send('Try again Pass True',client)
                    break
                elif optpass == 'n':
                    send('Try again Pass False',client)
                    return 
                else:
                    continue
            continue

def changename(client,email,name):
    while 1:
        clear()
        print(f'Hello {name},')
        print('Name change')
        global alarm
        if alarm == True:
            print('\nALARM ACTIVATED!!!\n')
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
                    while 1:
                        optname=input('Do you confirm name change[y/n]?:').lower()
                        if optname == 'y':
                            send('Name Change True',client)
                            print('Nome alterado com sucesso!')
                            input('Pressiona qualquer tecla para continuar...')
                            return newname
                        elif optname == 'n':
                            send('Name Change False',client)
                            return name
                        else:
                            continue
                   
        else:
            print('Wrong password')
            while 1:
                optpass=input('Sure you want to try again[y/n]?:').lower()
                if optpass == 'y':
                    send('Try again Pass True',client)
                    break
                elif optpass == 'n':
                    send('Try again Pass False',client)
                    return name
                else:
                    continue
            continue

#==============Erase account======================================#

def eraseaccount(client,email,name):
    while 1:
        clear()
        print(f'Hello {name},')
        password = secure_pass('Password:')
        send(password, client) 
        if read(client) == 'True Password':
            while 1:
                delete = input('Sure you want to delete the account[y/n]?: ').lower()

                if delete == 'y':
                    send(delete, client)
                    print('Conta eliminada com sucesso!')
                    input('Pressiona qualquer tecla para continuar...')
                    return True

                elif delete == 'n':
                    send(delete, client)
                    return False

                else:
                    continue
        else:
            print('Wrong password')
            while 1:
                optpass=input('Sure you want to try again[y/n]?:').lower()
                if optpass == 'y':
                    send('Try again Pass True',client)
                    break
                elif optpass == 'n':
                    send('Try again Pass False',client)
                    return name
                else:
                    continue
            continue

#==========================================Signup==========================================================#
def signup(client):
    
    while 1:
        clear()
        print('Signup Security Officer')
        name = input('Name: ')
        if not isNotBlank(name):
            print('Insert a valid name')
            continue
        else:
            name=AjustContent(name)
            send(name, client)
            break

    while 1:
        clear()
        print('Signup Security Officer')
        print(f'Name:{name}')
        mail = emailREGEX('Mail: ').lower()
        send(mail, client) #1
        if read(client) == 'already exists': #2
            print('This mail already exists')
            while 1:
                optmail=input('Sure you want to try again[y/n]?:').lower()
                if optmail == 'y':
                    send('Try again Mail True',client) #1
                    break
                elif optmail == 'n':
                    send('Try again Mail False',client) #1
                    return
                else:
                    continue
            continue
        else:
            clear()
            print('Signup Security Officer')
            print(f'Name:{name}')
            print(f'Mail:{mail}')
            password = secure_pass('Password:')
            epchave = sha256_crypt.hash(password)
            send(epchave,client) #3
            while 1:
                optionsignin = input('Confirma o registo da conta[y/n]?:').lower()
                if optionsignin == 'y':
                    send('Confirm True',client)
                    print('Conta criada com sucesso')
                    input('Pressione qualquer tecla para continuar...')
                    break
                elif optionsignin == 'n':
                    send('Confirm False',client)
                    break
                else:
                    continue
            break
#==========================================Handle Alarm====================================================#

def alarmconsult(client,mail,name):
    global alarm
    if read(client) == 'All answered': #1
        alarm=False
    while 1:
        clear()
        print(f'Hello {name},')
        print('Alarm Consulting')
        allalarms = eval(read(client)) #2
        table_alarms = PrettyTable()
        table_alarms.title = 'Alarms'
        table_alarms.field_names=["Id","Nome do professional","Email do professional","Hora e Data","Local","Respondido"]
        table_alarms._max_width = {"Local" : 50}
        for alarme in allalarms:
                table_alarms.add_row(alarme)
        print(table_alarms)

        id_alarm = input('The id of the professional you want to rescue(0 to exit): ')
        if not representsint(id_alarm):
            send('Not int',client)
            continue
        else:
            send('int',client)

        send(id_alarm,client) #1
        if id_alarm == '0':
            return

        if read(client) == 'id False': #2
            print('ID doesnt exist or professional already rescued')
            input('Pressiona qualquer tecla para continuar...')
            continue
        else:
            while 1:
                optmailconfirm=input('Do you confirm the rescue[y/n]?:').lower()
                if optmailconfirm == 'y':
                    send('ID Confirm True',client)
                    if read(client) == 'All answered':
                        alarm=False
                    print('On the move')
                    input('Pressiona qualquer tecla para continuar...')
                    return 
                elif optmailconfirm == 'n':
                    send('ID Confirm False',client)
                    return
                else:
                    continue

def handle_alarme_security(SERVER_ALARM,PORT_ALARM):
    ADDR_ALARM=(SERVER_ALARM,PORT_ALARM)
    client_alarm = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_alarm.connect(ADDR_ALARM)
    global alarm,time_to_exit

    while not time_to_exit:
        ready = select.select([client_alarm], [], [], 0.3)
        if ready[0]:
            if read(client_alarm) == 'Alarm':
                alarm=True
                print('\n \t\tALARM ACTIVATED!!!\n \t\tPRESS ANY KEY TO CONTINUE...')
                while True:
                    if not alarm:
                        send('discard',client_alarm)
                        break
                    if time_to_exit:
                        send('get out',client_alarm)
                        client_alarm.close()
                        return
    send('get out',client_alarm)
    client_alarm.close()
    return
#==========================================================================================================#

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    print(read(client)) #Read People Menu
    while 1:
        try:
            clear();
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
                global time_to_exit
                time_to_exit = True
                client.close()
                return
                
        except Exception as e:
            print(e)
    
