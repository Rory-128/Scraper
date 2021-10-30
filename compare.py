'compares last two dataframes and saves to a local spreadsheet True/False on differences'

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

scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

credentials = Credentials.from_service_account_file(
    "C:\\Users\\PC\\Desktop\\Scraper\\creds.json",
    scopes=scopes
)

gc = gspread.authorize(credentials)

last_sheet = gc.open("Comps").get_worksheet(-1)
df_last = pd.DataFrame(last_sheet.get_all_records())

penultimate_sheet = gc.open("Comps").get_worksheet(-2)
df_penultimate = pd.DataFrame(penultimate_sheet.get_all_records())

comp = df_last.eq(df_penultimate)
comp.to_excel(str(random.randint(1,20)) + "output.xlsx")  
