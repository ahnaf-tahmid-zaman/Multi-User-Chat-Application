import socket
import threading

# Create a socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the server's host and port
server_host = '192.168.0.9'  # Replace with the server's IP address
server_port = 12345

# Connect to the server
client.connect((server_host, server_port))

# Function to receive and display messages from the server
def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            print(message)
        except:
            print("Connection closed.")
            client.close()
            break

# Create a thread to receive messages
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

# Main loop for sending messages
while True:
    message = input()
    client.send(message.encode('utf-8'))

