# ServerTest.py
# CMPT 371: Mini-Project
# Created On:  Dec 5, 2022
# Last Modified On: Nov 23, 2022
#
# Description: Test script for the multi-threaded server

from multiprocessing import Process, Manager
import multiprocessing as mp
import random
import time
from MultiThreadServer import start_server
from socket import *
import socket


SERVER_NAME = socket.gethostbyname(socket.gethostname())
SERVER_PORT = 12002




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
def server_test_1(results, clientNumber):
    print(f"Executing test 1 for client {clientNumber+1}...")
    request = ("GET /test.html HTTP/1.1\r\n" + 
                "Host: " + str(SERVER_NAME) + ":" + str(SERVER_PORT) + "\r\n")
    serverResponse = client_connection(request)
    # validate response
    expectedResult = "200"
    response = serverResponse.decode().split(" ")
    status = "PASS" if response[1] == expectedResult else "FAIL"
    results[clientNumber][0] = {"status": status, "time": time.time()}

def server_test_2(results, clientNumber):
    print(f"Executing test 2 for client {clientNumber+1}...")
    request = ("GET /test1.html HTTP/1.1\r\n" + 
                "Host: " + str(SERVER_NAME) + ":" + str(SERVER_PORT) + "\r\n")
    serverResponse = client_connection(request)
    # validate response
    expectedResult = "200"
    response = serverResponse.decode().split(" ")
    status = "PASS" if response[1] == expectedResult else "FAIL"
    results[clientNumber][1] = {"status": status, "time": time.time()}

def server_test_3(results, clientNumber):
    print(f"Executing test 3 for client {clientNumber+1}...")
    request = ("GET /test2.html HTTP/1.1\r\n" + 
                "Host: " + str(SERVER_NAME) + ":" + str(SERVER_PORT) + "\r\n")
    serverResponse = client_connection(request)
    # validate response
    expectedResult = "200"
    response = serverResponse.decode().split(" ")
    status = "PASS" if response[1] == expectedResult else "FAIL"
    results[clientNumber][2] = {"status": status, "time": time.time()}
    
def server_test_4(results, clientNumber):
    print(f"Executing test 4 for client {clientNumber+1}...")
    request = ("GET /test3.html HTTP/1.1\r\n" + 
                "Host: " + str(SERVER_NAME) + ":" + str(SERVER_PORT) + "\r\n")
    serverResponse = client_connection(request)
    # validate response
    expectedResult = "200"
    response = serverResponse.decode().split(" ")
    status = "PASS" if response[1] == expectedResult else "FAIL"
    results[clientNumber][3] = {"status": status, "time": time.time()}

def server_test_5(results, clientNumber):
    print(f"Executing test 5 for client {clientNumber+1}...")
    request = ("GET /test4.html HTTP/1.1\r\n" + 
                "Host: " + str(SERVER_NAME) + ":" + str(SERVER_PORT) + "\r\n")
    serverResponse = client_connection(request)
    # validate response
    expectedResult = "200"
    response = serverResponse.decode().split(" ")
    status = "PASS" if response[1] == expectedResult else "FAIL"
    results[clientNumber][4] = {"status": status, "time": time.time()}
    
def server_test_6(results, clientNumber):
    print(f"Executing test 6 for client {clientNumber+1}...")
    request = ("GET /test5.html HTTP/1.1\r\n" + 
                "Host: " + str(SERVER_NAME) + ":" + str(SERVER_PORT) + "\r\n")
    serverResponse = client_connection(request)
    # validate response
    expectedResult = "200"
    response = serverResponse.decode().split(" ")
    status = "PASS" if response[1] == expectedResult else "FAIL"
    results[clientNumber][5] = {"status": status, "time": time.time()}

# Description: Send a request for test.htm. Bad request because unknown file extension (400)
def server_test_7(results, clientNumber):
    print(f"Executing test 7 for client {clientNumber+1}...")
    request = ("GET /test.htm HTTP/1.1\r\n" + 
                "Host: " + str(SERVER_NAME) + ":" + str(SERVER_PORT) + "\r\n")
    serverResponse = client_connection(request)
    # validate response
    expectedResult = "400"
    response = serverResponse.decode().split(" ")
    status = "PASS" if response[1] == expectedResult else "FAIL"
    results[clientNumber][6] = {"status": status, "time": time.time()}  

# Description: Send a request for notFound.html. File should not be found (404)
def server_test_8(results, clientNumber):
    print(f"Executing test 8 for client {clientNumber+1}...")
    request = ("GET /notFound.html HTTP/1.1\r\n" + 
                "Host: " + str(SERVER_NAME) + ":" + str(SERVER_PORT) + "\r\n")
    serverResponse = client_connection(request)
    # validate response
    expectedResult = "404"
    response = serverResponse.decode().split(" ")
    status = "PASS" if response[1] == expectedResult else "FAIL"
    results[clientNumber][7] = {"status": status, "time": time.time()}


# Description: Execute all test cases in a sequential order since the server
#               is singly-threaded
def server_tests(results, clientNumber, numberOfClients):
    tests = [1, 2, 3, 4, 5, 6, 7, 8]
    while len(tests) != 0:
        time.sleep(random.randint(0, numberOfClients))
        testCase = random.choice(tests)
        if testCase == 1:
            server_test_1(results, clientNumber)
        elif testCase == 2:
            server_test_2(results, clientNumber)
        elif testCase == 3:
            server_test_3(results, clientNumber)
        elif testCase == 4:
            server_test_4(results, clientNumber)
        elif testCase == 5:
            server_test_5(results, clientNumber)
        elif testCase == 6:
            server_test_6(results, clientNumber)
        elif testCase == 7:
            server_test_7(results, clientNumber)
        elif testCase == 8:
            server_test_8(results, clientNumber)
        tests.remove(testCase)



# Description: Run the server
def run_server():
    start_server()



if __name__ == "__main__":
    numberOfClients = input("Number of clients: ")
    try:
        numberOfClients= int(numberOfClients)
    except ValueError:
        print("Input must be a number!")
        exit(1)
    if numberOfClients < 1:
        print("There must be at least 1 client!")
        exit(1)
    else:
        expectedCode = [200, 200, 200, 200, 200, 200, 400, 404] # expected codes for test cases
        max_runtime = len(expectedCode) * numberOfClients * numberOfClients
        if numberOfClients == 1:
            max_runtime *= 2
        with Manager() as manager:

            results = []
            for i in range(numberOfClients):
                testResults = manager.dict()   # dictionary of test case results
                results.append(testResults)            

            print("Executing tests...")
            run = Process(target=run_server) # process to run the server
            run.start()

            p = []
            for clientNumber in range(numberOfClients):
                p.append(Process(target=server_tests, args=(results, clientNumber, numberOfClients, ))) # process to execute test cases
            
            for process in p:
                process.start()
            
            time.sleep(max_runtime)
            
            for process in p:
                if process.is_alive():
                    process.terminate()
                process.join()

            run.terminate()
            run.join()

            print("\n#################################################################################")
            print("#                                  TEST RESULTS                                 #")
            print("#                                                                               #")
            for index in range(len(expectedCode)):
                for testResult in range(numberOfClients):
                    s = results[testResult][index]['status']
                    t = results[testResult][index]['time']
                    print(f"#\tTest {index+1} [Client-{testResult+1}] ({expectedCode[index]}):\t {s}\t[{time.ctime(t)}]\t#")
                print("#                                                                               #")
            print("#################################################################################\n")