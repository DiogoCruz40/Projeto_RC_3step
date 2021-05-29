from threading import local
import System_Manager 
import Security_Officer 
import Health_Professional 
from os import system
clear = lambda: system('clear')


def Show_client_help():
    try:
        clear()
        print(' Ola!\n')
        print(' Neste menu vais ter de escolher que tipo de utilizador és.')
        print(' Se és um Profissional de Saúde seleciona a opção “1”.\n Caso sejas um Agente de Segurança seleciona a opção “2”.\n No caso de seres um Gestor de Sistema seleciona a opção “3”.\n Em qualquer uma destas opções vais ser redirecionado para\n a aplicação correspondente à tua profissão.\n')
        print(' Para sair prime a opção 5.\n')
        print(' Obrigado!')
        input(' \n Press any key to continue...')
    except Exception as e:
        print(e)   

if __name__ == "__main__":
    while 1:
        try:
            clear()
            opt = input('Sistema de ocorrencias\n 1) Health Professional\n 2) Security Officer\n 3) System Manager\n 4) Help\n 5) Exit\n Select: ')
            if opt == '1':
               Health_Professional.main()
            if opt == '2':
                Security_Officer.main()
            if opt == '3':
                System_Manager.main()
            if opt == '4':
                Show_client_help()
            if opt == '5':
                exit(1)
        except Exception as e:
            print(e)
