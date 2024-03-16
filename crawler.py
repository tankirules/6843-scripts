from requests_pkcs12 import get, post
import json
import pprint
from requests import Session
from requests_pkcs12 import Pkcs12Adapter
import threading, sys, os
import requests
import time
import urllib.parse

#this is the new pw for the new cert
pw = ''

url = 'https://blog.quoccabank.com'

headers = {
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
            #url1 = url + '?p=42'
            for i in range(1000):
                status_code = -1
                url1 = url + '?author=' + str(i)
                while status_code != 200:
                    r = s.get(url1, verify=False)
                    status_code = r.status_code
                    if status_code == 404:
                        break
                    if status_code == 429:
                        headers = r.headers
                        sec = float(headers['X-Retry-In:'])
                        print(f"Retrying url {url1} in {sec / 1000} seconds")
                        time.sleep(sec)
                if 'COMP6443' in r.text and status_code != 404:
                    print(r.text)    
                    
            
            
    
    

    except KeyboardInterrupt:
        print("Force exiting")
        os._exit(1)


    

    
if __name__ == '__main__':
    main()