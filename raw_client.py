#!/usr/bin/env python
#_*_coding: utf-8_*_

import socket
import fcntl
import struct
import os
from scapy.all import *

#Provides a list of the available interfaces
def interface_list():
	print("\nSelect the desired Ethernet interface: \n")
	return os.system("ifconfig -a | grep \\\'Ethernet\\\'")

#Obtain the host machine MAC address
def host_mac(ifname):
	info = fcntl.ioctl(sock.fileno(), 0x8927, struct.pack('265s', ifname[:15]))
	return ''.join(['%02x:' % ord(char) for char in info[18:24]])[:-1]

"""
Use the Scapy library to create the desired Ethernet packet.

Arguments:

	Ether() -> 
	This layer contains the Destination and Source addresses as
	well as the ethertype of the frame. IF no ethertype is provided, the
	default value is taken as 0x9000.

	Payload ->
	This layer contains the payload or the user data (message) of the frame.

	packet.show() ->
	Generates the detailed view of the generated packet.

	hexdump(packet) ->
	Generates a hexdump of the packet.
"""

def create_eth_packet(destination_mac, source_mac, eth_type, payload):
	packet = Ether(dst=destination_mac, src=source_mac)/payload
	print("\nRAW Ethernet packet created with the following values: \n")
	packet.show()
	return packet

"""
File Descriptor ->
Creates and defines the characteristics of the RAW socket for the client.

Arguments:

	socket.AF_PACKET: socket supports the protocol refferd by the protocol family.
	socket.SOCK_RAW: creates a RAW socket.
	socket.htons: the htons() function converts the unsigned short integer host short 
	from host byte order to network byte order.

Return:
Creates a RAW socket with the above defined properties and binds it to the
selected interface and port using the bind operation from the socket library.
"""

def main():
	interface_list()
	interface = str(raw_input("\nEnter the interface name connected to the server machine: "))
	eth_type = ("\nEnter the desired ethertype value: ")
	sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(eth_type))
	sock.bind((interface, 0))

#Obtain user input to create a RAW Ethernet packet.

	source_mac = host_mac(interface)
	print "\nSource machine MAC address: ", source_mac
	destination_mac = str(raw_input("\nEnter the Destination machine MAC address: "))
	BUF_SIZE = int(raw_input("\nEnter the desired Buffer size: "))
	payload = raw_input("\nEnter the payload data: ")
	packet_count = int(raw_input("\nEnter the total number of packets to be sent: "))
	packet = create_eth_packet(destination_mac, source_mac, eth_type, payload)

#Send the desired number of packets and wait for the server response.

	sendp(packet, iface = interface, count = packet_count)
	print("\nServer response: \n")
	while True:
		response = sock.recv(BUF_SIZE)
		hexdump(response)


if __name__ == '__main__':
	main()