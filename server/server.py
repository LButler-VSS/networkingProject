import socket
import tqdm
import os
import threading

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5001

BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"


def recvFile(client_socket, filename, filesize):
    # received = client_socket.recv(BUFFER_SIZE).decode()
    # filename, filesize = received.split(SEPARATOR)
    filename = os.path.basename(filename)
    filesize = int(filesize)

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
    print(f"[+] File {filename} transferred successfully from {address}")

def sendMessage(filename, filesize, client_socket):
    filename = os.path.basename(filename)
    try: 
        if os.path.getsize(filename) != int(filesize):
            client_socket.sendall(f"[!] The program encountered an error transferring the file. Please try again.".encode())
        else:
            client_socket.sendall(f"[+] Transfer of the file {filename} was completed succesfully.".encode())
    except:
        client_socket.sendall(f"[!] The program encountered an error trying to find the file. Please try again.".encode())
    else:
        client_socket.sendall(f"[!] The program encountered an error transferring the file or the file does not exist. Please try again.".encode())
    print(f"[+] File {filename} was queried by {address}")
    

# These are functions to allow the threading of server operations. More work
# would need to be done to allow for multiple calls to the server at once.
def callRecvFile(client_socket, arg1, arg2):
    t1 = threading.Thread(target=recvFile, args=(client_socket, arg1, arg2))
    t1.start()
    t1.join()

def callSendMessage():
    t2 = threading.Thread(target=sendMessage, args=(client_socket,))
    t2.start()
    t2.join()

# Main program loop, Server will remain open until told by client to quit
quit = True
while quit:
    # establish socket and listen for clients
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((SERVER_HOST, SERVER_PORT))
    s.listen(5)
    

    while True:
        # Establish connection with client
        print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")
        client_socket, address = s.accept() 
        print(f"[+] {address} is connected.\n")

        # Client first a string with 3 arguements separated by Separator tokens
        # First arg will determine the operation being performed
        # The others will provide the arguements to fulfill the task if necessary
        received = client_socket.recv(BUFFER_SIZE).decode()
        operation, arg1, arg2 = received.split(SEPARATOR)
        if operation == "sendingfile":
            callRecvFile(client_socket, arg1, arg2)
        elif operation == "checkingfile":
            sendMessage(arg1, arg2, client_socket)
        elif operation == "printmessage":
            print(f"[+] Message from {address}: {arg1}")
        # If client just wished to disconnect but leave the server up, 
        # this command will do so
        elif operation == "continue":
            print(f"[+] Client {address} is disconnecting.\n")
            client_socket.close()
            break
        # Any invalid operation calls will cause the server to shutdown.
        # May want to make it so any other call causes just the client to disconnect
        else:
            quit = False
            break
        # Disconnect from client
        client_socket.close()
    
    

# close the client socket
client_socket.close()
# close the server socket
s.close()
print("[!] Shutting down server")