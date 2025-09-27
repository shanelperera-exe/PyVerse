from socket import *
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
print('The server is ready to receive')
while True:
    message, clientAddress = serverSocket.recvfrom(2048)
    print('Received message ',message,' from host ',clientAddress)
    modifiedMessage = message.decode().upper()
    print('Sending reply',modifiedMessage)
    serverSocket.sendto(modifiedMessage.encode(),clientAddress)

