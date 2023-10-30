import pyeapi
from pprint import pprint as pp
from prettytable import PrettyTable

pyeapi.load_config('eapi.conf')

spine1 = pyeapi.connect_to('spine1')
spine2 = pyeapi.connect_to('spine2')
leaf1 = pyeapi.connect_to('leaf1')
leaf2 = pyeapi.connect_to('leaf2')

spines = [spine1, spine2]
leafs = [leaf1, leaf2]

allswitches = spines+leafs


def evpn_summary(devices):
	x = PrettyTable()
	x.field_names = ["Switch Name", "Neighbor", "State", "Prefix Recieved"]
	for switch in allswitches:
		output = switch.enable(['show bgp evpn summary', 'show hostname'])
		hostname = output[1]['result']['hostname']
		peer_list = output[0]['result']['vrfs']['default']['peers']
		for i in peer_list.keys():
			peer = peer_list[i]
			state = peer['peerState']
			prefix = peer['prefixReceived']
			neighip = i
			x.add_row([hostname, neighip, state, prefix])
	print(x)

def main():
    evpn_summary(allswitches)

if __name__=="__main__":
    main()
