import threading
import socket


# define your host, if you want to host on your local computer, use local host
host = "127.0.0.1"    # local host

# define the port that you want to use
# pick a port outside the reserved ports
port = 55555


# create a TCP socket connection
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind this server to your host:port
server.bind((host,port))

# make your server to listen for the incoming connection
server.listen()


clients = []
nicknames = []

###### broadcast method
def broadcast(message):
    for client in clients:
        client.send(message)

###### handle method
def handle(client):
    while True:
        try:
            # receive the message that our client sends
            message = client.recv(1024)

            # broadcast the message to the rest of clients
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            broadcast(f'{nickname} left the chat!'.encode("ascii"))
            break


###### receive method
def receive():
    while True:
        client, address = server.accept()
        print(f"connected with {str(address)}")

        client.send("NICK".encode("ascii"))
        nickname = client.recv(1024).decode("ascii")
        nicknames.append(nickname)
        clients.append(client)

        print(f'Nickname of the client is {nickname}')
        broadcast(f'{nickname} joined the chat \n'.encode("ascii"))

        client.send("Connected to the server".encode("ascii"))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


# run the main method: receive 
print("The server is listening ...")
receive()