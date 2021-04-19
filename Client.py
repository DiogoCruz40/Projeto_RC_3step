import System_Manager 
import Security_Officer 
import Health_Professional 


if __name__ == "__main__":
    while 1:
        try:
            opt = input('SELECT:\n 1) Health Professional\n 2) Security Officer\n 3) System Manager\n 4) Exit\n Select: ')
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

