import socket
from threading import Thread


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

Users = dict()# Dictionnaire de donnée contenant les différent clients avec leur pseudo

