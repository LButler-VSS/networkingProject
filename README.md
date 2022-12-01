# Overview

This is a simple program designed to increase my familiarity with python's Socket library and networking tools. It functions as a client/server connection, with the host needing the ip address of the server, and from there the
the server runs the server.py file and the client only need run the main.py file to establish the connections and transfer a file between the devices. 

I have had a working knowledge of networking principles and terminology, but had only used it in a cybersecurity capacity. I wanted to design and implement this program to
have hands on experience implementing and using networking tools. Dip my toes in the water, so to speak.

{Provide a link to your YouTube demonstration.  It should be a 4-5 minute demo of the software running (you will need to show two pieces of software running and communicating with each other) and a walkthrough of the code.}

[Software Demo Video](http://youtube.link.goes.here)

# Network Communication

This program is using a Client/Server model to facilitate the transfer of files between the devices.

Connection are made using TCP port 5001

The client is sending a file to the server and the server is responding back with a response to indicate whether the transfer was successful.

# Development Environment

Coding was completed using Visual Studio Code and Powershell.

Language used was Python, utilizing the Socket library to faciliate the connection, TQDM to show a progress bar of the file transfer, and OS to read and write the file.

# Useful Websites

{Make a list of websites that you found helpful in this project}
* [Python Socket Library Documentation](https://docs.python.org/3/library/socket.html)
* [PythonCode File Transfer Tutorial](https://www.thepythoncode.com/article/send-receive-files-using-sockets-python)

# Future Work

{Make a list of things that you need to fix, improve, and add in the future.}
* Item 1
* Item 2
* Item 3