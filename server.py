import socket
import sys
import ConfigParser
import mido

pins_state = [False] * 40

Config = ConfigParser.ConfigParser()
Config.read("server_config.ini")

ServerIpAddress = Config.get('ServerConfigurartion', 'IpAddress')
ServerPort = Config.get('ServerConfigurartion', 'Port')

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print "opening midi port"
outport = mido.open_output('VMPK Input:in 128:0')

# Bind the socket to the port
server_address = (ServerIpAddress, int(ServerPort))
print  'starting up on %s port %s' % server_address
sock.bind(server_address)



while True:
	print 'waiting to receive message'
	data, address = sock.recvfrom(4096)
    
	print 'received %s bytes from %s' % (len(data), address)
	data_vec = []
	data_vec = data.split(' ')
	Name = data_vec[0]
	pin = int(data_vec[2])
	
	print Name + " " + str(pin)
	
	outport.send(mido.Message('note_on', note=(72 + pin)))
	
    
	if data:
		sent = sock.sendto(data, address)
		print 'sent %s bytes back to %s' % (sent, address)

