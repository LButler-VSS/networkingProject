import socket
import tqdm
import os
import threading

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5001

BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((SERVER_HOST, SERVER_PORT))

s.listen(5)
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

client_socket, address = s.accept() 

print(f"[+] {address} is connected.")
def recvFile(client_socket, list):
    received = client_socket.recv(BUFFER_SIZE).decode()
    filename, filesize = received.split(SEPARATOR)
    filename = os.path.basename(filename)
    filesize = int(filesize)
    list[0] = filename
    list[1] = filesize

    progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "wb") as f:
        
        while True:
            # read 1024 bytes from the socket (receive)
            bytes_read = client_socket.recv(BUFFER_SIZE)
            if not bytes_read:    
                # nothing is received
                # file transmitting is done
                break
            # write to the file the bytes we just received
            f.write(bytes_read)
            # update the progress bar
            progress.update(len(bytes_read))

def sendMessage(client_socket, list):
    if os.path.getsize(list[0]) == list[1]:
        client_socket.send(f"The program encountered an error transferring the file. Please try again.".encode())
    else:
        client_socket.send(f"Transfer of file {list[0]} was completed succesfully.".encode())

list = ["", 0]
t1 = threading.Thread(target=recvFile, args=(client_socket,list))
t1.start()
t1.join()

t2 = threading.Thread(target=sendMessage, args=(client_socket,list))
t2.start()
t2.join()

# close the client socket
client_socket.close()
# close the server socket
s.close()