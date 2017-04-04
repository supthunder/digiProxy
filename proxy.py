import digitalocean
import sys
from time import sleep
import paramiko
import concurrent.futures
import json
from termcolor import cprint

info = {
	"token" : "some token", # get this from digital ocean
	"ssh_num" : [1234], # has to be a list of INT's
	"sss_path"	: "/Users/username/key.pub", # location to ssh pub key
	"tnd_script" : "https://gist.githubusercontent.com/supthunder/e9362875d5fadc11e614440d87be3a24/raw/08cafe4e1dd75d0ac5767b08809e1a028c906c2f/p.sh" # DZT's script for ubuntu 16.04
}

ips = []
proxies = []
def createDrop(each, extra):
	global ips, proxies, info
	token = "token" 
	droplet = digitalocean.Droplet(token=info['token'],
	                               name='somename',
	                               region='nyc2',
	                               image='ubuntu-16-04-x64', # Change etc
	                               size_slug='512mb',  # $5
	                               backups=False,
	                               ssh_keys=info['ssh_num']) # should be int's in a list
	droplet.create()
	checkCompleted = False
	while(not checkCompleted):
		cprint("[Proxy #{}] - Waiting to create...".format(each),"red")
		if droplet.get_actions()[0].status == "completed":
			checkCompleted = True
		sleep(5)
	droplet.load()
	cprint("[Proxy #{}] - Created ".format(each) + str(droplet.ip_address),"green")
	ips.append(droplet.ip_address)

def proxy(ip, extra):
	cprint("[{}] - Creating proxy...".format(ip),"yellow")
	client = paramiko.SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

	check = False
	while(not check):
		cprint("[{}] - Connecting to droplet...".format(ip),"yellow")
		

		try:
			client.connect(str(ip), username='root',look_for_keys=False,key_filename=info['sss_path'])
			sleep(2)
			condition = str(client.get_transport().is_active())
			if condition == "True":
				cprint("[{}] - Connected!".format(ip),"green")
				check = True
			else:
				cprint("[{}] - Failed, trying again...".format(ip),"red")
				sleep(2)
		except:
			cprint("[{}] - Droplet still loading, trying again in 5 seconds...".format(ip),"red")
			sleep(5)

	# Download tnd file
	cprint("[{}] - Downloading .sh file...".format(ip),"yellow")
	stdin,stdout,stderr=client.exec_command("wget "+info["tnd_script"])
	check = stdout.channel.recv_exit_status()

	# Run tnd file
	cprint("[{}] - running .sh file...".format(ip),"yellow")
	stdin,stdout,stderr=client.exec_command("sudo bash p.sh")
	check = stdout.channel.recv_exit_status()

	cprint("[{}] - Getting ip...".format(ip),"yellow")
	stdin,stdout,stderr=client.exec_command("curl ifconfig.co")
	outlines=stdout.readlines()
	resp=''.join(outlines)
	check = stdout.channel.recv_exit_status()

	cprint("[{}] - Getting port...".format(ip),"yellow")
	stdin,stdout,stderr=client.exec_command("cat /etc/squid/squid.conf")
	outlines=stdout.readlines()
	proxies.append(resp.rstrip() + ":" + outlines[0][-5:].rstrip())
	check = stdout.channel.recv_exit_status()

	cprint("[{}] - Done!".format(ip),"green")
	client.close()


def multiProxy(ips):
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        for item in ips:
            executor.submit(proxy, item, 60)
def multiDrop(items):
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        for item in items:
            executor.submit(createDrop, item, 60)

def main():
	global ips, proxies
	amount = int(input("How may proxies? "))
	each = list(range(1,amount+1))

	# Create droplets
	multiDrop(each)
	print(ips)

	# Create proxies
	multiProxy(ips)


	cprint("Successfully created {} proxies!".format(str(amount)),"green")
	print(proxies)

	# Save to json
	with open("proxy.json","w") as outfile:
		json.dump(proxies, outfile, indent=4, sort_keys=True)
	cprint("Saved to proxy.json","green")

if __name__ == '__main__':
	main()

