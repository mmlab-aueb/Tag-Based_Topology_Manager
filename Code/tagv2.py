from pox.core import core
import pox.openflow.nicira as nx
import pox.openflow.libopenflow_01 as of
from pox.lib.addresses import IPAddr6,EthAddr
import networkx as netx
import json
import matplotlib as plt
import os
import matplotlib.pyplot as plt


# Developed by Dimitris Mendrinos

"""
https://openflow.stanford.edu/display/ONL/POX+Wiki
http://flowgrammable.org/sdn/openflow/message-layer/match/#tab_ofp_1_2
"""
log = core.getLogger()

class Tagsv2 (object):

  def __init__ (self,connection):

    topo = TopologyManager()
    self.connection = connection
    connection.addListeners(self)
    l = {}
    print(topo.switches)

    if (connection.eth_addr.toStr() in topo.switches):
      print("Connected")
      for k,v in topo.links.items():
        if connection.eth_addr.toStr() in v:
          i=1
          for k, v in l.items():
            print ('Installing rule for link', k , 'table' ,i )
            msg = nx.nx_flow_mod_table_id()
            connection.send(msg)
            # table 0
            msg = nx.nx_flow_mod()
            msg.table_id = 0
            msg.priority = 1500
            msg.match.of_eth_dst = "00:00:00:00:00:00"
            msg.match.of_eth_type = 0x86dd
            msg.match.of_in_port = v[0]
            msg.actions.append(nx.nx_action_resubmit.resubmit_table(table=0))
            self.connection.send(msg)

            msg = nx.nx_flow_mod()
            msg.table_id = 0
            msg.priority = 1000
            msg.match.of_eth_dst = "00:00:00:00:00:00"
            msg.match.of_eth_type = 0x86dd
            msg.match.nx_ipv6_dst = (IPAddr6("::2"), IPAddr6("::2"))
            msg.actions.append(of.ofp_action_output(port= v[1]))
            msg.actions.append(nx.nx_action_resubmit.resubmit_table(table=0))
            self.connection.send(msg)
            if i!= topo.links.__len__():
              msg = nx.nx_flow_mod()
              msg.table_id = 0
              msg.priority = 500
              msg.match.of_eth_dst = "00:00:00:00:00:00"
              msg.match.of_eth_type = 0x86dd
              msg.actions.append(nx.nx_action_resubmit.resubmit_table(table=1))
              self.connection.send(msg)
              i +=1







class TopologyManager():

  """
  This is a Topology Manager for Software Defined Networks.
  From this Python Program we can extract from a JSON Configuration file
  the topology of a Software Defined Network, collect information and manage
  the network.
  """

  #Dictionaries with information from JSON

  ips = {}
  macs = {}
  switches = []
  links= {}
  linkname = {}
  os.environ['flag'] = 'true'
  Graph = netx.Graph()
  # Create a NetworkX Graph


  #Initialize the Class
  def __init__(self):
    if os.environ['flag'] == 'true':
      self.loadConfig()
      os.environ['flag'] = 'false'
  # In this method we read the Topology from Json file and
  # create a Graph from it.
  def loadConfig(self):

    with open(os.path.expanduser('/home/user/Desktop/pox/pox/misc/Configuration.json')) as data_file:
      data = json.load(data_file)
    for i in data['hosts']:
      self.ips[i] = data['hosts'][i]['ip']
      self.macs[i] = data['hosts'][i]['mac']
      self.Graph.add_node(i,color = data['hosts'][i]['color'])
    for s in data['switches']:
      self.Graph.add_node(s, mac  = data['switches'][s])
      self.switches.append(data['switches'][s])
    for l in data['link']:
      self.Graph.add_edge(data['link'][l]['connection'][0],data['link'][l]['connection'][1],name = l)
      self.links[l] = [data['link'][l]['ports'][0] ,data['link'][l]['ports'][1]]
      self.linkname[l] = data['link'][l]['connection']




  def add_tag(self,fnode,attr,value):
    for node in self.Graph.nodes():
      if node == fnode:
        attrs = {node: {attr: value}}
        netx.set_node_attributes(self.Graph,attrs)

  def remove_tag(self,fnode,attr):
    self.Graph.node[fnode].pop(attr,None)

  # Given a source and a destination node
  # We found the shortest path and return all the links
  # of the shortest path from the Graph.
  def get_shortest_path(self,src,dst):
    nodes = netx.shortest_path(self.Graph, source=src, target=dst)
    attr = netx.get_edge_attributes(self.Graph,'name')
    path = []
    for n in range(0,len(nodes)-1):
      try:
        path.append(attr[(nodes[n],nodes[n+1])])
      except:
        path.append(attr[(nodes[n+1],nodes[n])])

    return path

  # Given an attribute and a value we return all nodes
  # where satisfy that rule.
  def get_dest_by_eq_attribute(self,attr,value):
    dest = []
    for node in self.Graph:
      if node not in self.switches:
        if self.Graph.node[node][attr] == value:
          dest.append(node)
    return dest

  def get_dest_by_geq_attribute(self,attr,value):
    dest = []
    for node in self.Graph:
      if node not in self.switches:
        if self.Graph.node[node][attr] >= value:
          dest.append(node)
    return dest

  def get_dest_by_leq_attribute(self,attr,value):
    dest = []
    for node in self.Graph:
      if node not in self.switches:
        if self.Graph.node[node][attr] <= value:
          dest.append(node)
    return dest


  # Calculate the Forwarding Identifier (FID) of the
  # requested path or paths (multicast?)
  def get_FID(self, path):
    bf = '0000000000'
    for i in path:
      bf = bin(int(bf,2) | int(i,2))
    return bf[2:]

  def hextodec(self,hex):
    return int(hex,16)

  def dectobin(self,dec):
    return bin(dec)
  def printGraph(self):
    color_map = []
    for node in self.Graph:
      if node in self.switches:
        color_map.append('grey')
      else:
        color_map.append(self.Graph.node[node]['color'])


    edge_labels = netx.get_edge_attributes(self.Graph, 'name')
    pos = netx.spring_layout(self.Graph, k=0.5, iterations=50)
    color_map.append('green')
    netx.draw(self.Graph, pos, node_size=800, node_color=color_map, with_labels=True)
    netx.draw_networkx_edge_labels(self.Graph, pos, edge_labels=edge_labels)
    plt.show()  # display

def launch ():
  """
  Starts the component
  """
  def start_switch (event):
    Tagsv2(event.connection)
  core.openflow.addListenerByName("ConnectionUp", start_switch)
