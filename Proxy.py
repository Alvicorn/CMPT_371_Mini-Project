# Proxy.py
# CMPT 371: Mini-Project
# Created On:  Nov 29, 2022
# Last Modified On: Nov 29, 2022
#
# Description: Basic, singly-threaded web proxy 


import socket
import os
import time
import HTTP
import sys

###########
# GLOBALS #
###########
SERVER_PORT = 12000
SERVER_NAME = socket.gethostbyname(socket.gethostname())
PROXY_PORT = 12001
BUFFER_SIZE = 1024

CACHED_FILES = []
CACHE_SIZE = 5



#############
# FUNCTIONS #
#############

# Description: Create a connection with the server. Send the request and 
#               return the server response
def request_to_server(request):
    # establish TCP connection to the server
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        clientSocket.connect((SERVER_NAME,SERVER_PORT))
        clientSocket.send(request.encode())
        serverResponse = clientSocket.recv(BUFFER_SIZE)
        header = serverResponse.decode().split(" ", 15)
      
        if header[1] == "200":
            data = header[15].split("\n", 1)[1]
            time.sleep(1)     # buffer to allow time for the server to close
            clientSocket.close()
            return data
        else:
            time.sleep(1)     # buffer to allow time for the server to close
            clientSocket.close()
            return header[1]
    except socket.error:
        print("Error: Server is not online")
        return socket.error

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
            filePath_cache = "Cache/" + filePath
            # print(" File path: " + filePath)
            
            # print(os.path.abspath(os.getcwd()))
            
            if method == "GET":

                # cache is empty
                if len(CACHED_FILES) == 0:
                    request = ("GET /"+ filePath + " HTTP/1.1\r\n" + 
                                "Host: " + str(SERVER_NAME) + ":" + str(SERVER_PORT) + "\r\n")
                    serverResponse = request_to_server(request)
                    if serverResponse != socket.error:
                        if serverResponse == "404":
                                HTTP.respond_404(connectionSocket)
                        
                        # TODO handle the other codes...remainder is 200
                        
                        if len(serverResponse) > 6: # 200 code
                            if len(CACHED_FILES) == CACHE_SIZE - 1: # cache size exceeded, evict oldest item
                                CACHED_FILES.pop(0)
                            CACHED_FILES.append(filePath)
                            with open(filePath_cache, "w") as f:
                                f.write(serverResponse)

                            HTTP.respond_200(connectionSocket, filePath_cache)

                # check if file exists in the cache folder
                else:
                    if len(filePath) > 1 and os.path.exists(filePath_cache) == True: # 200
                        HTTP.respond_200(connectionSocket, filePath_cache)
                
                    elif filePath[-5:] != ".html": # 400
                        HTTP.respond_400(connectionSocket)                    

                    # file is not found in cache, make a request to the server
                    else:
                        request = ("GET /"+ filePath + " HTTP/1.1\r\n" + 
                                "Host: " + str(SERVER_NAME) + ":" + str(SERVER_PORT) + "\r\n")
                        serverResponse = request_to_server(request)
                        if serverResponse != socket.error:
                            if serverResponse == "404":
                                HTTP.respond_404(connectionSocket)
            
            else: # 400
                HTTP.respond_400(connectionSocket)

    # Close connection too client (but not welcoming socket)
    connectionSocket.close()

# Description: Create the socket and listen for connections
def start_proxy():

    ip = socket.gethostbyname(socket.gethostname())

    # Create TCP welcoming socket
    serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    serverSocket.bind((ip,PROXY_PORT))

    serverSocket.listen(1)
    print ("The proxy is online...")
    
    
    while True:
        # Server waits on accept for incoming requests.
        # New socket created on return
        connectionSocket, addr = serverSocket.accept()
        handle_request(connectionSocket)



##################################
if __name__ == "__main__":
    print("Starting Proxy...")
    start_proxy()