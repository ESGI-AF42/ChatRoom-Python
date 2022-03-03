import socket
from threading import Thread
from User import User


# Adresse IP du serveur
HOST = "127.0.0.1"
PORT = 5002 # port du serveur

# initialise une liste de tous les clients connecté au socket
client_sockets = set()
MySocket = socket.socket() #on cré un socket tcp
MySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # on rend le port reutilisable pour que plusieurs clients puisse s'y connecter
MySocket.bind((HOST, PORT))# associe le socket à l'adresse qu'on utilise
MySocket.listen() #le socket est en attente de connection, il y aura maximum 42 connections 
print(f"[*] Listening as {HOST}:{PORT}")

#initialisation des listes et dict permettant l'identification des différents clients dans le chat bot
clients = list()#list de clients connectés
nicknames = dict()# Dictionnaire de donnée contenant les différent pseudo associé à leur client

# 1.Broadcasting Method
def broadcast(message):
    for client in clients:
        client.send(message)

# 2.Recieving Messages from client then broadcasting
def room(client):
    while True:
        try:
            msg = message = client.recv(1024)  
            broadcast(message)   # dès que le message est reçu, il est retourné
        
        except:
            if client in clients:
                #permet de retirer le client de la liste lorsqu'il quitte la room
                index = clients.index(client)  
                client.remove(client)
                client.close
                nickname = nicknames[index]
                broadcast(f'{nickname} left the Chat!'.encode('ascii'))
                nicknames.remove(nickname)
                break
# Main Recieve method
def recieve():
    while True:
        client, address = MySocket.accept()
        print(f"Connected with {str(address)}")
        # Ask the clients for Nicknames
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        # If the Client is an Admin promopt for the password.
        with open('bans.txt', 'r') as f:
            bans = f.readlines()
        
        if nickname+'\n' in bans:
            client.send('BAN'.encode('ascii'))
            client.close()
            continue

        if nickname == 'admin':
            client.send('PASS'.encode('ascii'))
            password = client.recv(1024).decode('ascii')
            # I know it is lame, but my focus is mainly for Chat system and not a Login System
            if password != 'adminpass':
                client.send('REFUSE'.encode('ascii'))
                client.close()
                continue

        nicknames.append(nickname)
        clients.append(client)

        print(f'Nickname of the client is {nickname}')
        broadcast(f'{nickname} joined the Chat'.encode('ascii'))
        client.send('Connected to the Server!'.encode('ascii'))

        # Handling Multiple Clients Simultaneously
        thread = Thread(target=room, args=(client,))
        thread.start()



