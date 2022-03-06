from pickle import TRUE
import socket
from sqlite3 import connect
import threading
from threading import Thread
from datetime import datetime
# from colorama import Fore, init, Back
import random


 # client_color = choose_color() # c'est inutile oui

# cgoisir une couleur valide
# colors = [Fore.BLUE, Fore.CYAN, Fore.GREEN, Fore.LIGHTBLACK_EX, 
#     Fore.LIGHTBLUE_EX, Fore.LIGHTCYAN_EX, Fore.LIGHTGREEN_EX, 
#     Fore.LIGHTMAGENTA_EX, Fore.LIGHTRED_EX, Fore.LIGHTWHITE_EX, 
#     Fore.LIGHTYELLOW_EX, Fore.MAGENTA, Fore.RED, Fore.WHITE, Fore.YELLOW
# ]

# censé chosir une couleur random mais ne fonctioone pas UwU
# client_color = random.choice(colors)

nickname = input("Choisissez votre Pseudo: ")
if nickname == 'admin':
    password = input("Enter Password for Admin:")
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1',5002))

stop_thread = False

# Test connection 
def try_connect():
    a_socket = socket.socket()
    try :
        a_socket.connect(("127.0.0.1", 5002)) # Tente de se connecter à l'adresse IP et au port suivant
        a_socket.shutdown(socket.SHUT_RDWR) # Essaye de se deconnecter du client ? verif que ça marche côté serveur 
        a_socket.close()
    except : 
        print("Le serveur ne répond pas")
        return False 

# fonction pour choisir une couleur affichée dans le chat mais ne fonctionne pas
# def choose_color():
#     test = True
#     colors = [Fore.BLUE, Fore.GREEN, Fore.MAGENTA, Fore.RED, Fore.YELLOW]
#     under_color = ["Bleu", "Vert", "Rose", "Rouge", "Jaune"]
#     print("Choisissez la couleur de votre chat :")
#     print("Avaiable colors : Bleu, Vert, Rose, Rouge, Jaune")
#     client_color = input("Votre choix: ")
#     while test: # Je sais pas pourquoi j'ai fais comme ça mais ça marche 
#         for i in range(len(colors)) :
#             if under_color[i] == client_color :
#                 client_color = colors[i]
#                 test = False
#                 exit
#         if test != False :
#             print("La couleur n'existe pas")
#             client_color = str(input("Votre choix: "))
#     return client_color

def client_connect():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1',5002))


def receive():
    while True:
        global stop_thread
        if stop_thread:
            break    
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'NICK':
                client.send(nickname.encode('utf-8'))
                next_message = client.recv(1024).decode('utf-8')
                if next_message == 'PASS':
                    client.send(password.encode('utf-8'))
                    if client.recv(1024).decode('utf-8') == 'REFUSE':
                        print("Connection is Refused !! Wrong Password")
                        stop_thread = True
                # les clients qui sont bannis ne peuvent pas se reconencter
                elif next_message == 'BAN':
                    print('Connection Refused due to Ban')
                    client.close()
                    stop_thread = True
            else:
                split_message= message.split(': ')
                if split_message[0]!=nickname:
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
        if message[len(nickname)+2:].startswith('/'):
            if nickname == 'admin':
                if message[len(nickname)+2:].startswith('/kick'):
                    # 2 for : and whitespace and 6 for /KICK_
                    client.send(f'KICK {message[len(nickname)+2+6:]}'.encode('utf-8'))
                elif message[len(nickname)+2:].startswith('/ban'):
                    # 2 for : and whitespace and 5 for /BAN
                    client.send(f'BAN {message[len(nickname)+2+5:]}'.encode('utf-8'))
            else:
                print("Commands can be executed by Admins only !!")
        else:
            client.send(message.encode('utf-8'))

recieve_thread = threading.Thread(target=receive)
recieve_thread.start()
write_thread = threading.Thread(target=write)
write_thread.start()


    


