from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.log import setLogLevel, info
import json
class TopoByConf( Topo ):
    "Simple topology example."

    def __init__( self ):
        "Create custom topo from Configuration.json File ."

        # Initialize topology
        with open('/home/user/Desktop/pox/pox/misc/Configuration.json') as data_file:
            data = json.load(data_file)

        Topo.__init__( self )


        # Add hosts and switches
        info('*** Adding Hosts\n')
        for h in data['hosts']:
            h = self.addHost(str(h), ip = data['hosts'][h]['ip'], mac = data['hosts'][h]['mac'])
        info('*** Adding Switches\n')
        for s in data['switches']:
            s = self.addSwitch(str(s))
        info('Adding Links\n')

        # Add links
        for l in data['link']:

            l = self.addLink(data['link'][l]['connection'][0],data['link'][l]['connection'][1], data['link'][l]['ports'][0],data['link'][l]['ports'][1])



topos = { 'topobyconf': ( lambda: TopoByConf() ) }