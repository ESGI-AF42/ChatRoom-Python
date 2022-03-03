import socket
from threading import Thread
from user import User


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

#initialisation des listes permettant l'identification des différents clients dans le chat bot
clients = list()#list de clients connectés
nicknames = list()# list des pseudos connectés

user_list=User.load_user_from_csv("ouioui")# récupère la liste de tous les utilisateurs qui se sont une fois connecté

def main():
    while True:
        client, address = MySocket.accept()
        print("Connected with " + str(address))
        #Demander au client son pseudo
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        #status par défaut (dans le cas où ce serait la première connection de l'utilisateur)
        status = "member"

        # vérifie si le client s'est déjà connecté ainsi que son status
        # si ce n'est pas le cas il le cré 
        for user in user_list:
            if user.get_user_nickname() == nickname:
                status = user.get_user_status()
            
            else:
                NewUser=User(nickname,status)
                NewUser.save_user()
        
        # Si le client à un pseudo ayant un status ban il sera déconnecté
        if status == "ban":
            client.send('BAN'.encode('ascii'))
            client.close()
            continue
        
        # Si le client à un pseudo ayant un status, un mot de passe lui sera demandé
        #s'il a le bon mot de passe il se connecte en tant qu'admin et peut donc avoir plus de privilèges 
        if status == 'admin':
            client.send('PASS'.encode('ascii'))
            password = client.recv(1024).decode('ascii')
            if password != 'adminpass': #mot de passe pour donner un exemple, pourrait être implémenté dans le fichier user csv
                                        #par manque de temps ce n'est pas le cas actuellement
                client.send('REFUSE'.encode('ascii'))
                client.close()
                continue

        nicknames.append(nickname)
        clients.append(client)

        print("Le pseudo du client est " + nickname )
        broadcast( nickname + " à rejoind le chat".encode('ascii'))
        client.send('Connecté sur le serveur!'.encode('ascii'))

        # Handling Multiple Clients Simultaneously
        thread = Thread(target=update_chat, args=(client))
        thread.start()


def update_chat(client):
    while True:
        try:
            msg = message = client.recv(1024) 

            if msg.decode('ascii').startswith('KICK'):
                if nicknames[clients.index(client)] == 'admin':
                    name_to_kick = msg.decode('ascii')[5:]
                    if name_to_ban in nickname:
                        kick_user(name_to_kick)
                    else:
                        client.send('L\'utilisateur n\'est pas connecté'.encode('ascii'))
                else:
                    client.send('Commande refusée!'.encode('ascii'))

            elif msg.decode('ascii').startswith('BAN'):
                if nicknames[clients.index(client)] == 'admin':
                    name_to_ban = msg.decode('ascii')[4:]
                    for user in user_list:
                        if user.get_user_nickame() == name_to_ban:
                            if name_to_ban in nickname:
                               kick_user(name_to_ban)
                            user.change_status("ban")               
                else:
                    client.send('Command Refused!'.encode('ascii'))
            else:
                broadcast(message)   # dès que le message est reçu, il est retourné
        
        except:
            if client in clients:
                #permet de retirer le client de la liste lorsqu'il quitte la room
                index = clients.index(client)  
                client.remove(client)
                client.close
                nickname = nicknames[index]
                broadcast(nickname + " à quitté le chat".encode('ascii'))
                nicknames.remove(nickname)
                break


def broadcast(message):
    for client in clients:
        client.send(message)




def kick_user(name):
    if name in nicknames:
        name_index = nicknames.index(name)
        client_to_kick = clients[name_index]
        clients.remove(client_to_kick)
        client_to_kick.send('Vous avez été kick de la room !'.encode('ascii'))
        client_to_kick.close()
        nicknames.remove(name)
        broadcast(name + " was kicked from the server!".encode('ascii'))


#Calling the main method
print('Server is Listening ...')
main()
