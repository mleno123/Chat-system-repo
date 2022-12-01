from socket import AF_INET, SOCK_STREAM, socket
from threading import Thread
from person import Person

FORMAT = 'utf-8'
CHAT_EXIT = "EXIT"
BUFSZE = 512

CLIENTS = []


class Connection():
    def __init__(self) -> None:
        self.server = 'localhost'
        self.port = 5050


def client_recv(person):
    client = person.client
    while True:
        msg = client.recv(BUFSZE).decode(FORMAT)

        if not msg or msg == CHAT_EXIT:
            CLIENTS.remove(person)
            client.close()
            send_all_clients(f"{person.name} has left the chat")
            break
            
        send_all_clients(f"{person.name}: {msg}")

def get_name(client):
    client.send("Enter name for the chat: ".encode(FORMAT))
    msg = client.recv(BUFSZE).decode(FORMAT)

    if not msg:
        client.send("Invalid username.. EXITING".encode(FORMAT))
        client.close()
    else:
        return msg

def handle_client(client, address):
    name = get_name(client)
    person = Person(client=client, addr=address, name=name)

    CLIENTS.append(person)

    send_all_clients(f"{person.name} has joined the chat\n")
    client.send("To exit chat, type EXIT\n".encode(FORMAT))

    thread_recv = Thread(target=client_recv, args=(person,))
    thread_recv.start()


def send_all_clients(msg):
    for person in CLIENTS:
        client = person.client
        client.send(msg.encode(FORMAT))


def main():
    connection = Connection()
    addr = (connection.server, connection.port)

    with (socket(AF_INET, SOCK_STREAM)) as server:
        print(f"Binding to {addr}")
        server.bind(addr)
        server.listen()
        print(f"listening on {addr}")

        while True:
            client, address = server.accept()
            handle_client(client, address)


if __name__ == "__main__":
    main()
