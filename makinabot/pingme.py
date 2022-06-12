#!/usr/bin/python3
import random, time, requests
url='https://stirring-precious-bed.glitch.me'
headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'}
max=90
min=0

while True:
    try:
        req=requests.get(url,headers=headers)
        print('Pinging',url)
        print(req)
        time.sleep(random.randrange(min,max+1))
    except:
        pass
