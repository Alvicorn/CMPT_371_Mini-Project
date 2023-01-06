# ServerTest.py
# CMPT 371: Mini-Project
# Created On:  Nov 30, 2022
#
# Description: Test script for the singly-threaded proxy server

from multiprocessing import Process, Manager
import multiprocessing as mp
import time
from socket import *
import socket
import shutil
import os

from Proxy import start_proxy
from Server import start_server

MAX_RUNTIME = 20 # second
SERVER_NAME = socket.gethostbyname(socket.gethostname())
PROXY_PORT = 12001

test1Result = "FAIL"


# Description: Create a connection with the server. Send the request and 
#               return the server response
def client_connection(request):
    # establish TCP connection to the server
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((SERVER_NAME,PROXY_PORT))
    clientSocket.send(request.encode())
    serverResponse = clientSocket.recv(1024)
    time.sleep(1)     # buffer to allow time for the server to close
    clientSocket.close()
    return serverResponse


# Description: Send a request for test.html. Proxy will request from the server.
#              File should be found (200)
def proxy_test_1(testResults):
    print("Executing test 1...")
    request = ("GET /test.html HTTP/1.1\r\n" + 
                "Host: " + str(SERVER_NAME) + ":" + str(PROXY_PORT) + "\r\n" + 
                "If-Modified-Since: Wed, 01 Dec 2022 13:24:54\r\n")
    serverResponse = client_connection(request)
    # validate response
    expectedResult = "200"
    response = serverResponse.decode().split(" ")
    testResults[0] = "PASS" if response[1] == expectedResult else "FAIL"

# Description: Send a request for test.html. Proxy will request from the server.
#              File should be found (200)
def proxy_test_2(testResults):
    print("Executing test 2...")
    request = ("GET /test1.html HTTP/1.1\r\n" + 
                "Host: " + str(SERVER_NAME) + ":" + str(PROXY_PORT) + "\r\n" + 
                "If-Modified-Since: Wed, 01 Dec 2022 13:24:54\r\n")
    serverResponse = client_connection(request)
    # validate response
    expectedResult = "200"
    response = serverResponse.decode().split(" ")
    testResults[1] = "PASS" if response[1] == expectedResult else "FAIL"

# Description: Send a request for test.html. Proxy will request from the server.
#              File should be found (200)
def proxy_test_3(testResults):
    print("Executing test 3...")
    request = ("GET /test2.html HTTP/1.1\r\n" + 
                "Host: " + str(SERVER_NAME) + ":" + str(PROXY_PORT) + "\r\n" + 
                "If-Modified-Since: Wed, 01 Dec 2022 13:24:54\r\n")
    serverResponse = client_connection(request)
    # validate response
    expectedResult = "200"
    response = serverResponse.decode().split(" ")
    testResults[2] = "PASS" if response[1] == expectedResult else "FAIL"

# Description: Send a request for test.html. Proxy will request from the server.
#              File should be found (200)
def proxy_test_4(testResults):
    print("Executing test 4...")
    request = ("GET /test3.html HTTP/1.1\r\n" + 
                "Host: " + str(SERVER_NAME) + ":" + str(PROXY_PORT) + "\r\n" + 
                "If-Modified-Since: Wed, 01 Dec 2022 13:24:54\r\n")
    serverResponse = client_connection(request)
    # validate response
    expectedResult = "200"
    response = serverResponse.decode().split(" ")
    testResults[3] = "PASS" if response[1] == expectedResult else "FAIL"

# Description: Send a request for test.html. Proxy will request from the server.
#              File should be found (200)
def proxy_test_5(testResults):
    print("Executing test 5...")
    request = ("GET /test4.html HTTP/1.1\r\n" + 
                "Host: " + str(SERVER_NAME) + ":" + str(PROXY_PORT) + "\r\n" + 
                "If-Modified-Since: Wed, 01 Dec 2022 13:24:54\r\n")
    serverResponse = client_connection(request)
    # validate response
    expectedResult = "200"
    response = serverResponse.decode().split(" ")
    testResults[4] = "PASS" if response[1] == expectedResult else "FAIL"

# Description: Send a request for test.html. Proxy will request from the server.
#              File should be found (200)
def proxy_test_6(testResults):
    print("Executing test 6...")
    request = ("GET /test5.html HTTP/1.1\r\n" + 
                "Host: " + str(SERVER_NAME) + ":" + str(PROXY_PORT) + "\r\n" + 
                "If-Modified-Since: Wed, 01 Dec 2022 13:24:54\r\n")
    serverResponse = client_connection(request)
    # validate response
    expectedResult = "200"
    response = serverResponse.decode().split(" ")
    testResults[5] = "PASS" if response[1] == expectedResult else "FAIL"

# Description: Send a request for test.html which should be found in the proxy
#              File should be found and return 200 because the file was last modified
#              in 2022 (200)
def proxy_test_7(testResults):
    print("Executing test 7...")
    request = ("GET /test5.html HTTP/1.1\r\n" + 
                "Host: " + str(SERVER_NAME) + ":" + str(PROXY_PORT) + "\r\n" + 
                "If-Modified-Since: Wed, 01 Dec 2023 13:24:54\r\n")
    serverResponse = client_connection(request)
    # validate response
    expectedResult = "200"
    response = serverResponse.decode().split(" ")
    testResults[6] = "PASS" if response[1] == expectedResult else "FAIL"

# Description: Send a request for test.html which should be found in the proxy
#              File should be found and return 304 because the file has not been Modified
#              since 2022
def proxy_test_8(testResults):
    print("Executing test 8...")
    request = ("GET /test5.html HTTP/1.1\r\n" + 
                "Host: " + str(SERVER_NAME) + ":" + str(PROXY_PORT) + "\r\n" + 
                "If-Modified-Since: Wed, 01 Dec 2021 13:24:54\r\n")
    serverResponse = client_connection(request)
    # validate response
    expectedResult = "304"
    response = serverResponse.decode().split(" ")
    testResults[7] = "PASS" if response[1] == expectedResult else "FAIL"

# Description: Send a request for test.htm. Bad request because unknown file extension (400)
def proxy_test_9(testResults):
    print("Executing test 9...")
    request = ("GET /test.htm HTTP/1.1\r\n" + 
                "Host: " + str(SERVER_NAME) + ":" + str(PROXY_PORT) + "\r\n" + 
                "If-Modified-Since: Wed, 01 Dec 2022 13:24:54\r\n")
    serverResponse = client_connection(request)
    # validate response
    expectedResult = "400"
    response = serverResponse.decode().split(" ")
    testResults[8] = "PASS" if response[1] == expectedResult else "FAIL"    

# Description: Send a request for notFound.html. File should not be found (404)
def proxy_test_10(testResults):
    print("Executing test 10...")
    request = ("GET /notFound.html HTTP/1.1\r\n" + 
                "Host: " + str(SERVER_NAME) + ":" + str(PROXY_PORT) + "\r\n" + 
                "If-Modified-Since: Wed, 01 Dec 2022 13:24:54\r\n")
    serverResponse = client_connection(request)
    # validate response
    expectedResult = "404"
    response = serverResponse.decode().split(" ")
    testResults[9] = "PASS" if response[1] == expectedResult else "FAIL"


# Description: Execute all test cases in a sequential order since the server
#               is singly-threaded
def proxy_tests(testResults):
    proxy_test_1(testResults)
    proxy_test_2(testResults)
    proxy_test_3(testResults)
    proxy_test_4(testResults)
    proxy_test_5(testResults)
    proxy_test_6(testResults)
    proxy_test_7(testResults)
    proxy_test_8(testResults)
    proxy_test_9(testResults)
    proxy_test_10(testResults)
        

# Description: Run the server
def run_server():
    start_server()

def run_proxy():
    start_proxy()

if __name__ == "__main__":

    # remove cache
    try: 
        shutil.rmtree("Cache")
    except OSError:
        if os.path.exists("Cache"):
            os.rmdir("Cache")

    expectedCode = [200, 200, 200, 200, 200, 200, 200, 304, 400, 404] # expected codes for test cases

    with Manager() as manager:
        testResults = manager.dict()   # dictionary of test case results

        print("Executing tests...")
        server = Process(target=run_server) # process to run the server
        proxy = Process(target=run_proxy) # process to run the proxy
        test = Process(target=proxy_tests, args=(testResults,)) # process to execute test cases
        
        server.start()
        proxy.start()
        test.start()
        
        time.sleep(MAX_RUNTIME)
        
        if (test.is_alive()):
            test.terminate()

        server.terminate()
        proxy.terminate()
        
        test.join()
        proxy.join()
        server.join()

        print("\n#########################################")
        print("#              TEST RESULTS             #")
        print("#                                       #")
        for index in range(len(expectedCode)):  
            print(f"#\tTest {index+1} ({expectedCode[index]}):\t\t {testResults[index]} \t#")
        print("#########################################\n")