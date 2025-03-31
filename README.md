# UnixSocketExample
Example server and client implementing an Asyncio TCP server forwarding from a Unix socket

# Run
1. Open a terminal and run the server
```
python unix-socket-server.py
```

2. Open another terminal and run the client
```
python unix-socket-client.py
```

# Overview
The client sends a Hello World message over TCP to the TCP socket server.
The TCP server reads the data from its StreamReader and writes it to the Unix Socket.
The Unix server reads the data and writes it back to the Unix socket.
The TCP server reads the data from the Unxi socket and writes it back to the client 

# Example server output:
```
UNIX socket server started at /tmp/asyncio_unix_socket
TCP socket server started at 127.0.0.1:8888
TCP client connected: ('127.0.0.1', 35036)
Received from TCP client: Hello from TCP client!
UNIX client connected: 
Received from UNIX client: Hello from TCP client!
Closing TCP client connection
Closing UNIX client connection
```

# Example client output
```
Sending: Hello from TCP client!
Received: Server received: Hello from TCP client!
Closing TCP client connection...
```
