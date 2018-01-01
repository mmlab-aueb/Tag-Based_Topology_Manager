from pox.core import core
import pox.openflow.nicira as nx
import pox.openflow.libopenflow_01 as of
from pox.lib.addresses import IPAddr6,EthAddr 

log = core.getLogger()

"""
h1 ---0001---s1---0010---s2---0100---h2
https://openflow.stanford.edu/display/ONL/POX+Wiki
http://flowgrammable.org/sdn/openflow/message-layer/match/#tab_ofp_1_2
"""

class Tags (object):
  def __init__ (self, connection):
    self.connection = connection
    connection.addListeners(self)
    if (connection.eth_addr.toStr() == "00:00:00:00:00:01"):
        print "Preparing of rules"
        msg = nx.nx_flow_mod_table_id()
        connection.send(msg)
        #table 0      
        msg = nx.nx_flow_mod()
        msg.table_id = 0
        msg.priority = 1500
        msg.match.of_eth_dst = "00:00:00:00:00:00"
        msg.match.of_eth_type = 0x86dd
        msg.match.of_in_port = 1
        msg.actions.append(nx.nx_action_resubmit.resubmit_table(table = 1))
        self.connection.send(msg)

        msg = nx.nx_flow_mod()
        msg.table_id = 0
        msg.priority = 1000
        msg.match.of_eth_dst = "00:00:00:00:00:00"
        msg.match.of_eth_type = 0x86dd
        msg.match.nx_ipv6_dst = (IPAddr6("::1"),IPAddr6("::1"))
        msg.actions.append(of.ofp_action_output(port = 1 ))
        msg.actions.append(nx.nx_action_resubmit.resubmit_table(table = 1))
        self.connection.send(msg)
        
        msg = nx.nx_flow_mod()
        msg.table_id = 0
        msg.priority = 500
        msg.match.of_eth_dst = "00:00:00:00:00:00"
        msg.match.of_eth_type = 0x86dd
        msg.actions.append(nx.nx_action_resubmit.resubmit_table(table = 1))
        self.connection.send(msg)
        
        #table 1
        msg = nx.nx_flow_mod()
        msg.table_id = 1
        msg.priority = 1000
        msg.match.of_eth_dst = "00:00:00:00:00:00"
        msg.match.of_eth_type = 0x86dd
        msg.match.nx_ipv6_dst = (IPAddr6("::2"),IPAddr6("::2"))
        msg.actions.append(of.ofp_action_output(port = 1))
        self.connection.send(msg)
        
        msg = nx.nx_flow_mod()
        msg.table_id = 1
        msg.priority = 1500
        msg.match.of_eth_dst = "00:00:00:00:00:00"
        msg.match.of_eth_type = 0x86dd
        msg.match.of_in_port = 2
        self.connection.send(msg)
        
    if (connection.eth_addr.toStr() == "00:00:00:00:00:02"):
        print "Preparing of rules"
        msg = nx.nx_flow_mod_table_id()
        connection.send(msg)
        #table 0      
        msg = nx.nx_flow_mod()
        msg.table_id = 0
        msg.priority = 1500
        msg.match.of_eth_dst = "00:00:00:00:00:00"
        msg.match.of_eth_type = 0x86dd
        msg.match.of_in_port = 1
        msg.actions.append(nx.nx_action_resubmit.resubmit_table(table = 1))
        self.connection.send(msg)
        
        msg = nx.nx_flow_mod()
        msg.table_id = 0
        msg.priority = 1000
        msg.match.of_eth_dst = "00:00:00:00:00:00"
        msg.match.of_eth_type = 0x86dd
        msg.match.nx_ipv6_dst = (IPAddr6("::2"),IPAddr6("::2"))
        msg.actions.append(of.ofp_action_output(port = 1 ))
        msg.actions.append(nx.nx_action_resubmit.resubmit_table(table = 1))
        self.connection.send(msg)
        
        msg = nx.nx_flow_mod()
        msg.table_id = 0
        msg.priority = 500
        msg.match.of_eth_dst = "00:00:00:00:00:00"
        msg.match.of_eth_type = 0x86dd
        msg.actions.append(nx.nx_action_resubmit.resubmit_table(table = 1))
        self.connection.send(msg)
        #table 1
        msg = nx.nx_flow_mod()
        msg.table_id = 1
        msg.priority = 1000
        msg.match.of_eth_dst = "00:00:00:00:00:00"
        msg.match.of_eth_type = 0x86dd
        msg.match.nx_ipv6_dst = (IPAddr6("::4"),IPAddr6("::4"))
        msg.actions.append(of.ofp_action_output(port = 2 ))
        self.connection.send(msg)
        
        msg = nx.nx_flow_mod()
        msg.table_id = 1
        msg.priority = 1500
        msg.match.of_eth_dst = "00:00:00:00:00:00"
        msg.match.of_eth_type = 0x86dd
        msg.match.of_in_port = 2
        self.connection.send(msg)


  def _handle_PacketIn (self, event):
    """
    Handles packet in messages from the switch.
    """



def launch ():
  """
  Starts the component
  """
  def start_switch (event):
    Tags(event.connection)
  core.openflow.addListenerByName("ConnectionUp", start_switch)
