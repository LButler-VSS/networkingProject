import socket
import os
import tqdm
import threading

# Relevant variables. Would likely need to be asked as input from user for modality
SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096
host = "10.50.109.10"
port = 5001
filename = "data.csv"
filesize = os.path.getsize(filename)

# Sends a file to the server
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
                break
            # we use sendall to assure transimission in 
            # busy networks
            s.sendall(bytes_read)
            # update the progress bar
            progress.update(len(bytes_read  ))

# Checks if a file with a name and filesize exists on the server.
def recvMessage(filename, filesize, s):
    s.send(f"checkingfile{SEPARATOR}{filename}{SEPARATOR}{filesize}".encode())

    msg = s.recv(BUFFER_SIZE)
    print(msg.decode())

# These are functions designed to facilitate threading of the server calls
# Changes to the server would be required to get threading to work.
def callSendFile():
    t1 = threading.Thread(target=sendFile, args=(filename, filesize, s))
    t1.start()
    t1.join()

def callRecvMessage():
    t2 = threading.Thread(target=recvMessage, args=(s,))
    t2.start()
    t2.join()

# Main program loop
while True:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Ask user for task
    print("\nWhat would you like to do?")
    print("1. Send File")
    print("2. Check if file has been sent already")
    print("3. Send server a message")
    print("6. Disconnect from server")
    print("?. Any other key will shutdown server and exit program")
    operation = input("\nEnter the number of the action you would like to take: ")
    
    # Connect to server
    print(f"[+] Connecting to {host}:{port}")
    s.connect((host, port))
    print("[+] Connected.")

    # Perform task
    if operation == "1":
        sendFile(filename, filesize, s)
    elif operation == "2":
        recvMessage(filename, filesize, s)
    elif operation == "3":
        msg = input("\nEnter your message: ")
        s.send(f"printmessage{SEPARATOR}{msg}{SEPARATOR} ".encode())
    elif operation == "6":
        s.send(f"end{SEPARATOR}1{SEPARATOR}1".encode())
        break
    else:
        s.send(f"continue{SEPARATOR}1{SEPARATOR}1".encode())
        break
    # Disconnect from server
    print("\n[-] Disconnected from server successfully.")
    s.close()

# close the socket
s.close()
print("[-] Disconnected from server successfully. Closing Program")