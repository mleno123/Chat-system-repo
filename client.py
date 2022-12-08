import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog
from socket import AF_INET, SOCK_STREAM, socket
from threading import Thread

from server import Connection

FORMAT = 'utf-8'
CHAT_EXIT = "exit"
BUFSZE = 512


class Client:
    def __init__(self, sock) -> None:
        self.sock = sock
        msg = tkinter.Tk()
        msg.withdraw()

        self.nickname = simpledialog.askstring("Name", "Please enter name", parent=msg)
        self.gui_done = False
        self.running = True

        gui_thread = Thread(target=self.gui_loop, daemon=True)
        rcv_thread = Thread(target=self.receive_loop, daemon=True)

        gui_thread.start()
        rcv_thread.start()

        gui_thread.join()

        
    def gui_loop(self):
        self.win = tkinter.Tk()
        self.win.configure(bg="lightgray")

        self.chat_label = tkinter.Label(self.win, text="Chat:", bg="lightgray")
        self.chat_label.config(font=("Arial", 12))
        self.chat_label.pack(padx=20, pady=5)

        self.text_area = tkinter.scrolledtext.ScrolledText(self.win)
        self.text_area.pack(padx=20, pady=5)
        self.text_area.config(state="disabled")

        self.msg_label = tkinter.Label(self.win, text="Chat:", bg="lightgray")
        self.msg_label.config(font=("Arial", 12))
        self.msg_label.pack(padx=20, pady=5)

        self.input_area = tkinter.Text(self.win, height=3)
        self.input_area.pack(padx=20, pady=5)

        self.send_button = tkinter.Button(self.win, text="Send", command=self.write_loop)
        self.send_button.config(font=("Arial", 12))
        self.send_button.pack(padx=20, pady=5)
        self.win.bind("<Return>", self.write)

        self.gui_done = True
        self.win.protocol("WM_DELETE_WINDOW", self.stop)
        self.win.mainloop()

    def write(self, event):
        message = f"{self.input_area.get('1.0', 'end')}".strip().__add__("\n")
        self.sock.send(message.encode(FORMAT))
        self.input_area.delete('1.0', 'end')

    def write_loop(self):
        message = f"{self.input_area.get('1.0', 'end')}"
        self.sock.send(message.encode(FORMAT))
        self.input_area.delete('1.0', 'end')

    def stop(self):
        self.running = False
        self.win.destroy()
        self.sock.send(CHAT_EXIT.encode(FORMAT))
        self.sock.close()

    def receive_loop(self):
        while self.running:
            try:
                msg = self.sock.recv(BUFSZE).decode(FORMAT)
                if msg == "name":
                    self.sock.sendall(self.nickname.encode(FORMAT))
                elif msg == "exit":
                    break
                else:
                    if self.gui_done:
                        self.text_area.config(state="normal")
                        self.text_area.insert("end", msg)
                        self.text_area.yview("end")
                        self.text_area.config(state="disabled")
            except:
                print("[ERROR] error in the receive_loop function")
                break
        
        self.stop()
        

def main():
    connection = Connection()
    ADDR = (connection.server, connection.port)

    with (socket(AF_INET, SOCK_STREAM)) as sock:
        sock.connect(ADDR)
        client = Client(sock)

    exit()

if __name__ == "__main__":
    main()
