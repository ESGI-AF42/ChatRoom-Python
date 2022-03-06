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

user_list=User.load_user_from_csv()# récupère la liste de tous les utilisateurs qui se sont une fois connecté

def main():
    while True:
        client, address = MySocket.accept()
        print("Connecté avec " + str(address))
        #Demander au client son pseudo
        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
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
            client.send('BAN'.encode('utf-8'))
            client.close()
            continue
        
        # Si le client à un pseudo ayant un status, un mot de passe lui sera demandé
        #s'il a le bon mot de passe il se connecte en tant qu'admin et peut donc avoir plus de privilèges 
        if status == 'admin':
            client.send('PASS'.encode('utf-8'))
            password = client.recv(1024).decode('utf-8')
            if password != 'adminpass': #mot de passe pour donner un exemple, pourrait être implémenté dans le fichier user csv
                                        #par manque de temps ce n'est pas le cas actuellement
                client.send('REFUSE'.encode('utf-8'))
                client.close()
                continue

        #ajoute le client et son pseudo dans la liste
        nicknames.append(nickname)
        clients.append(client)

        print("Le pseudo du client est " + nickname )
        phrase = nickname + " a rejoint le chat"
        broadcast( phrase.encode('utf-8'))
        client.send('Connecté sur le serveur! \n(écrivez votre premier message) '.encode('utf-8'))

        # Handling Multiple Clients Simultaneously
        thread = Thread(target=update_chat, args=(client,))
        thread.start()


#thread permettant de traiter les informations recues par les clients
def update_chat(client):
    while True:
        try:
            msg =''
            msg = message = client.recv(1024)
            text = msg.decode('utf-8').split(': ')
            #si le message de l'utilisateur commence par KICK et que son pseudo est admin
            if text[1].startswith('KICK'):
                if nicknames[clients.index(client)] == 'admin':
                    name_to_kick = text[1][5:]
                    if name_to_kick in nicknames:
                        kick_user(name_to_kick)
                    else:
                        client.send('L utilisateur n est pas connecté'.encode('utf-8'))
                else:
                    client.send('Commande refusée!'.encode('utf-8'))

            #si le message de l'utilisateur commence par BAN et que son pseudo est admin
            elif text[1].startswith('BAN'):
                if nicknames[clients.index(client)] == 'admin':
                    name_to_ban = text[1][4:]
                    for user in user_list:
                        if user.get_user_nickname() == name_to_ban:
                            #si l'utilisateur à bannir est connecté
                            if name_to_ban in nicknames:
                                kick_user(name_to_ban)#il le kick 
                            user.change_status("ban")#avant de le bannir
                            break               
                else:
                    client.send('Command Refused!'.encode('utf-8'))
            else:
                
                broadcast(message)   # dès que le message est reçu, il est retourné
        
        except:
            if client in clients:
                #permet de retirer le client de la liste lorsqu'il quitte la room
                index = clients.index(client)  
                clients.remove(client)
                client.close()
                nickname = nicknames[index]
                leave_server_phrase = nickname + " à quitté le chat"
                broadcast(leave_server_phrase.encode('utf-8'))
                nicknames.remove(nickname)
                break

#renvoi les messages recues à tous les clients
def broadcast(message):
    for client in clients:
        client.send(message)

#procédure pour kick un utilisateur
def kick_user(name):
    name_index = nicknames.index(name)
    client_to_kick = clients[name_index]
    clients.remove(client_to_kick)#retire le client à kick de la liste actuel des clients
    client_to_kick.send('Vous avez été kick de la room !'.encode('utf-8'))
    client_to_kick.close()#ferme la connection avec le client
    nicknames.remove(name)#retire le surnom du client à kick de la liste actuel des surnoms
    kick_server_phrase = name + " a été kick du serveur!"
    broadcast(kick_server_phrase.encode('utf-8'))#préviens tous les utilisateurs que le client a été kick


#appelle de la méthode main
print('Server is Listening ...')
main()
