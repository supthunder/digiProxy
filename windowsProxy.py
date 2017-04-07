import digitalocean
import sys
from time import sleep
import concurrent.futures
import json
from termcolor import cprint

info = {
	"token" : "TOKEN", # get this from digital ocean
	"image_id": 'IMAGE_ID',
	"ssh_num" : [1234567], # has to be a list of INT's,  get this from rsaKey.py
	"ssh_path"	: "C:\\Users\\USERNAME\\Desktop\\FOLDER\\key.pub", # location to ssh pub key
	"tnd_script" : "https://gist.githubusercontent.com/supthunder/e9362875d5fadc11e614440d87be3a24/raw/08cafe4e1dd75d0ac5767b08809e1a028c906c2f/p.sh" # DZT's script for ubuntu 16.04
}

ips = []
def createDrop(each, extra):
	global ips, info
	token = "token" 
	droplet = digitalocean.Droplet(token=info['token'],
	                               name='proxy',
	                               region='sfo1',
	                               image=info['image_id'], # get from rsaKey.py
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
	ips.append(str(droplet.ip_address)+":3128")

def multiDrop(items):
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        for item in items:
            executor.submit(createDrop, item, 60)

def main():
	global ips
	amount = int(input("How many proxies? "))
	each = list(range(1,amount+1))

	# Create droplets
	multiDrop(each)

	cprint("Successfully created {} proxies!".format(str(amount)),"green")
	print(ips)
	# Save to json
	with open("proxy.json","w") as outfile:
		json.dump(ips, outfile, indent=4, sort_keys=True)
	cprint("Saved to proxy.json","green")

if __name__ == '__main__':
	main()

