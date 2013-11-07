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
        switch_core = self.addSwitch('s0', ip='161.24.0.1/24')
	switch_segundo_core = self.addSwitch('s1', ip='161.24.0.2/24')
	switch_comp = self.addSwitch('s2', ip='161.24.0.3/24')
	h0 = self.addHost('h0',vcpu=cpumax,ip='161.24.0.4/24')
	host_externo = self.addHost('h9999', vcpu=cpumax, ip='8.8.8.8/0')
	gateway_cta = self.addHost('h1000', vcpu=cpumax, ip='161.24.0.5/16')


	self.addLink(gateway_cta, switch_core,
			   bw=100, delay='5ms', loss=10, max_queue_size=1000, use_htb=True)
	self.addLink(gateway_cta, host_externo,
			   bw=20, delay='1s', loss=10, max_queue_size=1000, use_htb=True)
	self.addLink(switch_core, switch_segundo_core,
			   bw=20, delay='1s', loss=10, max_queue_size=1000, use_htb=True)
	self.addLink(switch_segundo_core, switch_comp,
			   bw=20, delay='1s', loss=10, max_queue_size=1000, use_htb=True)
	self.addLink(switch_comp, h0,
			   bw=20, delay='1s', loss=10, max_queue_size=1000, use_htb=True)

def addRoutes(net, numdiv=3, numhostsdiv=3):
	for h in net.hosts:
		num = int(h.name[1:])
		h.cmd('sysctl net.ipv4.ip_forward=1') #https://gist.github.com/lantz/5640610

		if num == 9999:
		    h.cmd('ip r add default dev h9999-eth0')
		elif num == 1000:
		    h.cmd('ip r add default dev h1000-eth1')
		else:
		    h.cmd('ip r add default dev h0-eth1')

def topoTest():
    "Create network and run simple performance test"
    topo = ITATopo()
    #topo = ITATopo(12, 10)
    net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink)
    addRoutes(net)
    
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
