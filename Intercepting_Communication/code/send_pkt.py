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

def send_ARP():
    eth = Ether(dst = 'a2:bb:52:d2:69:a5', src = get_if_hwaddr('eth0'))
    arp = ARP(op = 2, psrc = get_if_addr('eth0'), pdst = '10.0.0.3', hwsrc = '86:55:bf:5b:5c:a0') # op: 2 is-at
    pkt = eth / arp
    pkt.show()
    sendp(pkt, iface = 'eth0')

# send_Ether()
# send_IP()
# send_TCP()
# send_ARP()
