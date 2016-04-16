#from socket import *
import socket 
import base64 #used to encode username and password

msg = "\r\n I love computer networks!"
endmsg = "\r\n.\r\n"

# Choose a mail server (e.g. Google mail server) and call it mailserver
# gmail's SMTP server name is smtp.gmail.com and their port is 587(TLS required)
mailserver = ('smtp.gmail.com', 587)

# Create socket called clientSocket and establish a TCP connection with mailserver
# Notice that SOCK_STREAM is for a TCP connection
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect(mailserver)
print "connecting to mail server"
recv = clientSocket.recv(1024)
print(recv)
if recv[:3] != '220':
    print '220 reply not received from server.'

# Sent HELO command and print server response.
print "sending HELO command"
clientSocket.send('HELO Alice\r\n')
recv1 = clientSocket.recv(1024)
print(recv1)
if recv1[:3] != '250':
    print '250 reply not received from server.'

# Request an encrypted connection.
print "request to add TLS (Transport Layer Security)"
clientSocket.send('STARTTLS\r\n')
TLSrecv = clientSocket.recv(1024)
print (TLSrecv)
if TLSrecv[:3] != '220':
    print '220 reply not received from server.'

# Encrypt the socket using SSL.
print "encrypting the client socket using SSL"
SSLclientSocket = socket.ssl(clientSocket)

# Send the AUTH LOGIN command and print server response.
SSLclientSocket.write('AUTH LOGIN\r\n')
auth_recv = SSLclientSocket.read(1024)
print (auth_recv)
if auth_recv[:3] != '334':
    print '334 reply not received from server.'

# Encode and send username and print server response.
username = "cullan.liang@nspire.org"
encodedusername = base64.b64encode(username) + '\r\n'
SSLclientSocket.write(encodedusername)
username_recv = SSLclientSocket.read(1024)
print username_recv
if username_recv[:3] != '334':
    print '334 reply not received from server.'

# Encode and send password and print server response.
password = "<mypassword>"
encodedpassword = base64.b64encode(password) + '\r\n'
SSLclientSocket.write(encodedpassword)
password_recv = SSLclientSocket.read(1024)
print password_recv
if password_recv[:3] != '235':
    print '235 reply not received from server.'

# Send MAIL FROM command and print server response.
print "sending MAIL FROM command"
SSLclientSocket.write("MAIL FROM: <cullan.liang@nspire.org>\r\n")
recv2 = SSLclientSocket.read(1024)
print (recv2)
if recv2[:3] != '250':
    print '250 reply not received from server.'

# Second RCPT TO command and print server response.
print "sending RCPT TO command"
SSLclientSocket.write("RCPT TO: <cullan.liang@hotmail.com>\r\n")
recv3 = SSLclientSocket.read(1024)
print(recv3)
if recv3[:3] != '250':
    print '250 reply not received from server.'

# Send DATA command and print server response.
print "sending DATA command"
SSLclientSocket.write("DATA\r\n")
recv4 = SSLclientSocket.read(1024)
print(recv4)
if recv4[:3] != '250':
    print '250 reply not received from server.'

# Send message data
print "sending message data"
SSLclientSocket.write(msg)

# Message ends with a single period.
print "sending end message data"
SSLclientSocket.write(endmsg)
recv5 = SSLclientSocket.read(1024)
print(recv5)
if recv5[:3] != '250':
    print '250 reply not received from server.'

# Send QUIT command and get server response.
print "sending QUIT command"
SSLclientSocket.write("QUIT\r\n")
recv6 = SSLclientSocket.read(1024)
print(recv6)
if recv6[:3] != '250':
    print '250 reply not received from server.'

# Close the socket.
clientSocket.close()
