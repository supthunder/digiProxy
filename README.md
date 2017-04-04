# proxy.py
Create proxies using DigitalOcean's API, based upon [@thenikedestroyer's script](https://gist.github.com/thenikedestroyer/803a7cd3557f69aadc88d83d6bdbbe40) and inpsired by [@ryan9918's script](https://github.com/ryan9918/digitaloceandestroyer)

## What it does:

Create droplets, create squid proxies on those droplets, saves to proxies.json

## How To:
1. Edit with your info
  ```
  info = {
	"token" : "some token", # get this from digital ocean
	"ssh_num" : [1234], # has to be a list of INT's
	"sss_path"	: "/Users/username/key.pub", # location to ssh pub key
	"tnd_script" : "https://gist.githubusercontent.com/supthunder/e9362875d5fadc11e614440d87be3a24/raw/08cafe4e1dd75d0ac5767b08809e1a028c906c2f/p.sh" # DZT's script for ubuntu 16.04
        }
```
2. Run ```python proxy.py```

![1](/images/1.gif)

![2](/images/2.gif)

![3](/images/3.gif)
