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
import Format

MAX_RUNTIME = 15 # second
SERVER_NAME = socket.gethostbyname(socket.gethostname())
SERVER_PORT = 12000

test1Result = "FAIL"


# Description: Create a connection with the server. Send the request and 
#               return the server response
def client_connection(request):
    # establish TCP connection to the server
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((SERVER_NAME,SERVER_PORT))
    clientSocket.send(request.encode())
    serverResponse = clientSocket.recv(1024)
    time.sleep(1)     # buffer to allow time for the server to close
    clientSocket.close()
    return serverResponse


# Description: Send a request for test.html. File should be found (200)
def server_test_1(testResults):
    Format.printTest("Executing test 1...")
    request = ("GET /test.html HTTP/1.1\r\n" + 
                "Host: " + str(SERVER_NAME) + ":" + str(SERVER_PORT) + "\r\n")
    serverResponse = client_connection(request)
    # validate response
    expectedResult = "200"
    response = serverResponse.decode().split(" ")
    testResults[0] = "PASS" if response[1] == expectedResult else "FAIL"

def server_test_2(testResults):
    Format.printTest("Executing test 2...")
    request = ("GET /test1.html HTTP/1.1\r\n" + 
                "Host: " + str(SERVER_NAME) + ":" + str(SERVER_PORT) + "\r\n")
    serverResponse = client_connection(request)
    # validate response
    expectedResult = "200"
    response = serverResponse.decode().split(" ")
    testResults[1] = "PASS" if response[1] == expectedResult else "FAIL"

def server_test_3(testResults):
    Format.printTest("Executing test 3...")
    request = ("GET /test2.html HTTP/1.1\r\n" + 
                "Host: " + str(SERVER_NAME) + ":" + str(SERVER_PORT) + "\r\n")
    serverResponse = client_connection(request)
    # validate response
    expectedResult = "200"
    response = serverResponse.decode().split(" ")
    testResults[2] = "PASS" if response[1] == expectedResult else "FAIL"

def server_test_4(testResults):
    Format.printTest("Executing test 4...")
    request = ("GET /test3.html HTTP/1.1\r\n" + 
                "Host: " + str(SERVER_NAME) + ":" + str(SERVER_PORT) + "\r\n")
    serverResponse = client_connection(request)
    # validate response
    expectedResult = "200"
    response = serverResponse.decode().split(" ")
    testResults[3] = "PASS" if response[1] == expectedResult else "FAIL"

def server_test_5(testResults):
    Format.printTest("Executing test 5...")
    request = ("GET /test4.html HTTP/1.1\r\n" + 
                "Host: " + str(SERVER_NAME) + ":" + str(SERVER_PORT) + "\r\n")
    serverResponse = client_connection(request)
    # validate response
    expectedResult = "200"
    response = serverResponse.decode().split(" ")
    testResults[4] = "PASS" if response[1] == expectedResult else "FAIL"

def server_test_6(testResults):
    Format.printTest("Executing test 6...")
    request = ("GET /test5.html HTTP/1.1\r\n" + 
                "Host: " + str(SERVER_NAME) + ":" + str(SERVER_PORT) + "\r\n")
    serverResponse = client_connection(request)
    # validate response
    expectedResult = "200"
    response = serverResponse.decode().split(" ")
    testResults[5] = "PASS" if response[1] == expectedResult else "FAIL"

# Description: Send a request for test.htm. Bad request because unknown file extension (400)
def server_test_7(testResults):
    Format.printTest("Executing test 7...")
    request = ("GET /test.htm HTTP/1.1\r\n" + 
                "Host: " + str(SERVER_NAME) + ":" + str(SERVER_PORT) + "\r\n")
    serverResponse = client_connection(request)
    # validate response
    expectedResult = "400"
    response = serverResponse.decode().split(" ")
    testResults[6] = "PASS" if response[1] == expectedResult else "FAIL"    

# Description: Send a request for notFound.html. File should not be found (404)
def server_test_8(testResults):
    Format.printTest("Executing test 8...")
    request = ("GET /notFound.html HTTP/1.1\r\n" + 
                "Host: " + str(SERVER_NAME) + ":" + str(SERVER_PORT) + "\r\n")
    serverResponse = client_connection(request)
    # validate response
    expectedResult = "404"
    response = serverResponse.decode().split(" ")
    testResults[7] = "PASS" if response[1] == expectedResult else "FAIL"
    
# Description: Send a request for test.htm. the request timed out (408)
# def server_test_9(testResults):
#     print("Executing test 9...")
#     request = ("GET /test.htm HTTP/1.1\r\n" + 
#                 "Host: " + str(SERVER_NAME) + ":" + str(SERVER_PORT) + "\r\n")
#     serverResponse = client_connection(request)
#     # validate response
#     expectedResult = "408"
#     response = serverResponse.decode().split(" ")
#     testResults[8] = "PASS" if response[1] == expectedResult else "FAIL"   

# Description: Execute all test cases in a sequential order since the server
#               is singly-threaded
def server_tests(testResults):
    server_test_1(testResults)
    server_test_2(testResults)
    server_test_3(testResults)
    server_test_4(testResults)
    server_test_5(testResults)
    server_test_6(testResults)
    server_test_7(testResults)
    server_test_8(testResults)
    # server_test_9(testResults)

# Description: Run the server
def run_server():
    start_server()



if __name__ == "__main__":

    expectedCode = [200, 200, 200, 200, 200, 200, 400, 404] #408 expected codes for test cases

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

        Format.printHeader("\n#########################################")
        Format.printHeader("#              TEST RESULTS             #")
        Format.printHeader("#                                       #")
        for index in range(len(expectedCode)):
            # assert testResults[index] == "PASS"

            Format.printHeader("#", end='')
            print(f"\tTest {index+1} ({expectedCode[index]}):\t\t", end='')
            if testResults[index] == "PASS":
                Format.printPass()
            else:
                Format.printFail()
            Format.printHeader("\t#")
        Format.printHeader("#########################################\n")
