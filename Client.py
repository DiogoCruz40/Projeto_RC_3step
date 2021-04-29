import System_Manager 
import Security_Officer 
import Health_Professional 
from os import system
clear = lambda: system('clear')

if __name__ == "__main__":
    while 1:
        clear()
        try:
            opt = input('Sistema de ocorrencias\n 1) Health Professional\n 2) Security Officer\n 3) System Manager\n 4) Exit\n Select: ')
            if opt == '1':
               Health_Professional.main()
            if opt == '2':
                Security_Officer.main()
            if opt == '3':
                System_Manager.main()
            if opt == '4':
                break
        except Exception as e:
            print(e)

