#pip install inputs 
# python 2.7

#RT right rotation
#LT left rotation
#B - terminate
#Right Joystic - Horizontal Speed
#Left Joystic - Vertical Speed

from inputs import get_gamepad

while 1:
	events = get_gamepad()
	for event in events:
		print(event.ev_type, event.code, event.state)