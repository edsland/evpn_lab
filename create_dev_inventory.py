import pyeapi
from pprint import pprint as pp
from prettytable import PrettyTable
import yaml


def create_conf():

	with open('clab-evpnlab01/ansible-inventory.yml', 'r') as file:
		ansible_host_file = yaml.safe_load(file)

	ans_dev_list = ansible_host_file['all']['children']['ceos']['hosts']

	device_list = ''

	for i in ans_dev_list:
		hostname = i.split('-')[-1]
		ip = ans_dev_list[i]['ansible_host']
		device_list += f'[connection:{hostname}]\n'
		device_list += f'host: {ip}\n\n'

	device_list += "[DEFAULT]\nusername: admin\npassword: admin\ntransport: https"
	
	print('Saving Ansible inventorty as eapi.conf')
	text_file = open("eapi.conf", "w")
	text_file.write(device_list)
	text_file.close()


def main():
    create_conf()

if __name__=="__main__":
    main()
