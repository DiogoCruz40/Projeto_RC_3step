import socket
import stdiomask
from passlib.handlers.sha2_crypt import sha256_crypt
import re
from os import system
import time
from datetime import datetime
import datetime
from dateutil.relativedelta import relativedelta

HEADER = 64
PORT = 8100
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
        print('\nLogin Health Professional')
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

        if delete == True:
            break

        try:
            clear()
            print(f'\nHello {name},')
            option=input(' 1) Create occurrence\n 2) Change profile\n 3) Erase account\n 4) Exit \n Select: ')
            if option == '1':
                send(option,client)
                createoccurence(client,mail,name)
                continue
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

#==============Change profile====================================#

def changeprofile(client,mail,name):
     while 1:
        try:
            clear()
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
        clear()
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
        clear()
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
        clear()
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
        clear()
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
#======================================Create an Occurence=================================================#

def createoccurence(client,email,name):
    while 1:
        clear()
        print(f'\nHello {name},')
        print('\n   >> Registo de Ocorrências \n')
        opt =input(' 1) Registo \n 2) Exit \n')
        if opt == '1':
            send(opt,client)
            occurenceclient(client, email, name)
            #continue
            return
        elif opt == '2':
            send(opt,client)
            break


def occurenceclient(client,email,name):
    valid_date = False
    valid_time = False 
    valid_local = False 
    valid_description = False 
    while 1:
        try:
            clear()
            print(f'\nHello {name},')
            print('\n   >> Registo de Ocorrências \n')
            opt = input(' 1) Registo da data \n 2) Registo da hora\n 3) Registo da Localidade\n 4) Descrição da Ocorrência\n 5) Submeter Ocorrência  \n 6) Exit \n')
            if opt == '1':
                send(opt,client)
                input_date = input("Data (formato: YYYY-MM-DD) :\n ")
                try:
                    date2 = datetime.datetime.strptime(input_date, "%Y-%m-%d")             
                    current_date = datetime.datetime.now()
                    diff = relativedelta(current_date, date2).years
                    if diff>100 or date2>current_date:
                        raise ValueError()
                    valid_date = True
                    send(input_date,client)
                    result = input("Data guardada\n Prima qualquer tecla para voltar atrás\n")
                    continue 
                
                except:                    
                    result = input("O formato da data está errado. Deverá ser YYYY-MM-DD e o ano dado deverá ser válido\n Prima qualquer tecla para voltar atrás\n")
                    send('False',client)
                    valid_date = False
                    continue;
            elif opt == '2':
                send(opt,client)
                time_string = input("Hora (formato: HH:MM) :\n ")
                try:
                    time.strptime(time_string, '%H:%M')
                    valid_time = True
                    send(time_string,client)
                    result = input("Hora guardada\n Prima qualquer tecla para voltar atrás\n")
                    continue
                except:
                    result = input("O formato da hora está errado. Deverá ser HH:MM\n Prima qualquer tecla para voltar atrás\n")
                    send('False',client)
                    valid_time = False         
                    continue
            elif opt == '3':
                send(opt,client) 
                local = input("Local da ocorrência: \n")
                result = any(chr.isdigit() for chr in local)
                if result == True:
                    result2 = input("A localidade não pode conter números\n Prima qualquer tecla para voltar atrás\n")
                    send('False',client)
                    valid_local = False 
                    continue
                else:
                    result2 = input("Localidade guardada\n Prima qualquer tecla para voltar atrás\n")
                    valid_local = True 
                    send(local,client)
                    continue
            elif opt == '4':
                send(opt,client)
                description = input("Faça a descrição da ocorrência com o máximo de detalhes possíveis. Prima \"Enter\" para finalizar a descrição:\n")
                while 1:
                    result = input("Pretende manter esta descrição:\n" + description + "\n 1) Sim \n 2) Não\n")
                    if result == '1':
                        send(result,client)
                        result2 = input("Descrição guardada\n Prima qualquer tecla para voltar atrás\n")
                        valid_description = True
                        send(description,client)
                        break
                    elif result =='2':
                        send(result,client)
                        result2 = input("A descrição será eliminada\n Prima qualquer tecla para voltar atrás\n")
                        valid_description = False
                        send('False',client)
                        break
                    
            elif opt == '5':
                send(opt,client)
                while 1:
                    result = input("Pretende submeter a ocorrencia em modo anónimo?\n 1) Sim\n 2) Não\n")
                    
                    if result == '1':
                        send(result,client)                          
                        while read(client)!='True':
                            continue
                        break
                    elif result == '2':
                        send(result,client)
                        while read(client)!='True':
                            continue
                        break   
                    else: 
                        continue   

                if(valid_date==False or valid_time==False or valid_local==False or valid_description==False): 
                    send('False',client) 
                    print(" Ainda tem campos por preencher. Por favor preencha os seguintes campos para submeter a ocorrência:\n")
                    if valid_date == False:
                        print("->Data\n")
                    if valid_time == False:
                        print("->Hora\n") 
                    if valid_local == False:
                        print("->Localidade\n") 
                    if valid_description == False:
                        print("->Descrição\n")
                    result = input(" Prima qualquer teclar para voltar atrás\n")
                    #break
                else:      
                    send('True',client)
                    result=0
                    while result!='1' and result!= '2':
                        result = input("Pretende fazer submissão do seguinte registo? :\n" + "Data: " + str(input_date) + "\n" +
                                        "Hora: " + str(time_string) + "\n" + "Localidade: " + local + "\n" + "Descrição: " + description 
                                        + "\n 1) Sim \n 2) Não\n")        
                        if result == '1':
                            send(result,client)
                            result1 = input("Submissão feita\n Prima qualquer tecla para sair\n")
                            send('True', client)
                            return               
                        elif result =='2':
                            send(result,client)
                            result1= input("O registo não foi submetido.\n Prima qualquer tecla para voltar atrás\n")
                            #send('False',client)
                            break
            elif opt == '6':
                send(opt,client)
                break
        except Exception as e:
            print(e)
           


#==========================================Signup==========================================================#
def signup(client):
    clear()
    while 1:
        
        print('\nSignup Health Professional')
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
            clear();
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
    





