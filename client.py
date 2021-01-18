import OpenSSL
import socket as soct
import ssl
from cryptography.fernet import Fernet
import base64
import sys
import hashlib

def sendMessage(message,socket):
	socket.send(message)  


def connectToServer(IP, Port):                   
	try:
		#print("a")
		clientSocket = soct.socket()
		clientSocket.connect((IP,Port)) 
		
	except ConnectionRefusedError:
		print("Could not connect to the server")
		clientSocket = None
	return clientSocket

message=""
serverIP = '127.0.0.1'
serverPort = 8000
socket = connectToServer(serverIP, serverPort)
while True and message.lower()!="bye":
	
	if not socket:
		sys.exit()
	message = input("Enter message for server: ")
	key1= hashlib.sha256()
	key1.update(soct.gethostname().encode('utf-8'))
	key2=key1.hexdigest()
	key2=key2[:32]
	key3=base64.b64encode(key2.encode('utf-8'))
	cipher_suite = Fernet(key3) 

	encoded_text = cipher_suite.encrypt(message.encode('utf-8'))
	if message.lower()!="bye":
		sendMessage(encoded_text,socket)
		recieved=socket.recv(1024).decode("utf-8")
		decrpyted=cipher_suite.decrypt(recieved.encode('utf-8'))
		print(">>Message sent from server: ",decrpyted.decode('utf-8'))
	else:

		socket.close()

