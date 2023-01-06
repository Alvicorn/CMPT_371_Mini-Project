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
import Format
import json
from datetime import datetime as dt

###########
# GLOBALS #
###########
SERVER_PORT = 12000
SERVER_NAME = socket.gethostbyname(socket.gethostname())
SERVER_TIMEOUT = 120 # 1 until timeout
PROXY_PORT = 12001
BUFFER_SIZE = 1024

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
        header = serverResponse.decode().split(" ", 20)
        # File found in server
        if header[1] == "200":
            t = header[13].split("\n")[0]
            lastModified = f"{header[9]} {header[10]} {header[11]} {header[12]} {t}"
            data = header[20].split("\n", 1)[1]
            time.sleep(1)     
            clientSocket.close()
            return [data, lastModified]
        # file not found in server
        else:
            time.sleep(1)  
            clientSocket.close()
            return header[1]
    except socket.error:
        Format.printError("Server is not online")
        return socket.error

# Description: Handle a single client request
def handle_request(connectionSocket):
    # load cache information
    cacheCount = 0
    cacheList = []
    blank = False

    if not os.path.exists("./Cache/files.json"):
        os.mkdir("Cache")
        open("./Cache/files.json", "w").close()

    with open("./Cache/files.json", "r+") as f:
        try:
            j = json.load(f)
            cacheCount = j["cache_count"]
            cacheList = j["files"]
        except ValueError:
            blank = True
            blankJson = {
                "cache_count": 0,
                "files": []
            }
            json.dump(blankJson, f, ensure_ascii=False, indent=4)
    if blank:
        with open("./Cache/files.json", "r") as f:
            j = json.load(f)
            cacheCount = j["cache_count"]
            cacheList = j["files"]

    # parse request from client            
    request = connectionSocket.recv(BUFFER_SIZE).decode()  
    lines = request.split("\r\n")
    requestWords = lines[0].split(" ")
    modSince = 0
    if (len(lines) > 2):
        if (lines[2].find("Connection")): 
            str_date = lines[2].split(" ", 1)[1]
            modSince = dt.strptime(str_date, "%a, %d %b %Y %H:%M:%S") 
    
    if len(requestWords) > 1:

        method = requestWords[0]
        filePath = requestWords[1][1:] if len(requestWords[1]) > 2 else requestWords[1] # remove the leading /

        if filePath != "favicon.ico":           
            filePath_cache = "Cache/" + filePath.split("/")[-1] #isolate the file name and its extension
            if method == "GET":
                # cache is empty
                if cacheCount < 1:
                    request = ("GET /"+ filePath + " HTTP/1.1\r\n" + 
                                "Host: " + str(SERVER_NAME) + ":" + str(SERVER_PORT) + "\r\n")
                    serverResponse = request_to_server(request)
                    if serverResponse != socket.error:
                        if serverResponse == "404":
                                HTTP.respond_404(connectionSocket)
                        
                        # TODO handle the other codes...remainder is 200
                        
                        if len(serverResponse) == 2: # 200 code
                            cacheCount += 1
                        
                            date = dt.now()
                            cacheList.append({
                                "path": filePath_cache,
                                "last_access_date": date.strftime("%a, %d %b %Y %H:%M:%S"),
                                "last_modified":serverResponse[1]
                            })
                            with open("./Cache/files.json", "w", encoding="utf8") as f:
                                toJson = {
                                    "cache_count": cacheCount,
                                    "files": cacheList
                                }
                                json.dump(toJson, f, ensure_ascii=False, indent=4)

                            with open(filePath_cache, "w") as f:                                
                                f.write(serverResponse[0])

                            HTTP.respond_200(connectionSocket, serverResponse[0], lastModified=serverResponse[1])

                # check if file exists in the cache folder
                else:
                    if len(filePath) > 1 and os.path.exists(filePath_cache) == True: # 200
                        
                        cacheItem = 0
                        for index in cacheList:
                            if (index["path"] == filePath_cache):
                                cacheItem = index

                        fileLastModified = cacheItem["last_modified"]
                        fileLastModified = dt.strptime(fileLastModified, "%a, %d %b %Y %H:%M:%S")       
                        if (fileLastModified > modSince):
                            modTime = os.path.getmtime(filePath_cache)
                            modTime = dt.fromtimestamp(modTime)
                            modTime = modTime.strftime("%a, %d %b %Y %H:%M:%S")
                            # open and read file
                            file = open(filePath_cache)
                            data = file.read()      
                            HTTP.respond_304(connectionSocket, data, lastModified=modTime)
                        else:                        
                            modTime = os.path.getmtime(filePath_cache)
                            modTime = dt.fromtimestamp(modTime)
                            modTime = modTime.strftime("%a, %d %b %Y %H:%M:%S")
                            # open and read file
                            file = open(filePath_cache)
                            data = file.read()      
                            HTTP.respond_200(connectionSocket, data, lastModified=modTime)
                            
                        
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
                         
                            else: # 200 code
                                if cacheCount == CACHE_SIZE:
                                    rm = cacheList.pop(0) # evict the oldest cached entry
                                    cacheCount -= 1
                                    os.remove(rm["path"])

                                cacheCount += 1
                        
                                date = dt.now()
                                cacheList.append({
                                    "path": filePath_cache,
                                    "last_access_date": date.strftime("%a, %d %b %Y %H:%M:%S"),
                                    "last_modified":serverResponse[1]
                                })
                                with open("./Cache/files.json", "w", encoding="utf8") as f:
                                    toJson = {
                                        "cache_count": cacheCount,
                                        "files": cacheList
                                    }
                                    json.dump(toJson, f, ensure_ascii=False, indent=4)

                                with open(filePath_cache, "w") as f:                                
                                    f.write(serverResponse[0])

                                HTTP.respond_200(connectionSocket, serverResponse[0], lastModified=serverResponse[1])
                        else: # 400
                            HTTP.respond_400(connectionSocket)

    # Close connection too client (but not welcoming socket)
    connectionSocket.close()

# Description: Create the socket and listen for connections
def start_proxy():

    ip = socket.gethostbyname(socket.gethostname())

    # Create TCP welcoming socket
    serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    serverSocket.settimeout(SERVER_TIMEOUT)
    serverSocket.bind((ip,PROXY_PORT))

    serverSocket.listen(1)
    Format.printText("The proxy is online...")
    try:
        while True:
            # Server waits on accept for incoming requests.
            # New socket created on return
            connectionSocket, addr = serverSocket.accept()
            handle_request(connectionSocket)
    except socket.error:
        Format.printWarning("Socket timeout")
    



##################################
if __name__ == "__main__":
    Format.printHeader("Starting Proxy...")
    start_proxy()