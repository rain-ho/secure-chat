# server.py
import socket
import threading
import os
from dotenv import load_dotenv

load_dotenv()



def load_censored_words():
    # Load the words to be censored from a txt file
    with open("censored_words.txt", "r") as f:
        censored_words = set(f.read().splitlines())
    return censored_words

def censor_words(message, censored_words):
    # Replace censored words in the message
    words = message.split()
    censored_message = " ".join("*" * len(word) if word.upper() in censored_words else word for word in words)
    return censored_message

clients = {}  # Dictionary to store connected clients and their sockets

def handle_client(client_socket, address, censored_words):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            censored_message = censor_words(message, censored_words)
            print(f"Received from {address}: {message}")
            print(f"Censored: {censored_message}")

            # Send the censored message to the other client
            for client, socket in clients.items():
                if socket != client_socket:
                    socket.send(censored_message.encode())

        except:
            break

    # Remove the client from the dictionary when the connection is closed
    del clients[client_socket]
    client_socket.close()

def main():
    server_ip = os.getenv("YOUR_SERVER_IP")
    server_port = os.getenv("YOUR_SERVER_PORT")

    censored_words = load_censored_words()
    print (censored_words)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_ip, server_port))
    server_socket.listen(2)  # Maximum number of clients to handle simultaneously

    print(f"Server listening on {server_ip}:{server_port}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address[0]}:{client_address[1]}")

        # Add the client socket to the dictionary
        clients[client_socket] = client_socket

        # Start a separate thread to handle each client
        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address, censored_words))
        client_handler.start()

if __name__ == "__main__":
    main()
