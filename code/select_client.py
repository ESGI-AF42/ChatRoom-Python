from pickle import TRUE
import socket
from sqlite3 import connect
import threading
from threading import Thread
from datetime import datetime
from colorama import Fore, init, Back



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

def choose_nickname():
    nickname = input("Choisissez votre Pseudo: ")
    if nickname == 'admin':
        password = input("Enter Password for Admin:")
        log = [nickname, password]
    else:
        log = [nickname]
    
    return log

def choose_color():
    test = True
    colors = [Fore.BLUE, Fore.GREEN, Fore.MAGENTA, Fore.RED, Fore.YELLOW]
    under_color = ["Bleu", "Vert", "Rose", "Rouge", "Jaune"]
    print("Choisissez la couleur de votre chat :")
    print("Avaiable colors : Bleu, Vert, Rose, Rouge, Jaune")
    client_color = input("Votre choix: ")
    while test: # Je sais pas pourquoi j'ai fais comme ça mais ça marche 
        for i in range(len(colors)) :
            if under_color[i] == client_color :
                client_color = colors[i]
                test = False
                exit
        if test != False :
            print("La couleur n'existe pas")
            client_color = str(input("Votre choix: "))
    return client_color

def client_connect():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1',5002))
    if client:
        print("Connected")
    return client 


def receive(stop_thread, client, nickname, password):
    while True:
        if stop_thread:
            break    
        try:
            message = client.recv(1024).decode()
            if message == 'NICK':
                client.send(nickname)
                next_message = client.recv(1024)
                if next_message == 'PASS':
                    client.send(password)
                    if client.recv(1024) == 'REFUSE':
                        print("Connection is Refused !! Wrong Password")
                        stop_thread = True
                # Clients those are banned can't reconnect
                elif next_message == 'BAN':
                    print('Connection Refused due to Ban')
                    client.close()
                    stop_thread = True
            else:
                print(message)
        except:
            print('Error Occured while Connecting')
            client.close()
            break
        
def write(stop_thread, client, client_color, nickname): 
    while True:
        if stop_thread:
            break
        #Getting Messages
        date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
        message = f'{client_color}[{date_now}]  {nickname}: {input(":")}'
        if message[len(nickname)+2:].startswith('/'):
            if nickname == 'admin':
                if message[len(nickname)+2:].startswith('/kick'):
                    # 2 for : and whitespace and 6 for /KICK_
                    client.send(f'KICK {message[len(nickname)+2+6:]}')
                elif message[len(nickname)+2:].startswith('/ban'):
                    # 2 for : and whitespace and 5 for /BAN
                    client.send(f'BAN {message[len(nickname)+2+5:]}')
            else:
                print("Commands can be executed by Admins only !!")
        else:
            client.send(message)

def main(): # Main program 
    
    connected = True
    try:
        client = client_connect()
    except:
        IndexError
        connected = False
    
    if connected:
        stop_thread = False
        
        log = choose_nickname()
        log_size = len(log) 
        nickname = log[0]
        if log_size > 1:
            password = log[1]
        else:
            password = ""
        client_color = choose_color() # This is useless yes
        recieve_thread = threading.Thread(target=receive, args=(stop_thread, client, client_color, nickname, password))
        recieve_thread.start()
        write_thread = threading.Thread(target=write, args=(stop_thread, client, nickname))
        write_thread.start()
    else:
        print("error connection")
main()


    


