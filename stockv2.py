import requests
from bs4 import BeautifulSoup
import pandas as pd
import csvModule
import re
import time
import random
import ua
import globalsVar
#------time measure start -------#
tStart = time.time()

def getStockIdInfoList():
    #infolist = csvModule.readStockInfoFromCSV()
    infolist = csvModule.readStockInfoFromCSV()
    alist = []
    for ele in infolist:
        alist.append(re.findall(r'^\d{4,}[a-zA-Z]{0,1}', ele)[0])
    return alist

currentYear = time.strftime('%Y') # or "%y"
stockIdList = getStockIdInfoList()

AllInfoList = []
for stockId in stockIdList:
        # StockDetail.asp contains all the data we need to scrapy
        url = 'https://goodinfo.tw/StockInfo/StockDetail.asp?STOCK_ID='+stockId
        # make agent pool #todo: make multi agent pool
        fakeUA = ua.getFakeUA()
        headers = {
        'accept':'*/*',
        'accept-encoding':'gzip, deflate, br',
        'accept-language':'en-US,en;q=0.9,zh-TW;q=0.8,zh;q=0.7',
        'origin': 'https://goodinfo.tw',
        'User-Agent': fakeUA,
        }
        r = requests.get(url, headers = headers)
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, 'html.parser')

        #get stockdiv and moneydiv
        sectionTables = soup.findAll('table', {"class": "solid_1_padding_4_4_tbl"})
        trfromTable1 = sectionTables[4].findAll('tr')
        tdRows = trfromTable1[3].findAll('td')
        moneydiv = tdRows[1].getText()
        stockdiv = tdRows[2].getText()
        # print (len(sectionTables))
        trfromTable1Size = len(sectionTables[4].findAll('tr', limit=7))
        for i in range(3, trfromTable1Size):
                #equal to if trfromTable1[i].findAll('td')[0].getText() == currentYear:
                tdrows = trfromTable1[i].find('td')
                if tdrows.getText() == currentYear:
                        moneydiv = tdrows.findNext('td').getText()
                        stockdiv = tdrows.findNext('td').findNext('td').getText()
                
        #get this, last year eps
        sectionTables = soup.findAll('table', {"class": "solid_1_padding_4_0_tbl"}, limit=15)
        trfromTable2 = sectionTables[11].findAll('tr')
        tdRows =trfromTable2[1].findAll('td') #for this year rows
        thisyearEps = tdRows[-1].getText()
        tdRows =trfromTable2[2].findAll('td') #for last year rows to get last year eps
        lastyesrEps = tdRows[-1].getText()
        

        #endprice
        sectionTables = soup.find('table', {"class": "solid_1_padding_3_2_tbl"})
        # trfromTable3 = sectionTables.findAll('tr')[3]
        # tdRows =trfromTable3[3].findAll('td')       => equals to sectionTables.findAll('tr')[3].find('td').getText()
        # endprice = tdRows[0].getText()
        endprice = sectionTables.findAll('tr', limit=5)[3].find('td').getText()


        # print ("stockId:"+stockId+" endprice:"+endprice+"  stockdiv:"+stockdiv+" monetdiv:"+moneydiv+"  lastyesrEps:"+lastyesrEps+"  thisyearEps:"+thisyearEps)
        singleStockInfo = [stockId, endprice, stockdiv, moneydiv, lastyesrEps, thisyearEps]
        AllInfoList.append(singleStockInfo)

        # Dont have to sleep when scarpy to the end stockId 
        if stockId == stockIdList[-1]:
                #back door for getEPSYearStr buz only do once
                for i in range(2, 4):
                        globalsVar.setEPSYearStrList(trfromTable2[i].find('td').getText())
                break
        
        # avoid for anti-scrapy rules, dont request too mush time in a loop
        time.sleep(random.uniform(2, 4))
        



#-------time measure end---------#
tEnd = time.time()
print ("It cost %f sec" % (tEnd - tStart))

print ('All info')
print(AllInfoList)
csvModule.write2csv(AllInfoList)