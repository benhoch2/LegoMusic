import ConfigParser
import sys
import socket
import RPi.GPIO as GPIO  
from time import sleep    

input_pins = [10, 12, 14, 16, 18]
pins_status = [False] * 40
correction_loop = True

def output_change_cb(channel):
	if GPIO.input(channel):
		print "Rising edge detected on " + str(channel)
		pins_status[pin] = True
	else:
		print "Falling edge detected on " + str(channel) 
		pins_status[pin] = False
	
	update_status(pin, GPIO.input(channel))

def update_status(pin, state):
	message = "pin " + str(pin) + " is now "
	if state:
		message = message + "UP"
	else:
		message = message + "DOWN"
		
	sock.sendto(message.encode('utf-8'), (ServerIpAddress, int(ServerPort)))


print "reading configuration"
Config = ConfigParser.ConfigParser()
Config.read("client_config.ini")

ServerIpAddress = Config.get('ServerConfiguration', 'IpAddress')
ServerPort = Config.get('ServerConfiguration', 'Port')

print "setting pins"

GPIO.setmode(GPIO.BCM)   
for pin in input_pins:
	pins_status[pin] = False
	print "setting pin " + str(pin) + " as input"
	GPIO.setup(pin, GPIO.IN)
	print "setting callback for " + str(pin)
	GPIO.add_event_detect(pin, GPIO.BOTH, callback=output_change_cb) 

print "creating socket"
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)



try:  
	while correction_loop:
		for pin in input_pins:
			if GPIO.input(pin) != pins_status[pin]:
				print "correcting state of pin " + str(pin) + " to " + str(GPIO.input(pin))
				pins_status[pin] = GPIO.input(pin)
				 

			
		sleep(1)
		
except KeyboardInterrupt:         
    GPIO.cleanup()               
