# ServerTest.py
# CMPT 371: Mini-Project
# Created On:  Nov 23, 2022
# Last Modified On: Nov 23, 2022
#
# Description: Test script for the singly-threaded server

from multiprocessing import Process, Manager
import multiprocessing as mp
import time
from Server import start_server
from socket import *
import socket

MAX_RUNTIME = 10 # second

test1Result = "FAIL"


# Description: Create a connection with the server. Send the request and 
#               return the server response
def client_connection(request):
    # Specify Server Address
    serverName = socket.gethostbyname(socket.gethostname())
    serverPort = 12000

    # establish TCP connection to the server
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((serverName,serverPort))
    clientSocket.send(request.encode())
    serverResponse = clientSocket.recv(1024)
    time.sleep(1)     # buffer to allow time for the server to close
    clientSocket.close()
    return serverResponse


# Description: Send a request for test.html. File should be found (200)
def server_test_1(testResults):
    print("Executing test 1...")
    request = ("GET /test.html HTTP/1.1\r\n" + 
                "Host: localhost:12000\r\n")
    serverResponse = client_connection(request)
    # validate response
    expectedResult = "200"
    response = serverResponse.decode().split(" ")
    testResults[0] = "PASS" if response[1] == expectedResult else "FAIL"

# Description: Send a request for test.htm. Bad request because unknown file extension (400)
def server_test_2(testResults):
    print("Executing test 2...")
    request = ("GET /test.htm HTTP/1.1\r\n" + 
                "Host: localhost:12000\r\n")
    serverResponse = client_connection(request)
    # validate response
    expectedResult = "400"
    response = serverResponse.decode().split(" ")
    testResults[1] = "PASS" if response[1] == expectedResult else "FAIL"    

# Description: Send a request for notFound.html. File should not be found (404)
def server_test_3(testResults):
    print("Executing test 3...")
    request = ("GET /notFound.html HTTP/1.1\r\n" + 
                "Host: localhost:12000\r\n")
    serverResponse = client_connection(request)
    # validate response
    expectedResult = "404"
    response = serverResponse.decode().split(" ")
    testResults[2] = "PASS" if response[1] == expectedResult else "FAIL"


# Description: Execute all test cases in a sequential order since the server
#               is singly-threaded
def server_tests(testResults):
    server_test_1(testResults)
    server_test_2(testResults)
    server_test_3(testResults)

# Description: Run the server
def run_server():
    start_server()





if __name__ == "__main__":
    with Manager() as manager:
        testResults = manager.dict()   # dictionary of test case results

        print("Executing tests...")
        run = Process(target=run_server) # process to run the server
        test = Process(target=server_tests, args=(testResults,)) # process to execute test cases
        
        run.start()
        test.start()
        
        time.sleep(MAX_RUNTIME)
        
        if (test.is_alive()):
            test.terminate()

        run.terminate()
        
        test.join()
        run.join()

        print("\n#########################################")
        print("#              TEST RESULTS             #")
        print("#                                       #")
        print("#\tTest 1 (200):\t\t" + testResults[0] + "\t#")
        print("#\tTest 2 (400):\t\t" + testResults[1] + "\t#")
        print("#\tTest 2 (404):\t\t" + testResults[2] + "\t#")
        print("#########################################\n")