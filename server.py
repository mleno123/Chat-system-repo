import socket
import threading

FORMAT = 'utf-8'
CHAT_EXIT = "EXIT"


class Connection():
    def __init__(self) -> None:
        self.server = socket.gethostbyname("localhost")
        self.port = 5050

def client_recv(client):
    while True:
        msg = client.recv(1024)
        print(msg.decode(FORMAT))
    
def main():
    connection = Connection()
    addr = (connection.server, connection.port)

    with(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as server:
        print(f"Binding to {addr}")
        server.bind(addr)
        server.listen()
        print(f"listening on {addr}")

        while True:
            client, address = server.accept()
            print(f"{address} has joined the chat")
            thread_recv = threading.Thread(target=client_recv, args=(client,),daemon=True)
            thread_recv.start()

if __name__ == "__main__":
    main()
