import socket


HEADER = 64
PORT = 5050
FORMAT = 'utf-8' 
DISCONNECT_MSG = '!DISCONNECT'
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def read():      
    msg_length = client.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        msg = client.recv(msg_length).decode(FORMAT)
    return msg 

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length)) #PADDING
    client.send(send_length)
    client.send(message)



print(read()) #Read People Menu
opt = input('USER:')
# send(opt) # Send person to talk to
# opt = input('Password: ')
# send(opt) #Send content
# print(read()) #Job
send(DISCONNECT_MSG)





