import threading
import socket
# Now this Host is the IP address of the Server, over which it is running.
# I've user my localhost.

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5002 # Choose any random port which is not so common (like 80)

# initialize list/set of all connected client's sockets
client_sockets = set()
# create a TCP socket
s = socket.socket()
# make the port as reusable port
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# bind the socket to the address we specified
s.bind((SERVER_HOST, SERVER_PORT))
#Start Listening Mode
s.listen()
#List to contain the Clients getting connected and nicknames
clients = []
nicknames = []

# 1.Broadcasting Method
def broadcast(message):
    for client in clients:
        client.send(message)

# 2.Recieving Messages from client then broadcasting
def handle(client):
    while True:
        try:
            msg = message = client.recv(1024)  
            broadcast(message)   # As soon as message recieved, broadcast it.
        except:
            if client in clients:
                index = clients.index(client)
                #Index is used to remove client from list after getting diconnected
                client.remove(client)
                client.close
                nickname = nicknames[index]
                broadcast(f'{nickname} left the Chat!'.encode('ascii'))
                nicknames.remove(nickname)
                break
            
# Main Recieve method
def recieve():
    while True:
        client, address = s.accept()
        print(f"Connected with {str(address)}")
        nickname = client.recv(1024).decode('ascii')
        
        nicknames.append(nickname)
        clients.append(client)

        print(f'Nickname of the client is {nickname}')
        broadcast(f'{nickname} joined the Chat'.encode('ascii'))
        client.send('Connected to the Server!'.encode('ascii'))

        # Handling Multiple Clients Simultaneously
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

#Calling the main method
print('Server is Listening ...')
recieve()
