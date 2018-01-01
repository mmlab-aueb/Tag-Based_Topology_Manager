from socket import *
from pox.lib.packet import ethernet,ipv6
from pox.lib.addresses import IPAddr6,EthAddr 

s = socket(AF_PACKET, SOCK_RAW, htons(0x0003) )
s.bind(('h2-eth0', 0))
ether = ethernet()
data = s.recv(2048)
ether.parse(data)
ipv6 = ether.payload
print ipv6.payload
