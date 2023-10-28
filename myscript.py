import pyeapi
from pprint import pprint as pp
from prettytable import PrettyTable
import yaml


with open('clab-evpnlab01/ansible-inventory.yml', 'r') as file:
     ansible_host_file = yaml.safe_load(file)

pp(ansible_host_file['all']['children']['ceos']['hosts'])



pyeapi.load_config('eapi.conf')

spine1 = pyeapi.connect_to('spine1')
spine2 = pyeapi.connect_to('spine2')
leaf1 = pyeapi.connect_to('leaf1')
leaf2 = pyeapi.connect_to('leaf2')

spines = [spine1, spine2]
leafs = [leaf1, leaf2]

allswitches = spines+leafs


def display_inventory(devices):
    x = PrettyTable()
    x.field_names = ["Switch Name", "Role", "Model", "Version"]

    for switch in allswitches:
        output = switch.enable(['show version', 'show hostname'])
        version = output[0]['result']['version'].split(' ')[0]
        model = output[0]['result']['modelName']
        hostname = output[1]['result']['hostname']
        role = "leaf" if 'leaf' in hostname else "spine"
        x.add_row([hostname, role, model, version])
    
    print(x)
    #print (dir(switch.connection))


#display_inventory(allswitches)

