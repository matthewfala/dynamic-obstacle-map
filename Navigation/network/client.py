import socket
import getchar

def Main():
	host = '127.0.0.1'
	port = 5000

	mySocket = socket.socket()
	mySocket.connect((host, port))

	getch = getchar.getch

	print('>', end='')
	message = getch()

	while message != 'q':
		mySocket.send(message.encode())
		data = mySocket.recv(1024).decode()

		print('Recieved fron server: ' + data)

		print('>', end='')
		message = getch()

	mySocket.close()

if __name__ == '__main__':
	Main()