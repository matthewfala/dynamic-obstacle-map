import socket
import copy

from inputs import get_gamepad
def axisScale(raw,deadzone):
	if abs(raw) < deadzone:
		return 0.0
	else:
		if raw < 0:
			return (raw + deadzone) / (32768.0 - deadzone)
		else:
			return (raw - deadzone) / (32767.0 - deadzone)


def rScale(raw,deadzone):
	if abs(raw) < deadzone:
		return 0.0
	else:
		if raw < 0:
			return (raw + deadzone) / (255.0 - deadzone)
		else:
			return (raw - deadzone) / (255.0 - deadzone)

def Main():
	host = '127.0.0.1'
	port = 5000

	mySocket = socket.socket()
	mySocket.connect((host, port))

#	getch = getchar.getch
	
	values={"ABS_RY":0,"ABS_Y":0,"ABS_RZ":0,"ABS_Z":0,"BTN_EAST":0}
	mapping={"ABS_RY":"horizontal","ABS_Y":"depth","ABS_RZ":"rotate_right","ABS_Z":"rotate_left","BTN_EAST":"kill"}
	while 1:
	
		events = get_gamepad()
		valuesTmp=copy.copy(values);
		for event in events:
			if(event.code=="ABS_RY"):
				value=axisScale(event.state,4000)
				valuesTmp[event.code]=value;
			if(event.code=="ABS_Y"):
				value=axisScale(event.state,4000)
				valuesTmp[event.code]=value;
			if(event.code=="ABS_RZ"):
				value=rScale(event.state,50)
				valuesTmp[event.code]=value;
			if(event.code=="ABS_Z"):
				value=rScale(event.state,50)
				valuesTmp[event.code]=value;	
			if(event.code=="BTN_EAST"):
				value=event.state
				valuesTmp[event.code]=value;
		isDifferent=False
		for value in values:
			if values[value] != valuesTmp[value]:
				isDifferent=True
				break
		if isDifferent:
			mySocket.send( str(valuesTmp).encode())
			values=valuesTmp


	mySocket.close()

if __name__ == '__main__':
	Main()