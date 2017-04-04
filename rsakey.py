import digitalocean
import sys
from time import sleep

token = ""
manager = digitalocean.Manager(token=token)
keys = manager.get_all_sshkeys()
print(keys)
