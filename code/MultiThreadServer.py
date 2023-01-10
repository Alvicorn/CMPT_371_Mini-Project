# Server.py
# CMPT 371: Mini-Project
# Created On:  Dec 5, 2022
# Last Modified On: Nov 22, 2022
#
# Description: Basic, multi-threaded web server that handles HTTP requests


import socket
import os
import sys
import HTTP
import threading
import random
import Format



###########
# GLOBALS #
###########
SERVER_PORT = 12002
BUFFER_SIZE = 1024
SERVER_TIMEOUT = 120 # 1 until timeout
SOCKETS = 65535


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
            
            if method == "GET":
                filePath = "Files/" + filePath
                
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

    ip = socket.gethostbyname(socket.gethostname())

    # Create TCP welcoming socket
    serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    port = SERVER_PORT
    timeout = SERVER_TIMEOUT
    if (len(sys.argv) > 1):
        for arg in sys.argv[1:]:
            arg = arg.split('=')
            if (arg[0] == "-build"):
                timeout = 10
            elif (arg[0] == "-port"):
                try:
                    port = int(arg[1])
                except ValueError:
                    Format.printError("Port number must be an integer")
                    port = SERVER_PORT
            elif (not isinstance(int(arg[0]), int)):
                Format.printError("Illegal argument")
                exit(1)
    
    serverSocket.settimeout(timeout)
    socketFound = False
    socketCount = 0

    while (socketCount < SOCKETS and not socketFound):
        try:
            serverSocket.bind((ip, port))
            socketFound = True
        except OSError:
            Format.printError(f"{port} port is in use")
            socketCount += 1
            port = random.randint(1, SOCKETS) 

            

    serverSocket.listen(1)
    Format.printText(f"The server is online on port {port}...")
    
    try:
        while True:
            # Server waits on accept for incoming requests.
            # New socket created on return
            connectionSocket, addr = serverSocket.accept()
            thread = threading.Thread(target=handle_request, args=(connectionSocket, ))
            thread.start()
    except socket.error:
        Format.printWarning("Socket timeout")
##################################
if __name__ == "__main__":
    Format.printHeader("Starting Server...")
    start_server()