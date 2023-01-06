# Web Proxy Documentation

## What is different in request handling in a proxy server and a web server that hosts your files?

When handling requests in a proxy server, it is generally, faster because the proxy server is closer to the end user compared to the web sever. Therefore, it is able to respond faster and reduce traffic at the web server.


## Specifications of our Web Proxy Server
* Conditional GET
* A database of sorts to managed lasted update time, existence and capacity
### If cache **hit**...
respond to the client's request as a server.

client --> proxy --> client

### If cache **miss** ...
send a request to the web server for the client's request. If there is a negative response from the web server, redirect the message to the client. Otherwise, save the data from the response in the cache. If the cache is full, evict the oldest data member. Finally, send the data as a response back to the client.

client --> proxy --> web server --> proxy --> client