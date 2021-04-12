#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import csv

month_dict = {}
month_dict[1] = 'enero'
month_dict[2] = 'febrero'
month_dict[3] = 'marzo'
month_dict[4] = 'abril'
month_dict[5] = 'mayo'
month_dict[6] = 'junio'
month_dict[7] = 'julio'
month_dict[8] = 'agosto'
month_dict[9] = 'septiembre'
month_dict[10] = 'octubre'
month_dict[11] = 'noviembre'
month_dict[12] = 'diciembre'

def query(URL, headers, data):
    page = requests.get(URL, headers = headers)
    soup = BeautifulSoup(page.content)
    table = soup.find('table')
    try:
        for row in table.findAll('tr'):
            cells = row.findAll('td')
            date = get_date(cells[0].string)
            value, currency = get_change(cells[1].string)
            data.append([date, value, currency])
        return
    except:
        return
    

def get_date(date):
    date = date.split(sep = " ")
    day = date[1]
    month = date[3]
    year = date[-1]
    for num, name in month_dict.items():
        if month == name:
            break
    date_str =  day + "/" + str(num) + "/" + year
    return datetime.strptime(date_str, '%d/%m/%Y').date()

def get_change(change):
    change = change.split(sep = " ")
    value = change[3]
    value = value.replace(",", ".")
    currency = change[-1]
    return value, currency

# Initialization of variables
data = list()

# Dataset's header
dataHeader = ["Date", "Value", "Currency"]
data.append(dataHeader)

# HTTP Headers
headers = {
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
}

# Calculate 5 years from now
now = datetime.now()
year = now.year
years = [year - i for i in range(5) ]
# URL
baseURL = "https://cambio.today/historico/bitcoin/"

# List of currencies we will search
currencies = ["euro", "dolar-norteamericano", "peso-argentino", "rublo-ruso", "lira-turca",
             "peso-mexicano", "yen"]

for curr in currencies:
    month = now.month
    currURL = baseURL + curr + "/"
    for year in years:
        while month <= 12:
            URL = currURL + month_dict[month] + "-" + str(year)
            t0 = time.time()
            query(URL, headers, data)
            response_delay = time.time() - t0
            if response_delay <= 0.1: # Implement delay between queries
                time.sleep(10 * response_delay) 
            else:
                time.sleep(1)
            month += 1
        month = 1

with open('BitcoinValue.csv', 'w', newline = '') as csvfile:
    writer = csv.writer(csvfile, delimiter = ",",
                       quotechar = "|", quoting = csv.QUOTE_MINIMAL)
    for row in data:
        writer.writerow(row)

