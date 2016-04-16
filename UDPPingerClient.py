# UDPPingerClient.py
# include Python's socket library
import time
from datetime import datetime
#import socket
from socket import *

sent = 0;
received = 0;
mintime = 9999;
maxtime = 0;
totaltime = 0;

# client sents 10 pings to the server
for sequence_number in range(10):
    # Create UDP socket for server
    # Notice the use of SOCK_DGRAM for UDP packets
    clientSocket = socket(AF_INET, SOCK_DGRAM)

    # If no reply is received within one second, then timeout since we assume
    # that the packet was lost during transmission across the network
    clientSocket.settimeout(1)

    # Random message, server name, and server port to send to
    # Note that localhost's IP is 127.0.0.1
    message = "ping the server!"
    serverName = '127.0.0.1'
    serverPort = 12000

    # Start timer and attach server name, port to message and send into socket
    starttime = time.time()
    clientSocket.sendto('[%s]' % (datetime.now()),(serverName, serverPort))

    # Counts the total number of pings sent
    sent = sent + 1
    
    try:
        # Read reply characters from socket into string
        message, serverAddress = clientSocket.recvfrom(1024)
        
        # End timer
        endtime = time.time()

        # Calculate the round trip time(RTT) if server responds
        elapsedtime = endtime - starttime
        
        # Print out received string
        print '%s %.6fms' % (message, elapsedtime*1000)

        # Count the number of successful pings
        received = received + 1

        # Save the min, max and total time
        if(elapsedtime < mintime):
            mintime = elapsedtime
        if(elapsedtime > maxtime):
            maxtime = elapsedtime
        totaltime = totaltime + elapsedtime
        
    except timeout:
        # Time out if no reply is received within one second
        print 'The request timed out!'

# Print out the packets sent, received and lost as well as the packet loss %
print '\nPing statistics: \n Packets: Sent = %d, Received = %d, Lost = %d (%d' % (sent, received, sent - received, (sent - received)*100/sent) + '% loss)'

# Print out the min max and average round trip times (RTT)
print '\nApproximate round trip times in milli-seconds:\n Minimum = %.6fms, Maximum = %.6fms, Average = %.6fms' % (mintime*1000, maxtime*1000, totaltime*1000/received)

# Close the socket
clientSocket.close()
