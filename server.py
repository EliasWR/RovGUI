## SERVER/ HOST COMMUNICATION SIDE, RASPBERRY PI

import socket
import threading    # Might not need for my usage
import pickle

# Server needs to decide which IP address and port
# should be utilized for the communication

HEADER = 64     # Gives how many bytes that should be received
HOST = socket.gethostbyname(socket.gethostname())
PORT = 5050
ADDR = (HOST, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "Disconnect!"

# Binding a socket to my IP address and PORT
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        # msg_length = conn.recv(HEADER).decode(FORMAT)
        try:
            msg_length = pickle.loads(conn.recv(HEADER))
        except:
            continue

        if msg_length:
            print(f'msg length = {msg_length}')
            msg_length = int(msg_length)
            msg = pickle.loads(conn.recv(msg_length))
            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f"[{addr}] {msg}")
    
    conn.close()





def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {HOST}")
    while True:
        conn, addr  = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count()-1}")
    

print("[STARTING] Server is starting...")
start()

