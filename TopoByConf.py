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
        for s in data['switches']['names']:
            s = self.addSwitch(str(s))
        info('Adding Links\n')

        # Add links
        for k, v in data['link'].items():

            k = self.addLink(v[0],v[1])



topos = { 'topobyconf': ( lambda: TopoByConf() ) }