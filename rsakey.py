import digitalocean
import sys
from time import sleep

token = ""
manager = digitalocean.Manager(token=token)
keys = manager.get_all_sshkeys()
print("SSH keys:")
print([key.id for key in keys])
images = manager.get_my_images()
print("Image IDs:")
print([image.id for image in images])

