import socket

from inputs import get_gamepad

def Main():
	host = '127.0.0.1'
	port = 5000

	mySocket = socket.socket()
	mySocket.connect((host, port))

#	getch = getchar.getch
	
	ABS_RX=0;

	while 1:
	
		events = get_gamepad()
		for event in events:
			if(event.code=="ABS_RX"):
				ABS_RX+=int(event.state)
				print(str(event.state) +" "+str(ABS_RX))
			mySocket.send( str(str(event.ev_type) +" "+ str(event.code)+" "+str(event.state)).encode())
		
		data = mySocket.recv(1024).decode()

		#print('Recieved fron server: ' + data)


	mySocket.close()

if __name__ == '__main__':
	Main()