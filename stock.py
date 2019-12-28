import requests
from bs4 import BeautifulSoup
import pandas as pd 
'''
todo :
    1.get stockid from txt and avoid depucated data
    2.composite the data to a 2d array in order to push to csv
    3.make title for csv
    4.avoid banned by goodinfo find solution
'''
stockIdList = ['1402','2330']
AllInfoList = []
for stockId in stockIdList:
    url = 'https://goodinfo.tw/StockInfo/StockBzPerformance.asp?STOCK_ID='+stockId
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
    r = requests.get(url, headers = headers)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, 'html.parser')
    # parse data from talbe calss, we have two target section here
    # section1 is for stockDiv, moneyDiv 
    sectionTables = soup.findAll('table', {"class": "solid_1_padding_4_0_tbl"})

    # this is section1 for stockDiv and moneyDiv
    # 1.select talbe[0] 2.find all tr in table[0] 3.get all td from tr[10] 4.get stockdiv and moneydiv
    trfromTable1 = sectionTables[0].findAll('tr')
    tdRows =trfromTable1[10].findAll('td')
    stockdiv = tdRows[1].getText()
    moneydiv = tdRows[4].getText()
    print ("stokid " + stockId+"    stock " + stockdiv + " money " + moneydiv )
    # for td in tbls[10].findAll('td'):
        # print(td.getText())
    # for tr in tab.findAll('tr'):
        # for td in tr.findAll('td'):
            # print (td.getText())
   
    # this is section2 for dailyinfo : endprice, this year eps, last year eps
    trfromTable2 = sectionTables[1].findAll('tr')
    tdRows =trfromTable2[2].findAll('td') #for this year rows
    endprice = tdRows[3].getText()
    thisyearEps = tdRows[-3].getText()
    tdRows =trfromTable2[3].findAll('td') #for last year rows to get last year eps
    lastyesrEps = tdRows[-3].getText()
    print ("endprice " + endprice + "   thisyearEps " + thisyearEps + "   lastyearEps" + lastyesrEps )
    print ('*****************************************************************')
    # for td in tdRows:
        # print (td.getText())

    # tab = sectionTables[1]
    # for tr in tab.findAll('tr',limit=4):
        # for td in tr.findAll('td'):
            # print (td.getText())

    # dfs = pd.read_html(str(rows))
    # print (dfs[0])
    # dfs[0].to_html("1402.html",index=False)
    singleStockInfo = [stockId, endprice, stockdiv, moneydiv, lastyesrEps, thisyearEps]
    AllInfoList.append(singleStockInfo)

print(AllInfoList)
    