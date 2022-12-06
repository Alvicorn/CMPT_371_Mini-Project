# Mini Project: Web & Proxy Web Server 

## Notes
* Server port is on 12001
* Proxy port is 12001
* Multi-threaded server is on 12002
* Develped with Python 3.9



## **Task 1: Implement the Web Server**
Create a simple web server using socket programming that follows the HTTP protocol. The web server will handle the following HTTP request one at a time:

Code | Message           | Done |
-----|-------------------|------|
200  | OK                | Yes  |
400  | Bad Request       | Yes  |
404  | Not Found         | Yes  |
408  | Request Timed Out | Yes  |

### <u>Relevant Files</u>
* *Files* folder
* ```Server.py```
* ```TestServer.py```

### <u>Testing</u>
Note: Ensure the web server is running on port 12000 before testing

#### <mark>200</mark>
Type the following into a web browser
```
http://IP_ADDRESS:12000/test.html
```
* **Expected Response:** OK

* **Done:** Yes
* **Notes:** N/A

#### <mark>400</mark>
Type the following into a web browser
```
http://IP_ADDRESS:12000/test.htm
```
* **Expected Response:** Bad Request

* **Done:** Yes
* **Notes:** N/A

#### <mark>404</mark>
Type the following into a web browser
```
http://IP_ADDRESS:12000/notFound.html
```
* **Expected Response:** Not Found

* **Done:** Yes
* **Notes:** Do not make a file in the root directory named notFound.html


#### <mark>408</mark>
Type the following into a web browser
```
http://IP_ADDRESS:12000/test.html
```
* **Expected Response:** Request Timed Out

* **Done:** Yes
* **Notes:** N/A


## **Task 2: Implement the Web Proxy Server**
Hint: Module 2, slides 29-34

### <u>Specifications</u> 
* Cache size of 5
* Cache info and files are stored inside a folder named "Cache"
* When running the proxy, ensure the the main server is also running so that the proxy can make requests to the server

### <u>Relevant Files</u>
* *Files* folder
* *Cache* folder - generated when proxy runs
* ```Proxy.py```
* ```Server.py```
* ```TestProxy.py```
* ```WebProxySpecs.md```

### <u>Testing</u>
Code | Message           | Done |
-----|-------------------|------|
200  | OK                | Yes  |
304  | Not Modified      | No   |
400  | Bad Request       | Yes  |
404  | Not Found         | Yes  |
408  | Request Timed Out | NO   |


### Testing
Note: Ensure the web server is running on port 12000 before testing

#### <mark>200</mark>
Type the following into a web browser
```
http://IP_ADDRESS:12001/test.html
```
* **Expected Response:** OK

* **Done:** Yes
* **Notes:** N/A

#### <mark>304</mark>
Type the following into a web browser
```

```
* **Expected Response:** Not Modified

* **Done:** No
* **Notes:** N/A

#### <mark>400</mark>
Type the following into a web browser
```
http://IP_ADDRESS:12001/test.htm
```
* **Expected Response:** Bad Request

* **Done:** Yes
* **Notes:** N/A

#### <mark>404</mark>
Type the following into a web browser
```
http://IP_ADDRESS:12001/notFound.html
```
* **Expected Response:** Not Found

* **Done:** Yes
* **Notes:** Do not make a file in the root directory named notFound.html


#### <mark>408</mark>
Type the following into a web browser
```

```
* **Expected Response:** Request Timed Out

* **Done:** No
* **Notes:** N/A

## **Bonus Task: Multi-Treaded Web Server**
Create a multi-threaded web server using socket programming that follows the HTTP protocol. The web server will handle the following HTTP requests:

Code | Message           | Done |
-----|-------------------|------|
200  | OK                | Yes  |
400  | Bad Request       | Yes  |
404  | Not Found         | Yes  |
408  | Request Timed Out | No   |

### <u>Relevant Files</u>
* *Files* folder
* ```MultiThreadServer.py```
* ```TestMultiThreadServer.py```

### <u>Testing</u>
When testing in the browser, ensure the server is running on port 12002

When testing with ```MultiThreadServer.py```, ensure port 12002 is available. This test may take a while.

#### <mark>200</mark>
Type the following into a web browser
```
http://IP_ADDRESS:12000/test.html
```
* **Expected Response:** OK

* **Done:** Yes
* **Notes:** N/A

#### <mark>400</mark>
Type the following into a web browser
```
http://IP_ADDRESS:12000/test.htm
```
* **Expected Response:** Bad Request

* **Done:** Yes
* **Notes:** N/A

#### <mark>404</mark>
Type the following into a web browser
```
http://IP_ADDRESS:12000/notFound.html
```
* **Expected Response:** Not Found

* **Done:** Yes
* **Notes:** Do not make a file in the root directory named notFound.html


#### <mark>408</mark>
Type the following into a web browser
```
http://IP_ADDRESS:12000/test.html
```
* **Expected Response:** Request Timed Out

* **Done:** Yes
* **Notes:** N/A

