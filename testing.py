import requests
from bs4 import BeautifulSoup
import pandas as pd
from requests.api import get
from requests_html import HTMLSession

url = 'https://barefootbuttons.com/product-category/version-1/'
url = "https://www.hurdleysofficefurniture.co.nz/product/7342/capri-straight-desk-oak-black"

def get_links(url):
    pass

def get_string(data):
    s = (str(data))
    n = [c for c in s if c.isdigit() or c == "."]
    return(''.join(n))

def woorequest(data):
    temp_data = []
    s = HTMLSession()
    for line in data:
        if line == 'n/a' or line == "POA":
            temp_data.append(0)
        else:
            try:
                r = s.get(line)
                price = r.html.find('span.woocommerce-Price-amount.amount bdi')[1].full_text
                print(price)
                temp_data.append(price)
            except:
                temp_data.append('err')
    return temp_data

def request(data):
    config = {"class": "woocommerce-Price-amount amount"}
    el = "span"
    temp_data = []
    for line in data:
        print(line)
        k = requests.get(line).text
        soup=BeautifulSoup(k,'html.parser')
        productlist = soup.find_all(el, config)
        print((productlist))
        s = (get_string(productlist))
    return temp_data

test_data = open("testdata.txt", "r")
test_dataread = test_data.read()
test_datalist = test_dataread.splitlines()

#get_wooproductdata(url)
#print(request(["https://www.mcgreals.co.nz/products/agile-slimline-mobile", "https://www.mcgreals.co.nz/products/cubit-bar-leaner", "https://www.mcgreals.co.nz/products/solace"]))

print(woorequest(test_datalist))