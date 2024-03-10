#!/usr/bin/env python

from scapy.all import *

res_str = ''

def sniff_pkt(packet):
    global res_str
    if TCP in packet:
        if Raw in packet:
            data = packet[Raw].load
            res_str = res_str + data.decode('utf-8')
            print(res_str)

# Sniff packets
sniff(iface='eth0', filter='tcp and dst port 31337', prn=sniff_pkt, count=200)
