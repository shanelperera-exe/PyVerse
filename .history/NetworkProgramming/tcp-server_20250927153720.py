from socket import *

# Helper functions
def dd_to_int(dd: str) -> int:
    """Convert dotted decimal IP to 32-bit integer."""
    parts = list(map(int, dd.split(".")))
    return (parts[0] << 24) | (parts[1] << 16) | (parts[2] << 8) | parts[3]

def int_to_dd(num: int) -> str:
    """Convert 32-bit integer to dotted decimal IP."""
    return ".".join(str((num >> (i * 8)) & 0xFF) for i in reversed(range(4)))

def address_calc(cidr: str) -> str:
    """Do the address calculations and return the answer as a string."""
    ip_str, prefix_str = cidr.split("/")
    prefix = int(prefix_str)
    ip_int = dd_to_int(ip_str)

    # Netmask
    netmask_int = ((1 << 32) - 1) ^ ((1 << (32 - prefix)) - 1)
    netmask_dd = int_to_dd(netmask_int)

    # Network & Broadcast
    network_int = ip_int & netmask_int
    broadcast_int = network_int | ((1 << (32 - prefix)) - 1)

    network_dd = int_to_dd(network_int)
    broadcast_dd = int_to_dd(broadcast_int)

    # Single or Range
    addr_type = "Single Address" if prefix == 32 else "Range"

    # Address counts
    total_addrs = 1 << (32 - prefix)
    if prefix >= 31:
        usable_addrs = 0
        lowest_dd = highest_dd = "N/A"
    else:
        usable_addrs = total_addrs - 2
        lowest_dd = int_to_dd(network_int + 1)
        highest_dd = int_to_dd(broadcast_int - 1)

    # Build reply
    reply = (
        f"Address/Range: {addr_type}\n"
        f"Netmask: {netmask_dd}\n"
        f"Network address: {network_dd}\n"
        f"Broadcast address: {broadcast_dd}\n"
        f"Total number of addresses: {total_addrs}\n"
        f"Usable number of addresses: {usable_addrs}\n"
        f"Lowest usable address: {lowest_dd}\n"
        f"Highest usable address: {highest_dd}"
    )
    return reply

# TCP server setup
HOST = "127.0.0.1"
PORT = 2000
s = socket(AF_INET, SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()
print('The server is ready to receive')

while True:
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            msg_str = data.decode().strip()
            print('Received message', msg_str, 'from host', addr)

            if "/" in msg_str:
                modifiedMessage = address_calc(msg_str)
            else:
                modifiedMessage = msg_str.upper()

            print('Sending reply:', modifiedMessage, sep='')
            conn.sendall(modifiedMessage.encode())
