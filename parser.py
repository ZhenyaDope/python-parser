#!/usr/bin/python
# This parser only works on linux!

from time import sleep
from os import system

separator = '==========================================================='
print(separator)

# If Browser Tor is not installed
dist = ['apt-get install', 'pacman -S']
prog = ['tor']

for i in dist:
    for j in prog:
        system("{dist} {prog}".format(dist = i,prog = j))

print("[+] Tor Browser installed ")


# If dependencies are not installed
'''
installer = ['pip install']
deps = ['fake_useragent','bs4','requests','"requests[socks]"']

for inst in installer:
    for dep in deps:
        system("{inst} {dep}".format(inst = inst, dep = dep))
        print("[+] Dependencies {dep} installed".format(dep = dep))


print(separator)
'''

from bs4 import BeautifulSoup
import requests, fake_useragent




# Start Tor services
system("sudo systemctl start tor.service")
print('[+] Tor services starting...')

print(separator)


# Create random User-Agent
ua = fake_useragent.UserAgent()
user = ua.random
header = {'User-Agent':str(user)}

# Connect to the ip-site
ipSite = 'http://icanhazip.com'
adrs = requests.get(ipSite,headers=header)

# Check your ip adress
print(separator + '\n[*] Your IP address:\n'+adrs.text+"\n"+separator)
print('[!] Connecting to the Tor network',end = "")

# Just loading ...
for i in range(5):
    sleep(0.2)
    print('.',end="",flush=True)

# Proxie Tor Browser
proxie = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
}


# Connect to the network tor
try: 
    adrs = requests.get(ipSite, proxies=proxie, headers=header)
# Error coonection
except:
    connection = False
    print('/\n[x] Stopping connect to the Tor network\n' + separator)
else:
    connection = True
    print('/\n[+] Connection to the Tor network\n' + separator)
    print("[*] Your Tor IP network: \n" + adrs.text + separator)

finally:
    print('Exmaple : http://google.com tag attribute\n')
    print('Exmaple : http://google.com a href\n')
    url = input('[!] Enter website url \nhttp://')

    if connection == True:
        page = requests.get("http://"+str(url).split()[0],proxies=proxie,headers=header)
    else:
        page = requests.get("http://"+str(url).split()[0],headers=header)

    soup = BeautifulSoup(page.text,'html.parser')


    if url.split()[0] == url.split()[-1]:
        code = ""
        for tag in soup.findAll('html'):
            code += str(tag)

        with open('index.html','w') as html:
            html.write(code)
            html.close()
    else:
        # Parse tag
        if url.split()[1] == url.split()[-1]:
                links = ""
                for tag in soup.findAll(url.split()[1]):
                    links += str(tag)+"\n"
                with open('links.txt','w') as text:
                    text.write(links)
                    text.close()
        # Parse attribute
        else:
            attr = ""
            for tag in soup.findAll(url.split()[1]):
                attr += str(tag[url.split()[2]]) + '\n'
            with open('links.txt','w') as text:
                text.write(attr)
                text.close()
    print(separator)

# Disabled proxy Tor Browser
system("sudo systemctl stop tor.service")

print('Exit...')