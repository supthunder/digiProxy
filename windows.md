# Windows workaround for now

1. Create a new droplet on digital ocean
2. You will get email with password
3. Open the **console** for the droplet on digitalocean, and login as root + password in email
4. Run: 
```
wget https://gist.githubusercontent.com/supthunder/e9362875d5fadc11e614440d87be3a24/raw/08cafe4e1dd75d0ac5767b08809e1a028c906c2f/p.sh
```
5. Run: 
```
sudo bash p.sh
```
6. Exit console. Go to https://cloud.digitalocean.com/images/snapshots/droplets
7. Create a snapshot using the droplet you just created, now open terminal/powershell
8. Get **Image IDs** from ```python rsaKey.py```, its the 8 digit number
9. Add this to **image_id** in info{} in **[windowsProxy.py](windowsProxy.py)**
10. ```python windowsProxy.py```

**Once you create a snapshot/get the id, you can skip steps 1-9 next time you want to create a proxy**
