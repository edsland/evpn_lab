import pyeapi
import sys
from pprint import pprint as pp
from prettytable import PrettyTable

pyeapi.load_config('eapi.conf')

#spine1 = pyeapi.connect_to('spine1')
#spine2 = pyeapi.connect_to('spine2')
#leaf1 = pyeapi.connect_to('leaf1')
#leaf2 = pyeapi.connect_to('leaf2')

#spines = [spine1, spine2]
#leafs = [leaf1, leaf2]

#allswitches = spines+leafs


def create_vlan(devices, vlanid):
	for switch in devices:
		switch = switch.strip().lower()
		try:
			node = pyeapi.connect_to(switch)
			vlans = node.api('vlans')
			vlans.create(vlanid)
			vlans.set_name(vlanid, f'PY_CREATED_{vlanid}')
			print(f'Created VLAN {vlanid} on {switch}!')
		except Exception as e: 
			print(f'{switch}: {e}')
			print(f'Could not create VLAN {vlanid}')

def create_bgpconfig(devices, vlanid):
	for switch in devices:
		switch = switch.strip().lower()
		try:
			node = pyeapi.connect_to(switch)
			bgp = node.api('bgp')
			routerid = bgp.get()['router_id']
			bgp_cmd = ['router bgp 65000', f'vlan {vlanid}', f'rd {routerid}:{vlanid}', f'route-target both {vlanid}:{vlanid}', 'redistribute learned']
			bgp.configure_bgp(bgp_cmd)
			print(f'Created BGP config on {switch}!')
		except Exception as e:
			print(f'{switch}: {e}')

def main():
	swInput = input("Please specify one or more leaf switches(leaf1,leaf2): ")
	swList = swInput.split(',')
	
	vlInput = input("Enter VLAN ID (2-1000): ")
	try:
		vlanid = int(vlInput)
		if vlanid > 1 and vlanid < 1001:
			create_vlan(swList, vlanid)
			create_bgpconfig(swList, vlanid)
			print('')
			print(f'********* L2VNI {vlanid} created on switches {swList} *********')
		else:
			print('Your input is invalid. Try again')
			sys.exit(1)
	except Exception as e:
		print(e)



if __name__=="__main__":
	main()
