import socket
import threading
import tkinter as tk
from tkinter import simpledialog, scrolledtext

class ChatClient:
    def _init_(self, username):
        self.username = username
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(('localhost', 12345))

        # GUI Setup
        self.window = tk.Tk()
        self.window.title(f"{username}'s Chat")
        self.window.geometry("600x600")  # Set fixed size

        # Background color
        self.window.configure(bg="lightgrey")  # Light grey background

        # Chat window setup with scroll
        self.chat_window = scrolledtext.ScrolledText(self.window, wrap=tk.WORD, state=tk.DISABLED, height=20, width=60)
        self.chat_window.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        self.chat_window.config(bg="white")  # White background for chat window

        # Entry box for message
        self.message_entry = tk.Entry(self.window, width=50, fg='grey')
        self.message_entry.insert(0, "Enter your message...")
        self.message_entry.bind("<FocusIn>", self.clear_placeholder)
        self.message_entry.bind("<FocusOut>", self.add_placeholder)
        self.message_entry.bind("<Return>", self.send_message)
        self.message_entry.pack(pady=5, padx=10, fill=tk.X)

        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.start_client()

    def start_client(self):
        threading.Thread(target=self.receive_messages, daemon=True).start()

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if message:
                    self.display_message(message, received=True)
            except:
                break

    def send_message(self, event=None):
        message = self.message_entry.get()
        if message and message != "Enter your message...":
            self.client_socket.send(f"{self.username}: {message}".encode('utf-8'))
            self.display_message(f"{self.username}: {message}", received=False)
            self.message_entry.delete(0, tk.END)

    def display_message(self, message, received):
        self.chat_window.config(state=tk.NORMAL)

        if received:
            # Align received messages to the left
            self.chat_window.insert(tk.END, message + '\n', 'received')
        else:
            # Align sent messages to the right
            self.chat_window.insert(tk.END, message + '\n', 'sent')

        self.chat_window.yview(tk.END)
        
        # No background colors for text, only alignment
        self.chat_window.tag_config('sent', justify='right', lmargin1=50, lmargin2=50, spacing3=5, spacing2=10)
        self.chat_window.tag_config('received', justify='left', lmargin1=50, lmargin2=50, spacing3=5, spacing2=10)
        
        self.chat_window.config(state=tk.DISABLED)

    def clear_placeholder(self, event=None):
        if self.message_entry.get() == "Enter your message...":
            self.message_entry.delete(0, tk.END)
            self.message_entry.config(fg='black')

    def add_placeholder(self, event=None):
        if self.message_entry.get() == "":
            self.message_entry.insert(0, "Enter your message...")
            self.message_entry.config(fg='grey')

    def on_closing(self):
        self.client_socket.close()
        self.window.destroy()

if __name__ == "_main_":
    username = simpledialog.askstring("Login", "Enter your username:")
    if username:
        ChatClient(username)
    tk.mainloop()
