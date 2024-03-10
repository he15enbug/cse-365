#!/usr/bin/env python

from scapy.all import *

def send_Ether():
    pkt = Ether(dst = '1e:5f:b7:14:a6:0e', src = get_if_hwaddr('eth0'), type=0xFFFF)
    sendp(pkt, iface = 'eth0')

def send_IP():
    eth = Ether(dst = 'ff:ff:ff:ff:ff:ff', src = get_if_hwaddr('eth0'))
    ip = IP(dst = '10.0.0.3', proto = 0xFF)
    pkt = eth / ip
    sendp(pkt, iface = 'eth0')

def send_TCP():
    eth = Ether(dst = 'ff:ff:ff:ff:ff:ff', src = get_if_hwaddr('eth0'))
    ip = IP(dst = '10.0.0.3')
    tcp = TCP(sport=31337, dport=31337, seq=31337, ack=31337, flags='APRSF')
    pkt = eth / ip / tcp
    sendp(pkt, iface = 'eth0')
# send_Ether()
# send_IP()
send_TCP()
