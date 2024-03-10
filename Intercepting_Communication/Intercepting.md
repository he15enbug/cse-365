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
- *level 11*: 
- *level 12*: 
- *level 13*: 
- *level 14*: 