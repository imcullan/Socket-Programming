# UDPPingerServer.py
# We will need the following module to generate randomized lost packets
import random
from socket import *
from datetime import datetime

# Create a UDP socket
# Notice the use of SOCK_DGRAM for UDP packets
serverSocket = socket(AF_INET, SOCK_DGRAM)

#Assign IP address and port number to socket
serverSocket.bind(('', 12000))

while True:
    # Generate random number in the range of 0 to 10
    rand = random.randint(0,10)

    print 'waiting for mesage...'
    
    # Receive the client packet along with the address it is coming from
    message, address = serverSocket.recvfrom(1024)
    receivedtime = datetime.now()
    # Capitalize the message from the client
    # message = message.upper()
    clientsenttime = datetime.strptime(message, "[%Y-%m-%d %H:%M:%S.%f]")
    #print senttime
    #print receivedtime
    timedifference = receivedtime - clientsenttime
    
    # If rand is less than 4, we consider the packet lost and do not respond
    if rand < 4:
        print "Client's heart stopped!"
        continue
    
    # Otherwise, the server responds
    serverSocket.sendto(message, address)
    print 'Client sent message: %s' % (message) + '\nServer received message: [%s]' % (receivedtime) + '\nTime Difference = %sms' % (timedifference.microseconds/1000) + '\nServer sent message: [%s]' % (datetime.now())
    
