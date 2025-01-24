from socket import socket as Socket, AF_INET, SOCK_STREAM
from threading import Thread

HOST, PORT = "localhost", 8080
BUFFSIZE = 1024
ENCODING = "utf-8"

client = Socket(AF_INET, SOCK_STREAM)
client.connect((HOST, PORT))

running = True

def listen() -> None:
    global running
    empty_msgs_count = 0
    while running:
        try:
            msg = client.recv(BUFFSIZE).decode(ENCODING)
        except Exception as e:
            print(f"[ERROR] {e}")
            break
        else:
            if len(msg) == 0:
                empty_msgs_count += 1
                print(f"Received {empty_msgs_count} empty messages consecutively", end='\r')
            else:
                empty_msgs_count = 0
                print("\nServer:", msg)
    
    client.close()

def main() -> None:
    global running
    listener_thread = Thread(target=listen)
    listener_thread.start()

    while running:
        try:
            msg = input("> ")
        except KeyboardInterrupt:
            running = False
        else:
            result = client.send(msg.encode(ENCODING))
            print(f"Sent {result} bytes.")

if __name__ == "__main__":
    main()
