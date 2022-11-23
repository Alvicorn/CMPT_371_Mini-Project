# HTTP.py
# CMPT 371: Mini-Project
# Created On:  Nov 22, 2022
# Last Modified On: Nov 22, 2022
#
# Description: Implementation of HTTP protocols


from datetime import datetime as dt
import time

TIMEOUT = 2 # seconds


# Description: Generate the http response status line and header
def http_header_response(status, contentLength=0, contentType="none"):
    # create the status line
    header = "HTTP/1.1 "
    if status == 200:
        header = header + "200 OK\r\n"
    elif status == 304:
          header = header + "304 Not Modified\r\n"
    elif status == 400:
        header = header + "400 Bad Request\r\n"
    elif status == 404:
        header = header + "404 Not Found\r\n"
    elif status == 408:
        header = header + "408 Request Timed Out\r\n"
    
    # append the date
    date = dt.now()
    header = header + "date: " + date.strftime("%a, %d %b %Y %H:%M:%S %Z") + "\r\n"
    # append server details
    header = header + "Server: Local server for mini-project\r\n"
    #append accepted ranges
    header = header + "Accept-Ranges: bytes\r\n"
    if status != 200 or status != 304:
        # append content content
        header = header + "Content-Length: " + str(contentLength) + "\r\n"
        # append content type
        header = header + "Content-Type: " + contentType + "\r\n"
    print(header)
    return header



# Description: Respond 200 status to the request and send
#              the requested html file
def respond_200(connectionSocket, filePath):
    # open and read file
    file = open(filePath)
    data = file.read()

    # send header
    header = http_header_response(200, contentLength=len(data), contentType="text/html")
    connectionSocket.send(header.encode())
    # send data
    for i in range(0, len(data)):
        connectionSocket.send(data[i].encode())
    connectionSocket.send("\n".encode())


# Description: Respond 400 status to the request
def respond_400(connectionSocket):
    header = http_header_response(400, contentLength=16, contentType="text/html")
    response = header + "\n\n400 Bad Request"
    connectionSocket.send(response.encode())


# Description: Respond 404 status to the request
def respond_404(connectionSocket):
    header = http_header_response(404, contentLength=16, contentType="text/html")
    response = header + "\n\n404 Not Found"
    connectionSocket.send(response.encode())
