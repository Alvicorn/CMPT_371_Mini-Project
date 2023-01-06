# Server.py
# CMPT 371: Mini-Project
# Created On:  Dec 5, 2022
# Last Modified On: Nov 22, 2022
#
# Description: Basic, multi-threaded web server that handles HTTP requests


import socket
import os
import HTTP
import threading
import Format



###########
# GLOBALS #
###########
SERVER_PORT = 12002
BUFFER_SIZE = 1024
SERVER_TIMEOUT = 120 # 1 until timeout


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
    serverSocket.settimeout(SERVER_TIMEOUT)
    serverSocket.bind((ip,SERVER_PORT))

    serverSocket.listen(1)
    Format.printText("The server is online...")
    
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