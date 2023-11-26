import tkinter as tk
from tkinter import scrolledtext
import threading
import socket
import re
import webbrowser

# Create a socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the server's host and port
server_host = '192.168.0.9'  # Change this to the server's IP or hostname
server_port = 12345

# Connect to the server
client.connect((server_host, server_port))

# Function to send a message
def send_message():
    message = message_entry.get()
    client.send(message.encode('utf-8'))
    message_entry.delete(0, tk.END)
    display_message("You", message)

# Function to receive and display messages from the server
def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            display_message("", message)  # Removed "Server" label
        except:
            print("Connection closed.")
            client.close()
            break

# Function to handle Enter key press
def on_enter(event):
    send_message()

# Function to display messages in the chat window
def display_message(sender, message):
    chat_text.config(state=tk.NORMAL)
    formatted_message = f"{sender}: {message}\n" if sender else f"{message}\n"
    chat_text.insert(tk.END, formatted_message)

    # Check for URLs in the message and make them clickable
    urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message)
    for url in urls:
        chat_text.tag_configure('link', foreground='blue', underline=True)
        chat_text.insert(tk.END, url, 'link')
        chat_text.tag_bind('link', '<Button-1>', lambda e, url=url: open_browser(url))
        chat_text.insert(tk.END, " ")

    chat_text.config(state=tk.DISABLED)

# Function to open the URL in the default web browser
def open_browser(url):
    webbrowser.open(url)

# Create a GUI for the client
client_gui = tk.Tk()
client_gui.title("Chat Client")

chat_text = scrolledtext.ScrolledText(client_gui, wrap=tk.WORD)
chat_text.config(state=tk.DISABLED)
chat_text.pack()

message_entry = tk.Entry(client_gui)
message_entry.pack()

send_button = tk.Button(client_gui, text="Send", command=send_message)
send_button.pack()

# Bind the Enter key to the send_message function
client_gui.bind('<Return>', on_enter)

# Create a thread to receive messages
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

# Main GUI loop
client_gui.mainloop()

