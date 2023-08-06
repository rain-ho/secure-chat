import socket
import threading
import sys

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            print(f"\nContact: {message}")
        except:
            break
    client_socket.close()

def main():
    if len(sys.argv) != 3:
        print("Usage: python client1.py <server_ip> <server_port>")
        return

    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))

    # Start a separate thread to receive messages from the server
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    while True:
        message = input("You: ")
        client_socket.send(message.encode())

    client_socket.close()

if __name__ == "__main__":
    main()
