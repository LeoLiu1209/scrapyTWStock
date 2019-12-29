import csvModule
import re

#csvModule.mockwrite2csv()

# read from CSV and return StockInfoList
# lista = csvModule.readStockInfoFromCSV()

#test connect 
# infolist = csvModule.readStockInfoFromCSV()
# # print (infolist)
# alist = []
# for ele in infolist:
#     alist.append(re.findall(r'^\d{4,}[a-zA-Z]{0,1}', ele)[0])
   
# print (alist)

#test year
# import time
# year = time.strftime('%Y') # or "%y"
# if '2019' == year:
    # print('same')

import ua
import requests
from bs4 import BeautifulSoup
import time

testIdList = ['2330','1216','2880']

for stockId in testIdList:
    fakeUA = ua.getFakeUA()
    print (fakeUA)
    # StockDetail.asp contains all the data we need to scrapy
    url = 'https://goodinfo.tw/StockInfo/StockDetail.asp?STOCK_ID='+stockId
    headers = {
        'accept':'*/*',
        'accept-encoding':'gzip, deflate, br',
        'origin': 'https://goodinfo.tw',
        'User-Agent': fakeUA,
    }
    # make agent pool #todo: make multi agent pool
    r = requests.get(url, headers = headers)
    r.encoding = 'utf-8'
    print(r.status_code)
    soup = BeautifulSoup(r.text, 'html.parser')

    sectionTables = soup.find('table', {"class": "solid_1_padding_3_2_tbl"})
    endprice = sectionTables.findAll('tr', limit=5)[3].find('td').getText()
    print(endprice)
    time.sleep(3)
    