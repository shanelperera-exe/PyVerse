from socket import *

HOST = "127.0.0.1"  # This is the standard loopback interface address (localhost)
PORT = 2000  # Defines the port to listen on

s = socket(AF_INET, SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()
print('The server is ready to receive')
while (True):
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            print('Received message ', data, ' from host ',addr)
            modifiedMessage = data.decode().upper()
            if not data:
                break
            print('Sending reply',modifiedMessage)
            conn.sendall(modifiedMessage.encode())
