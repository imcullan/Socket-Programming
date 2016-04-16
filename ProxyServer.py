from socket import *
import sys

if len(sys.argv) <= 1:
    print 'Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address of Proxy Server'
    #sys.exit(2)

# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)
# Fill in start.
tcpSerPort = 12003
tcpSerSock.bind(('localhost', tcpSerPort))
tcpSerSock.listen(5)
# Fill in end.
while 1:
    # Start receiving data from the client
    print 'Ready to serve...'
    # Accept connection from client
    tcpCliSock, addr = tcpSerSock.accept()
    print 'Received a connection from:', addr
    # Get and print the message we received from the client
    message = tcpCliSock.recv(1024)
    if not message:
        message = "I think the connection might have closed..."
        tcpCliSock.close()
        continue
    print message

    # Extract the filename from the given message
    print message.split()[1]
    filename = message.split()[1].partition("/")[2]
    print filename
    fileExist = "false"
    filetouse = "/" + filename
    print filetouse
    try:
        # Check whether the file exist in the cache
        # Try to open the file and return an object of that file type to f, "r" means just to read it
        f = open(filetouse[1:], "r")
        # readlines() will read all the lines of the file f until EOF and returns a list containing all the lines
        outputdata = f.readlines()
        fileExist = "true"
        # ProxyServer finds a cache hit and generates a response message
        tcpCliSock.send("HTTP/1.0 200 OK\r\n")
        tcpCliSock.send("Content-Type:text/html\r\n")
        # Fill in start.
        # Since outputdata is a list containing all the lines, we need to send every line to the client; len() is used to get the length of the list
        for i in range(0, len(outputdata)):
            tcpCliSock.send(outputdata[i])
        # Fill in end.
        print 'Read from cache'
        f.close()
        
    #Error handling for file not found in cache
    except IOError:
        if fileExist == "false":
            # Create a socket on the proxy server
            print 'Creating a socket on the proxy server....'
            # Fill in start.
            c = socket(AF_INET, SOCK_STREAM)
            # Fill in end.
            hostn = filename.replace("www.","", 1)
            print hostn
            try:
                # Connect to the socket to port 80                
                # Fill in start.
                c.connect((hostn,80))
                print "The socket is connected to the host at port 80!"
                # Fill in end.
                
                # Create a temporary file on this socket and ask port 80 for the
                # file requested by the client
                fileobj = c.makefile('r', 0)
                fileobj.write("GET " + "http://" + filename + " HTTP/1.0\n\n")
                naming = bytes(fileobj, 'utf-8')
                c.send(fileobj)

                # Read the response into buffer
                # Fill in start.
                # readlines() will read all the lines of the file fileobj until EOF and returns a list containing the lines
                buffer = fileobj.readlines()
                # Fill in end.
                
                # Create a new file in the cache for the requested file.
                # Also send the response in the buffer to client socket
                # and the coresponding file in the cache
                tmpFile = open("./" + filename, "wb")
                # Fill in start.
                for i in range(0, len(buffer)):
                    tempFile.write(buffer[i]) #write the response from the buffer into the cache (temp file)
                    tcpCliSock.send(buffer[i]) #send the response in the buffer to the client socket
                # Fill in end.

                tmpFile.close()
            except: 
                print "illegal request"
            else:
                # HTTP response message for file not found
                # Fill in start.
                  print "Sorry the file was not found!"
                # Fill in end.
        # Close the client and the server sockets
    tcpCliSock.close()
# Fill in start.
tcpSerSock.close()
# Fill in end.
