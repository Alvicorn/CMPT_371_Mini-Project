# Web Proxy Documentation

## Q1:  What is different in request handling in a proxy server and a web server that hosts your files?

* satisfy client request without involving the origin web server
* reduce response time from server to client and reduce traffic to origin server

## Specifications of our Web Proxy Server
* Conditional GET
* A database of sorts to managed lasted update time, existence and capacity
### If hit...
return to client
### If miss ...
request from origin server and save in the cache. If cache is full, evict the oldest request. Finally, send request back to client