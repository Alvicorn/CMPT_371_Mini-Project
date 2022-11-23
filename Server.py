# Server.py
# CMPT 371: Mini-Project
# Created On:  Nov 22, 2022
# Last Modified On: Nov 22, 2022
#
# Description: Basic, singly-threaded web server that handles HTTP requests

from socket import *
import os
import time
import HTTP
import sys



###########
# GLOBALS #
###########
SERVER_PORT = 12000
BUFFER_SIZE = 1024



#############
# FUNCTIONS #
#############

# Description: Handle a single client request
def handle_request(connectionSocket):
    request = connectionSocket.recv(BUFFER_SIZE).decode()  
    requestWords = request.split(" ")[0:3]
    # print(request + "\n")

    if len(requestWords) > 1:

        method = requestWords[0]
        filePath = requestWords[1][1:] if len(requestWords[1]) > 2 else requestWords[1] # remove the leading /

        if filePath != "favicon.ico":
            # print("Method: " + method)
            # print(" File path: " + filePath)
            # print(os.path.abspath(os.getcwd()))
            
            if method == "GET":

                if len(filePath) > 1 and os.path.exists(filePath) == True: # 200
                    HTTP.respond_200(connectionSocket, filePath)
                
                elif filePath[-5:] != ".html": # 400
                    HTTP.respond_400(connectionSocket)                    

                else: # 404
                    HTTP.respond_404(connectionSocket)
            
            else: # 400
                HTTP.respond_400(connectionSocket)

    # Close connection too client (but not welcoming socket)
    connectionSocket.close()


# Description: Create the socket and listen for connections
def start_server():
    # Create TCP welcoming socket
    serverSocket = socket(AF_INET,SOCK_STREAM)

    # Bind the server port to the socket
    serverSocket.bind(('',SERVER_PORT))

    # Server begins listening for incoming TCP connections
    serverSocket.listen(1)
    print ("The server is online...")
    
    
    while True:
        # Server waits on accept for incoming requests.
        # New socket created on return
        try:
            connectionSocket, addr = serverSocket.accept()
            handle_request(connectionSocket)
        except KeyboardInterrupt:
            print("Closing Server...")
            serverSocket.close()
            break

    
##################################
if __name__ == "__main__":
    print("Starting Server...")
    start_server()