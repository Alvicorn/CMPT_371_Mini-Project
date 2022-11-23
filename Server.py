# Server.py
# CMPT 371: Mini-Project
# Created On:  Nov 22, 2022
# Last Modified On: Nov 22, 2022

from socket import *
import os

SERVER_PORT = 12000
BUFFER_SIZE = 1024

# Create TCP welcoming socket
serverSocket = socket(AF_INET,SOCK_STREAM)

# Bind the server port to the socket
serverSocket.bind(('',SERVER_PORT))

# Server begins listening for incoming TCP connections
serverSocket.listen(1)
print ("The server is online")



while True: 

    # Server waits on accept for incoming requests.
    # New socket created on return
    connectionSocket, addr = serverSocket.accept()
     
    # client request
    request = connectionSocket.recv(BUFFER_SIZE).decode()  
    
    requestWords = request.split(" ")[0:3]
    response = "HTTP/1.1 400 Not Found\n\n404 Not Found" # default response
    
    method = requestWords[0]
    filePath = requestWords[1][1:] if len(requestWords[1]) > 2 else requestWords[1] # remove the leading /
    if filePath != "favicon.ico":

        print("Method: " + method)
        print(" File path: " + filePath)
        
        if method == "GET":
            if len(filePath) > 1 and os.path.exists(filePath) == True: # 200
                response = "HTTP/1.1 200 OK\n\n"
                connectionSocket.send(response.encode())
                # open file, read the file and send it
                file = open(filePath)
                data = file.read()
                for i in range(0, len(data)):
                    connectionSocket.send(data[i].encode())
                connectionSocket.send("\n".encode())

            else:
                # Send the reply
                connectionSocket.send(response.encode())
    
    # Close connection too client (but not welcoming socket)
    connectionSocket.close()