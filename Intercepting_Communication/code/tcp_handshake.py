#!/usr/bin/env python

from scapy.all import *
import socket

HOST_IP  = '10.0.0.3'
SPORT    = 31337
DPORT    = 31337
INIT_SEQ = 31337

def initial_SYN():
    global HOST_IP
    global SPORT
    global DPORT
    global INIT_SEQ
    eth = Ether(dst = 'ff:ff:ff:ff:ff:ff', src = get_if_hwaddr('eth0'))
    ip = IP(dst = HOST_IP, src = get_if_addr('eth0'))
    tcp = TCP(sport=SPORT, dport=DPORT, seq=INIT_SEQ, flags='S')
    pkt = eth / ip / tcp
    sendp(pkt, iface = 'eth0')

def handshake(packet):
    global HOST_IP
    global SPORT
    global DPORT
    if(TCP in packet):
        print("Got TCP")
        packet.show()
        if(packet[TCP].flags == 'SA'):
            eth = Ether(dst = 'ff:ff:ff:ff:ff:ff', src = get_if_hwaddr('eth0'))
            ip = IP(dst = HOST_IP)
            seq2 = packet[TCP].ack
            ack2 = packet[TCP].seq + 1
            tcp = TCP(sport=SPORT, dport=DPORT, seq=seq2, ack=ack2, flags='A')
            pkt = eth / ip / tcp
            sendp(pkt, iface = 'eth0')
        
        # if the kernel sends an RST packet, we resend the SYN
        if(packet[TCP].flags == 'R'):
            initial_SYN()

def sniffing_function():
    sniff(iface = 'eth0', prn = handshake)

# this is to prevent the kernel from sending RST packet
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
sock.bind(('0.0.0.0', 31337))
sock.listen(100)

# start the sniffing function first (in a new thread)
# this ensures that we can capture all packets after sending the SYN packet
sniff_thread = threading.Thread(target=sniffing_function)
sniff_thread.start()

initial_SYN()
