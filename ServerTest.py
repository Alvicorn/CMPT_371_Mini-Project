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

TIMEOUT = 5 # second

test1Result = "FAIL"

# Description: Send a request for test.html. File should be found (200)
def server_test_1(testResults):
    request = ("GET /test.html HTTP/1.1\r\n" + 
                "Host: localhost:12000\r\n")

    # Specify Server Address
    serverName = 'localhost'
    serverPort = 12000

    # Create TCP Socket for Client
    clientSocket = socket(AF_INET, SOCK_STREAM)

    # Connect to TCP Server Socket
    clientSocket.connect((serverName,serverPort))

    # Send! No need to specify Server Name and Server Port! Why?
    clientSocket.send(request.encode())
    
    # Read reply characters! No need to read address! Why?
    serverResponse = clientSocket.recv(1024)

    # buffer to allow time for the server to close
    time.sleep(1)

    # Close the socket
    clientSocket.close()

    # validate response
    expectedResult = "200"
    response = serverResponse.decode().split(" ")
    testResults[0] = "PASS" if response[1] == expectedResult else "FAIL"
    




def run_server():
    start_server()


if __name__ == "__main__":
    with Manager() as manager:
        testResults = manager.dict()

        print("Executing tests... Please wait...")
        run = Process(target=run_server)
        test1 = Process(target=server_test_1, args=(testResults,))
        test1.start()
        run.start()

        test1Terminated = "NO"

        time.sleep(TIMEOUT)
        if (test1.is_alive()):
            test1.terminate()
            test1Terminated = "YES"
        run.terminate()
        run.join()
        run.join()

        print("#########################################")
        print("#              TEST RESULTS             #")
        print("#                                       #")
        print("#\tTest 1 terminated?:\t" + test1Terminated + " \t#")
        print("#\tTest 1 Complete?:\t" + testResults[0] + "\t#")
        print("#########################################\n")