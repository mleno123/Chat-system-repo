from socket import AF_INET, SOCK_STREAM, socket
from threading import Thread

from server import Connection

FORMAT = 'utf-8'
CHAT_EXIT = "EXIT"
BUFSZE = 512


def recv_msg(sock):
    while True:
        msg = sock.recv(BUFSZE).decode(FORMAT)
        print(msg)


def main():
    connection = Connection()
    ADDR = (connection.server, connection.port)

    with (socket(AF_INET, SOCK_STREAM)) as sock:
        sock.connect(ADDR)
        print(f'Connected to {ADDR}')

        connected = True
        thread = Thread(target=recv_msg, args=(sock,))
        thread.start()

        while connected:
            msg = input()
            sock.sendall(msg.encode(FORMAT))


if __name__ == "__main__":
    main()
