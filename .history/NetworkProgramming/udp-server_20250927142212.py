from socket import *

def dd_to_int(dd: str) -> int:
    """Convert dotted decimal IP to 32-bit integer."""
    parts = list(map(int, dd.split(".")))
    return (parts[0] << 24) | (parts[1] << 16) | (parts[2] << 8) | parts[3]

def int_to_dd(num: int) -> str:
    """Convert 32-bit integer to dotted decimal IP."""
    return ".".join(str((num >> (i * 8)) & 0xFF) for i in reversed(range(4)))

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

