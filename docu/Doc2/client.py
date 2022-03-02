import socket
import threading

nickname = input("Choose Your Nickname:")
if nickname == 'admin':
    password = input("Enter Password for Admin:")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Connect to a host
client.connect(('127.0.0.1',5002))

stop_thread = False

def recieve():
    while True:
        global stop_thread
        if stop_thread:
            break    
        try:
            message = client.recv(1024).decode('ascii')
            print(message)
        except:
            print('Error Occured while Connecting')
            client.close()
            break
        
def write():
    while True:
        if stop_thread:
            break
        #Getting Messages
        message = f'{nickname}: {input("")}'
        client.send(message.encode('ascii'))

recieve_thread = threading.Thread(target=recieve)
recieve_thread.start()
write_thread = threading.Thread(target=write)
write_thread.start()
