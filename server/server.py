import socket
import tqdm
import os

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5001

BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

s = socket.socket()

s.bind((SERVER_HOST, SERVER_PORT))

s.listen(5)
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

client_socket, address = s.accept() 

print(f"[+] {address} is connected.")

received = client_socket.recv(BUFFER_SIZE).decode()
filename, filesize = received.split(SEPARATOR)
filename = os.path.basename(filename)
filesize = int(filesize)

status = True
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
        status = False
        f.write(bytes_read)
        # update the progress bar
        progress.update(len(bytes_read))

if status == True:
    s.send(f"The program encountered an error transferring the file. Please try again.".encode())
else:
    s.send(f"Transfer of file {filename} was completed succesfully.".encode())

# close the client socket
client_socket.close()
# close the server socket
s.close()