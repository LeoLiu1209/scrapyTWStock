import requests
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup
import pandas as pd
import csvModule
import re
import time
import random
import ua
import globalsVar
import sys
from openpyxl import load_workbook
from urllib3.util.retry import Retry
#------time measure start -------#
tStart = time.time()

def getStockIdInfoList():
    stockIdListFromResultCSV = csvModule.readStockInfoFromExcel()
    stockIdList = []
    for ele in stockIdListFromResultCSV:
        #split stockid and stockName #0056 00692 006656R
        stockIdList.append(re.findall(r'^\d{4,}[a-zA-Z]{0,1}', ele)[0])
    return stockIdList

def requestPage(url):
    try:
        # make agent pool #todo: make multi agent pool
        fakeUA = ua.getFakeUA()
        headers = {
        'accept':'*/*',
        'accept-encoding':'gzip, deflate, br',
        'accept-language':'en-US,en;q=0.9,zh-TW;q=0.8,zh;q=0.7',
        'origin': 'https://goodinfo.tw',
        'User-Agent': fakeUA,
        }
        req = requests.Session()
        req.keep_alive = False
        retries = Retry(total=5,
                backoff_factor=0.5,
                status_forcelist=[ 500, 502, 503, 504 ])
        req.mount('https://', HTTPAdapter(max_retries=retries))
        resp = req.get(url, headers = headers, timeout = 20)
        if resp.status_code == 200:
            resp.encoding = 'utf-8'
            return BeautifulSoup(resp.text, 'html.parser')
        else :
            print ('status code not 200, actual code is {}'.format(resp.status_code))
            return None
    except Exception as e:
        print ('request error : {}'.format(e))
        time.sleep(3)
        return requestPage(url)
        

def scrapyData(stockIdList):
    currentYear = time.strftime('%Y') # or "%y"
    AllInfoList = []
    count = 0
    for stockId in stockIdList:

        # StockDetail.asp contains all the data we need to scrapy
        url = 'https://goodinfo.tw/StockInfo/StockDetail.asp?STOCK_ID='+stockId
        
        # request page and return page
        soup = requestPage(url)
        if soup == None:
            sys.exit('Internet error!! \nProgram finish')

        #get 前一年 stockdiv and moneydiv
        sectionTables = soup.findAll('table', {"class": "solid_1_padding_4_4_tbl"})
        trfromTable1 = sectionTables[4].findAll('tr')
        # tdRows = trfromTable1[3].findAll('td')
        lastYearDiviendStr = str(int(currentYear)-1)
        # moneydiv = tdRows[1].getText()
        # stockdiv = tdRows[2].getText()
        
        #get 前兩年 stockdiv and moneydiv
        # tdRows = trfromTable1[4].findAll('td')
        last2yearDiviendStr = str(int(currentYear)-2)
        # last2yearMoneydiv = tdRows[1].getText()
        # last2yearStockdiv = tdRows[2].getText()

        # print (len(sectionTables))
        trfromTable1Size = len(sectionTables[4].findAll('tr', limit=7))
        for i in range(3, trfromTable1Size):
                #equal to if trfromTable1[i].findAll('td')[0].getText() == currentYear:
                tdrows = trfromTable1[i].find('td')
                tdrows2 = trfromTable1[i+1].find('td')
                if tdrows.getText() == lastYearDiviendStr:
                        moneydiv = tdrows.findNext('td').getText()
                        stockdiv = tdrows.findNext('td').findNext('td').getText()
                        last2yearMoneydiv = tdrows2.findNext('td').getText()
                        last2yearStockdiv = tdrows2.findNext('td').findNext('td').getText()
                        break
       
        #get this, last year eps
        sectionTables = soup.findAll('table', {"class": "solid_1_padding_4_0_tbl"}, limit=15)
        trfromTable2 = sectionTables[11].findAll('tr')
        tdRows =trfromTable2[1].findAll('td') #for this year rows
        thisyearEps = tdRows[-1].getText()
        tdRows =trfromTable2[2].findAll('td') #for last year rows to get last year eps
        lastyesrEps = tdRows[-1].getText()
        tdRows =trfromTable2[3].findAll('td') #for previous 2 year rows to get previous 2 year eps
        previous2yearEps = tdRows[-1].getText()
        

        #endprice
        sectionTables = soup.find('table', {"class": "solid_1_padding_3_2_tbl"})
        # trfromTable3 = sectionTables.findAll('tr')[3]
        # tdRows =trfromTable3[3].findAll('td')       => equals to sectionTables.findAll('tr')[3].find('td').getText()
        # endprice = tdRows[0].getText()
        endprice = sectionTables.findAll('tr', limit=5)[3].find('td').getText()


        # print ("stockId:"+stockId+" endprice:"+endprice+"  stockdiv:"+stockdiv+" monetdiv:"+moneydiv+"  lastyesrEps:"+lastyesrEps+"  thisyearEps:"+thisyearEps)
        singleStockInfo = [stockId, endprice, last2yearStockdiv, last2yearMoneydiv, stockdiv, moneydiv, previous2yearEps, lastyesrEps, thisyearEps]
        AllInfoList.append(singleStockInfo)
        
        count+=1
        print ('Finish scrapy {} stock'.format(count))

        # Dont have to sleep when scarpy to the end stockId 
        if stockId == stockIdList[-1]:
                #back door for diviendYearStr
                globalsVar.setDiviendYearStrList([lastYearDiviendStr, last2yearDiviendStr])
                #back door for getEPSYearStr buz only do once
                for i in range(2, 4):
                        globalsVar.setEPSYearStrList(trfromTable2[i].find('td').getText())
                break
        # avoid for anti-scrapy rules, dont request too mush time in a loop
        time.sleep(random.uniform(7, 11))
        
#-------time measure end---------#
    tEnd = time.time()
    # print ("It cost %f sec to finish" % (tEnd - tStart))

    print ('All data to csv')
    print(AllInfoList)
    csvModule.write2excel(AllInfoList)

# if stockid deleted from stockcsv then the same stockid rows in resultcsv must be deleted.
def syncfiledata(stockIdListFromStockCsv, stockIdListFromResultCsv):
    diffList = []
    # print('Before diff two csv stockcsv: {} resultcsv: {} '.format(stockIdListFromStockCsv, stockIdListFromResultCsv))
    if stockIdListFromResultCsv:
        diffList = csvModule.diffList(stockIdListFromStockCsv, stockIdListFromResultCsv)
        print ('diff stock id in two csv: {}'.format(diffList))
        dataFilePath = 'resultx.xlsx'
        df = pd.read_excel(dataFilePath,sheet_name='result', encoding='big5', keep_default_na=False)

        deletedStockIdxlist = []
        for stockid in diffList:
                try:
                    # if stockcsv has stockid but resultcsv doesnt have difflist stockid then index() will ValueError
                    idx = stockIdListFromResultCsv.index(stockid)
                    deletedStockIdxlist.append(idx)
                except ValueError:
                    continue
        writer = pd.ExcelWriter('resultx.xlsx', engine='xlsxwriter')
        # drop the rows by getting diff IdList[]
        df.drop(deletedStockIdxlist, inplace=True)
        df.to_excel(writer, sheet_name='result', index=False)

        # sheet2
        wb = load_workbook(filename = 'resultx.xlsx')
        sheet_ranges = wb['record']
        data_rows = []
        for row in sheet_ranges.values:
            data_cols = []
            for cell in row:
                data_cols.append(cell)
            data_rows.append(data_cols)
        # print(data_rows)
        df2 = pd.DataFrame(data_rows)
        # print(df2)
        df2.to_excel(writer, sheet_name='record', index=False, header=False)
        writer.save()
    print('Finish sync data')

if __name__ == '__main__':
    print ('Backup lastest resultx.xlsx file to /backup/')
    csvModule.backupfile('resultx.xlsx')

    print ('Program start')
    stockIdList = getStockIdInfoList()
    if not stockIdList:
        sys.exit('No stockId in stock.csv')
    
    # using map() to perform conversion from str list to int list
    stockIdListFromStockCsv = list(map(int, stockIdList)) #stockIdList read from stock.csv
    stockIdListFromResultCsv = csvModule.getdatalistfromcolumnXlsx('股號', 'result') # read from result.csv
    print('before sync')


    try:
        syncfiledata(stockIdListFromStockCsv, stockIdListFromResultCsv)
    except PermissionError:
        #syncfiledata will do to_csv so if the data is opening than will throw PermissionError
        sys.exit("[Presmission Error]Probably result.csv is opening by others process")
    except Exception as e:
        sys.exit(e)
    print('start scrapy')
    scrapyData(stockIdList)
    print('Program Finish')
