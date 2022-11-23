import socket
import threading

from server import Connection

FORMAT = 'utf-8'
CHAT_EXIT = "EXIT"

def recv_msg(sock):
    while True:
        msg = sock.recv(1024).decode(FORMAT)
        print(msg)
    
    

def main():
    connection = Connection()
    ADDR = (connection.server, connection.port)

    with (socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        sock.connect(ADDR)
        print(f'Connected to {ADDR}')

        connected = True
        thread = threading.Thread(target=recv_msg, args=(sock,), daemon=True)
        thread.start()

        while connected:
            msg = input("> ")
            sock.sendall(msg.encode(FORMAT))
            

if __name__ == "__main__":
    main()
