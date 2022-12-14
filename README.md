# Overview

This is a simple program designed to increase my familiarity with python's Socket library and networking tools. It functions as a client/server connection, with the host needing the ip address of the server, and from there the
the server runs the server.py file and the client only need run the main.py file to establish the connections and transfer a file between the devices. 

I have had a working knowledge of networking principles and terminology, but had only used it in a cybersecurity capacity. I wanted to design and implement this program to
have hands on experience implementing and using networking tools. Dip my toes in the water, so to speak.
The program also serves as the beginnings of a data hosting server, capable of receiving files, verifying contents, and (eventually) able to provide information from hosted files or transfer files from server to client.


[Software Demo Video](https://youtu.be/6z-0JliTKCM)

# Network Communication

This program is using a Client/Server model to facilitate the transfer of files between the devices.

Connections are made using TCP port 5001 on the server side.

The client is sending a string to the server to alert it to the process that is being conducted, sometimes a file is sent to the server or another string to display, and then the server responds with strings when asked for information on transferred files.

# Development Environment

Coding was completed using Visual Studio Code and Powershell.

Language used was Python, utilizing the Socket library to faciliate the connection, TQDM to show a progress bar of the file transfer, and OS to read and write the file.

# Useful Websites

* [Python Socket Library Documentation](https://docs.python.org/3/library/socket.html)
* [PythonCode File Transfer Tutorial](https://www.thepythoncode.com/article/send-receive-files-using-sockets-python)
* [RealPython Sockets Tutorial](https://realpython.com/python-sockets/)

# Future Work

* ~~The most glaring issue is in the file transfer. When the transfer is the only function to the program, it works correctly. Once more is added it fails to function. Implementing that to work correctly without crashing either client or server is priority number one.~~ My logic required the socket to close the connection to finish the file transfer. Rewrote the program to disconnect and reconnect for every action taken.
* Converting the server into one that utilizes the Python socketserver library would be beneficial to learning that tool and the benefits to using a more defined server class.
* Improving on the UI and adding more functionality, i.e. messages from server to client, managment of multiple clients through threads, ability to retrieve information from files stored on the server