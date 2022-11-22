import socket
import argparse
import sys

FORMAT = 'utf-8'
CHAT_EXIT = "EXIT"
SERVER = "0.0.0.0"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('portNumber', help="Number 1", type=int)
    args = parser.parse_args()

    PORT = args.portNumber
    ADDR = (SERVER, PORT)

    with (socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        sock.bind(ADDR)
        sock.listen()

        conn, addr = sock.accept()
        msg = b'cleared'
        conn.send(msg)

        connected = True
        while connected:
            recv_msg = conn.recv(1024).decode()
            if recv_msg == CHAT_EXIT:
                conn.close()
            print(recv_msg)


if __name__ == "__main__":
    main()
