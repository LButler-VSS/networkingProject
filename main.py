import socket
import os
import tqdm
import threading

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096
#10.50.108.146
host = "10.50.108.131"

port = 5001

filename = "data.csv"
filesize = os.path.getsize(filename)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print(f"[+] Connecting to {host}:{port}")
s.connect((host, port))
print("[+] Connected.")

def sendFile(filename, filesize, s):
    # send the filename and filesize
    s.send(f"sendingfile{SEPARATOR}{filename}{SEPARATOR}{filesize}".encode())

    progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "rb") as f:
        while True:
            # read the bytes from the file
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                # file transmitting is done
                s.sendall(bytes_read)
                break
            # we use sendall to assure transimission in 
            # busy networks
            s.sendall(bytes_read)
            # update the progress bar
            progress.update(len(bytes_read  ))

def recvMessage(filename, filesize, s):
    s.send(f"checkingfile{SEPARATOR}{filename}{SEPARATOR}{filesize}".encode())

    msg = s.recv(BUFFER_SIZE)
    print(msg.decode)


def callSendFile():
    t1 = threading.Thread(target=sendFile, args=(filename, filesize, s))
    t1.start()
    t1.join()

def callRecvMessage():
    t2 = threading.Thread(target=recvMessage, args=(s,))
    t2.start()
    t2.join()

while True:
    print("What would you like to do?")
    print("1. Send File")
    print("2. Check if file has been sent already\n")
    print("3. Send server a message")
    operation = input("Enter the number of the action you would like to take, or press any other key to exit: ")
    if operation == "1":
        sendFile(filename, filesize, s)
        s.recv(BUFFER_SIZE)
    elif operation == "2":
        recvMessage(filename, filesize, s)
    elif operation == "3":
        msg = input("\nEnter your message: ")
        s.send(f"printmessage{SEPARATOR}{msg}{SEPARATOR} ".encode())
    else:
        break

# close the socket
s.close()