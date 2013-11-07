#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel

class ITATopo(Topo):
    "Single switch connected to n hosts."
    def __init__(self, numdiv=3, numhostsdiv=3, **opts):
	cpumax = .5/(numdiv*numhostsdiv+2) #divide a potencia da CPU pelo numero total de hosts
        Topo.__init__(self, **opts)
        self.switch_core = self.addSwitch('s0', ip='161.24.0.1/24')
	self.s1 = self.addSwitch('s1', ip='161.24.0.2/24')
	self.s2 = self.addSwitch('s2', ip='161.24.0.3/24')
	self.s3 = self.addSwitch('s3', ip='161.24.0.4/24')
	self.h0 = self.addHost('h0', vcpu=cpumax, ip='161.24.0.5/24')
	self.h1 = self.addHost('h1', vcpu=cpumax, ip='161.24.0.6/24')


	self.addLink(self.switch_core, self.s1, bw=100, delay='5ms', loss=10, max_queue_size=1000, use_htb=True)
	self.addLink(self.switch_core, self.s3, bw=100, delay='5ms', loss=10, max_queue_size=1000, use_htb=True)
	self.addLink(self.s1, self.s2, bw=100, delay='5ms', loss=10, max_queue_size=1000, use_htb=True)
	self.addLink(self.s1, self.h0, bw=100, delay='5ms', loss=10, max_queue_size=1000, use_htb=True)
	self.addLink(self.s3, self.h1, bw=100, delay='5ms', loss=10, max_queue_size=1000, use_htb=True)

def topoTest():
    "Create network and run simple performance test"
    topo = ITATopo()
    #topo = ITATopo(12, 10)
    net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink)
    
    net.interact()
#    net.start()
#    print "Dumping host connections"
#    dumpNodeConnections(net.hosts)
#    print "Testing network connectivity"
#    net.pingAll()
#    print "Testing bandwidth between h1 and h4"
#    h1, h4 = net.get('h1', 'h4')
#    net.iperf((h1, h4))
#    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    topoTest()
