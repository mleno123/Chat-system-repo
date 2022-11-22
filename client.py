import socket
import argparse
import sys

FORMAT = 'utf-8'
CHAT_EXIT = "EXIT"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('ip', help="Number 1")
    parser.add_argument('portNumber', help="Number 2", type=int)
    args = parser.parse_args()

    PORT = args.portNumber

    try:
        SERVER = socket.gethostbyname(args.ip)
    except socket.gaierror as x:
        sys.stderr.write("ERROR: " + str(x) + "\n")
        sys.exit(1)

    ADDR = (SERVER, PORT)

    with(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        try:
            sock.settimeout(10)
            sock.connect(ADDR)
            
            msg = sock.recv(1024).decode(FORMAT)
            if msg != "cleared":
                sock.close()
                
            sock.settimeout(240)

            connected = True
            while connected:
                send_msg = input().encode(FORMAT)
                sock.sendall(send_msg)

                if send_msg == CHAT_EXIT:
                    connected = False
                    
                # recv_msg = sock.recv(1024).decode(FORMAT)
                # print(recv_msg)
        
        
        except OverflowError as port:
            sys.stderr.write("ERROR: " + str(port) + "\n")
            sock.close()
            sys.exit(1)
        except socket.timeout as x:
            sys.stderr.write("ERROR: " + str(x) + "\n")
            sock.close()
            sys.exit(1)
        except socket.error as e:
            sys.stderr.write("ERROR: " + str(e) + "\n")
            sock.close()
            sys.exit(1)
        



if __name__ == "__main__":
    main()
