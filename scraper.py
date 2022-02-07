import requests
from bs4 import BeautifulSoup
import pandas as pd
from requests.api import get
import sys
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import gspread_dataframe as gd
import numpy as np
from gspread_dataframe import set_with_dataframe
from requests_html import HTMLSession
from datetime import date
import time
import random
import string
import emails
import subprocess
from emails import emailer
from comparisons import compare

start = time.time()
today = date.today()
# dd/mm/YY
d1 = today.strftime("%d/%m/%Y")
char_set = "_" + ''.join(random.sample((string.ascii_uppercase + string.digits  ) * 3, 3))

configdict = {
  "uno": "money exclGST",
  "mcg": "product-price__price product-price__price-product-template-split-view",
  "ofw": "taxmoney",
  "opd": "price-col",
  "kds": "product-single__price",
  "coms": "productPrice",
  "opo": "current-price"
}

scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

credentials = Credentials.from_service_account_file(
    "\\\MCGREALSSERVER\\Folder Redirection\\Rory\\Desktop\\Scraper-main\\creds.json",
    scopes=scopes
)

gc = gspread.authorize(credentials)

data_source = gc.open("Comps").worksheet("Raw Data")
web_links = pd.DataFrame(data_source.get_all_records())

#ws = gc.open("Comps").worksheet("Data")
sh = gc.open("Comps")
worksheet = sh.add_worksheet(title= d1 + char_set, rows="100", cols="20")

#sys.exit()
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}

def get_string(data):
    s = (str(data))
    n = [c for c in s if c.isdigit() or c == "."]
    return(''.join(n))

def request(data, brand):
    config = {"class": configdict[brand]}
    el = "span"
    temp_data = []
    for line in data:
        if line == 'n/a' or line == "POA":
            temp_data.append("0")
        else:
            try: 
                k = requests.get(line).text
                soup=BeautifulSoup(k,'html.parser')
                productlist = soup.find_all(el, config)
                #print(productlist)
                s = (get_string(productlist))
                temp_data.append(s)
            except:
                temp_data.append("no connection")
    return temp_data

def mcg_request(data, brand):
    config = {"class": configdict[brand]}
    config2 = {"class": "product-price__price product-price__price-product-template-split-view product-price__sale product-price__sale--single"}
    el = "span"
    temp_data = []
    for line in data:
        if line == 'n/a' or line == "POA":
            temp_data.append(0)
        else:
            try: 
                k = requests.get(line).text
                soup=BeautifulSoup(k,'html.parser')
                productlist = soup.find_all(el, config)
                if len(str(productlist)) < 2:
                    productlist = soup.find_all(el, config2)
                s = (get_string(productlist))
                if s == "":
                    productlist = soup.find_all(el, config2)
                    s = (get_string(productlist))
                temp_data.append(s)
            except:
                temp_data.append("no connection")
    return temp_data

def woorequest(data):
    temp_data = []
    s = HTMLSession()
    for line in data:
        if line == 'n/a' or line == "POA":
            temp_data.append(0)
        else:
            try:
                r = s.get(line)
                price = r.html.find('span.woocommerce-Price-amount.amount bdi')[0].full_text
                temp_data.append(price)
            except:
                temp_data.append('err')
    return temp_data

def direct_office_woorequest(data):
    temp_data = []
    s = HTMLSession()
    for line in data:
        if line == 'n/a' or line == "POA":
            temp_data.append(0)
        else:
            try:
                r = s.get(line)
                price = r.html.find('span.woocommerce-Price-amount.amount bdi')[1].full_text
                temp_data.append(price)
            except:
                temp_data.append('err')
    return temp_data

def request_alt(data, brand):
    config = {"id": configdict[brand]}
    el = "span"
    temp_data = []
    for line in data:
        if line == 'n/a' or line == "POA":
            temp_data.append(0)
        else:
            try: 
                k = requests.get(line).text
                soup=BeautifulSoup(k,'html.parser')
                productlist = soup.find_all(el, config)
                #print(productlist)
                s = (get_string(productlist))
                temp_data.append(s)
            except:
                temp_data.append("no connection")
    return temp_data

def request_alt2(data, brand):
    config = {"class": configdict[brand]}
    el = "p"
    temp_data = []
    for line in data:
        if line == 'n/a' or line == "POA":
            temp_data.append(0)
        else:
            try: 
                k = requests.get(line).text
                soup=BeautifulSoup(k,'html.parser')
                productlist = soup.find_all(el, config)
                #print(productlist)
                s = (get_string(productlist))
                temp_data.append(s)
            except:
                temp_data.append("no connection")
    return temp_data

def opd_request(data):
    config = {"class": "prices"}
    el = "div"
    temp_data = []
    for line in data:
        if line == 'n/a' or line == "POA":
            temp_data.append(0)
        else:
            try: 
                k = requests.get(line).text
                soup=BeautifulSoup(k,'html.parser')
                productlist = soup.find_all(el, config)
                s = (get_string(productlist))
                temp_data.append(s)
            except:
                temp_data.append(0)
    return temp_data

def refine_data(dataframe, col): #takes dataframe and a given column and returns a list of the column values
    data = pd.DataFrame(dataframe, columns= [col])
    data = dataframe[col].values.tolist()
    return data

#uno
uno_refined = refine_data(web_links, 'Uno Furniture')
uno_data = request(uno_refined, "uno")
uno_data = [str(i) for i in uno_data]
#mcg
mcg_refined = refine_data(web_links, 'McGreals')
mcg_data = mcg_request(mcg_refined, "mcg")
mcg_data = [str(i) for i in mcg_data]
#OFW
ofw_refined = refine_data(web_links, 'Office Furniture Warehouse')
ofw_data = request(ofw_refined, "ofw")
ofw_data = [str(i) for i in ofw_data]
ofw_data = [i[:i.find(".") + 3] for i in ofw_data]
#opd 
opd_refined = refine_data(web_links, 'Office Products Depot')
opd_data = opd_request(opd_refined)
opd_data = [str(i) for i in opd_data]
opd_data = [i[1:] for i in opd_data]
#systems
sys_refined = refine_data(web_links, 'Systems')
systems_data = woorequest(sys_refined)             # uses other woorequest function
systems_data = [str(i) for i in systems_data]
#directoffice 
directoffice_refined = refine_data(web_links, 'Direct Office')
directoffice_data = direct_office_woorequest(directoffice_refined)
#kds
kds_refined = refine_data(web_links, 'Kiwi Dragon Supplies')
kds_data = request(kds_refined, "kds")
kds_data = [str(i) for i in kds_data]
kds_data = [i[:i.find(".") + 3] for i in kds_data]
#Commercial Traders
commercialtraders_refined = refine_data(web_links, 'Commercial Traders')
coms_data = request_alt(commercialtraders_refined, "coms")         # uses other request_alt function
coms_data = [str(i) for i in coms_data]
#Office Products Online
opo_refined = refine_data(web_links, 'Office Products Online')
opo_data = request_alt2(opo_refined, "opo")         # uses other request_alt2 function
opo_data = [str(i) for i in opo_data]
opo_data = [i[:i.find(".") + 3] for i in opo_data]

products = refine_data(web_links, 'Product')
d = {'Product':products, 'McGreals': mcg_data, 'Uno Furniture': uno_data, 'Office Furniture Warehouse': ofw_data,
'Kiwi Dragon Supplies':kds_data, 'Office Products Depot': opd_data, 'Office Products Online': opo_data,'Direct Office':directoffice_data, 'Commercial Traders': coms_data, 'Systems Commercial': systems_data}

df = pd.DataFrame(data=d)
df = df.applymap(str)
set_with_dataframe(worksheet, df, row=1, col=1,) #-> THIS EXPORTS YOUR DATAFRAME TO THE GOOGLE SHEET
# starting time
end = time.time()

#comparison_df = compare()   ### compare dataframe to previous dates
#emailer(df) // this line sends the spreadsheet to rory@mcg email

# total time taken
print("Script ran in :", end-start, "seconds")
#subprocess.call("emails.py", shell=True)
