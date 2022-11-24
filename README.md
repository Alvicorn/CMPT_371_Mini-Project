# Mini Project: Web & Proxy Web Server 

***Server port is 12000***


## **Task 1: Implement the Web Server**
Create a simple web server using socket programming that follows the HTTP protocol. The web server will handle the following HTTP request one at a time:

Code | Message           | Done |
-----|-------------------|------|
200  | OK                | Yes  |
304  | Not Modified      | NO   |
400  | Bad Request       | NO   |
404  | Not Found         | Yes  |
408  | Request Timed Out | NO   |


### Testing
Note: Ensure the web server is running on port 12000 before testing

#### <mark>200</mark>
Type the following into a web browser
```
http://IP_ADDRESS:12000/test.html
```
* **Expected Response:** OK

* **Done:** Yes
* **Notes:** N/A

#### <mark>304</mark>
Type the following into a web browser
```

```
* **Expected Response:** Not Modified [cache]

* **Done:** No
* **Notes:** N/A

#### <mark>400</mark>
Type the following into a web browser
```

```
* **Expected Response:** Bad Request

* **Done:** No
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

```
* **Expected Response:** Request Timed Out

* **Done:** No
* **Notes:** N/A


## **Task 2: Implement the Web Proxy Server**
Hint: Module 2, slides 29-34

### Specifications: 

### Testing


## **Bonus Task: Multi-Treaded Web Server**