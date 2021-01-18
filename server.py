import OpenSSL
import socket as soct
import sys 
import ssl
from pprint import pprint
import hashlib
import base64
from cryptography.fernet import Fernet

openssl = OpenSSL.crypto
certiFile=open("namasvi.crt").read()
keyFile=open("namasvi.key").read()


x509 = openssl.load_certificate(openssl.FILETYPE_PEM, certiFile)
print(x509.get_subject())


key=openssl.load_privatekey(openssl.FILETYPE_PEM, keyFile)


# server connection
try: 
	serverSocket = soct.socket() 
	print("Socket successfully created")
except soct.error as err: 
	print("Socket creation failed with error",err) 

serverPort = 8000
serverSocket.bind(('127.0.0.1', serverPort))
serverSocket.listen(5)      
print("Socket is listening")
client, addr = serverSocket.accept() 
while True:
	     
	print('Received connection from: ', addr)
	key1= hashlib.sha256()
	key1.update(soct.gethostname().encode('utf-8'))
	key2=key1.hexdigest()
	key2=key2[:32]
	key3=base64.b64encode(key2.encode('utf-8'))
	cipher_suite = Fernet(key3)   
	recieved=client.recv(1024).decode("utf-8")
	decrpyted=cipher_suite.decrypt(recieved.encode('utf-8'))
	print("\n>>Message sent from client: ",decrpyted.decode('utf-8'))
	if(decrpyted.decode('utf-8')=="bye"):
		break
	message=input('Enter message for client: ') 
	encoded_text = cipher_suite.encrypt(message.encode('utf-8'))
	client.send(encoded_text)
