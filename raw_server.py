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
	BUF_SIZE = int(raw_input("\nEnter the desired Buffer size: "))
	sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(eth_type))
	sock.bind((interface, 0))
	while True:
		packet = sock.recv(BUF_SIZE)
		hexdump(packet)
		if not packet: 
			break
		sock.sendall(packet)

if __name__ == '__main__':
	main()