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


# Description: Send a request for test.html. File should be found (200)
def proxy_test_1(testResults):
    print("Executing test 1...")
    request = ("GET /test.html HTTP/1.1\r\n" + 
                "Host: " + str(SERVER_NAME) + ":" + str(PROXY_PORT) + "\r\n")
    serverResponse = client_connection(request)
    # validate response
    expectedResult = "200"
    response = serverResponse.decode().split(" ")
    testResults[0] = "PASS" if response[1] == expectedResult else "FAIL"

def proxy_test_2(testResults):
    print("Executing test 2...")
    request = ("GET /Files/test1.html HTTP/1.1\r\n" + 
                "Host: " + str(SERVER_NAME) + ":" + str(PROXY_PORT) + "\r\n")
    serverResponse = client_connection(request)
    # validate response
    expectedResult = "200"
    response = serverResponse.decode().split(" ")
    testResults[1] = "PASS" if response[1] == expectedResult else "FAIL"

def proxy_test_3(testResults):
    print("Executing test 3...")
    request = ("GET /Files/test2.html HTTP/1.1\r\n" + 
                "Host: " + str(SERVER_NAME) + ":" + str(PROXY_PORT) + "\r\n")
    serverResponse = client_connection(request)
    # validate response
    expectedResult = "200"
    response = serverResponse.decode().split(" ")
    testResults[2] = "PASS" if response[1] == expectedResult else "FAIL"

def proxy_test_4(testResults):
    print("Executing test 4...")
    request = ("GET /Files/test3.html HTTP/1.1\r\n" + 
                "Host: " + str(SERVER_NAME) + ":" + str(PROXY_PORT) + "\r\n")
    serverResponse = client_connection(request)
    # validate response
    expectedResult = "200"
    response = serverResponse.decode().split(" ")
    testResults[3] = "PASS" if response[1] == expectedResult else "FAIL"

def proxy_test_5(testResults):
    print("Executing test 5...")
    request = ("GET /Files/test4.html HTTP/1.1\r\n" + 
                "Host: " + str(SERVER_NAME) + ":" + str(PROXY_PORT) + "\r\n")
    serverResponse = client_connection(request)
    # validate response
    expectedResult = "200"
    response = serverResponse.decode().split(" ")
    testResults[4] = "PASS" if response[1] == expectedResult else "FAIL"

def proxy_test_6(testResults):
    print("Executing test 6...")
    request = ("GET /Files/test5.html HTTP/1.1\r\n" + 
                "Host: " + str(SERVER_NAME) + ":" + str(PROXY_PORT) + "\r\n")
    serverResponse = client_connection(request)
    # validate response
    expectedResult = "200"
    response = serverResponse.decode().split(" ")
    testResults[5] = "PASS" if response[1] == expectedResult else "FAIL"

# Description: Send a request for test.htm. Bad request because unknown file extension (400)
def proxy_test_7(testResults):
    print("Executing test 7...")
    request = ("GET /test.htm HTTP/1.1\r\n" + 
                "Host: " + str(SERVER_NAME) + ":" + str(PROXY_PORT) + "\r\n")
    serverResponse = client_connection(request)
    # validate response
    expectedResult = "400"
    response = serverResponse.decode().split(" ")
    testResults[6] = "PASS" if response[1] == expectedResult else "FAIL"    

# Description: Send a request for notFound.html. File should not be found (404)
def proxy_test_8(testResults):
    print("Executing test 8...")
    request = ("GET /notFound.html HTTP/1.1\r\n" + 
                "Host: " + str(SERVER_NAME) + ":" + str(PROXY_PORT) + "\r\n")
    serverResponse = client_connection(request)
    # validate response
    expectedResult = "404"
    response = serverResponse.decode().split(" ")
    testResults[7] = "PASS" if response[1] == expectedResult else "FAIL"


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
    
    # # remove cache
    # try: 
    #     shutil.rmtree("Cache")
    # except OSError:
    #     os.rmdir("Cache")
    

# Description: Run the server
def run_server():
    start_server()

def run_proxy():
    start_proxy()

if __name__ == "__main__":
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
        print("#\tTest 1 (200):\t\t" + testResults[0] + "\t#")
        print("#\tTest 2 (200):\t\t" + testResults[1] + "\t#")
        print("#\tTest 3 (200):\t\t" + testResults[2] + "\t#")
        print("#\tTest 4 (200):\t\t" + testResults[3] + "\t#")
        print("#\tTest 5 (200):\t\t" + testResults[4] + "\t#")
        print("#\tTest 6 (200):\t\t" + testResults[5] + "\t#")
        print("#\tTest 7 (400):\t\t" + testResults[6] + "\t#")
        print("#\tTest 8 (404):\t\t" + testResults[7] + "\t#")
        print("#########################################\n")