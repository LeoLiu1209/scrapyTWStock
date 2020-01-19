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
    lastYearDiviendStr = str(int(currentYear)-1)#2019
    last2yearDiviendStr = str(int(currentYear)-2)#2018
    last3yearDiviendStr = str(int(currentYear)-3)#2017
    AllInfoList = []
    count = 0
    for stockId in stockIdList:

        # StockDetail.asp contains all the data we need to scrapy
        url = 'https://goodinfo.tw/StockInfo/StockDividendPolicy.asp?STOCK_ID='+stockId
        
        # request page and return page
        soup = requestPage(url)
        if soup == None:
            sys.exit('Internet error!! \nProgram finish')

        sectionTables = soup.findAll('table', {"class": "solid_1_padding_4_0_tbl"})
        trfromTable2 = sectionTables[2].findAll('tr', limit=20)
        trfromTable2Size = len(sectionTables[2].findAll('tr', limit=20))
        previous2yearEps = 0
        lastyesrEps = 0
        thisyearEps = 0
        for i in range(4, trfromTable2Size):
            tdRows =trfromTable2[i].findAll('td')
            year = tdRows[0].getText()
            if not year.isdigit():
                # print('not digit')
                continue
            if year == lastYearDiviendStr:
                moneydiv = tdRows[3].getText()
                stockdiv = tdRows[6].getText()
            elif year == last2yearDiviendStr:
                last2yearMoneydiv = tdRows[3].getText()
                last2yearStockdiv = tdRows[6].getText()
            elif year == last3yearDiviendStr:
                previous2yearEps = tdRows[-4].getText()
                if previous2yearEps is not '0':
                    break
        
        #endprice
        sectionTables = soup.find('table', {"class": "solid_1_padding_3_2_tbl"})
        # trfromTable3 = sectionTables.findAll('tr')[3]
        # tdRows =trfromTable3[3].findAll('td')       => equals to sectionTables.findAll('tr')[3].find('td').getText()
        # endprice = tdRows[0].getText()
        endprice = sectionTables.findAll('tr', limit=5)[3].find('td').getText()
        time.sleep(random.uniform(6, 8))

        #eps
        urleps = 'http://goodinfo.tw/StockInfo/StockBzPerformance.asp?STOCK_ID='+stockId
        # request page and return page
        soup = requestPage(urleps)
        if soup == None:
            sys.exit('Internet error!! \nProgram finish')
        
        sectionTables = soup.findAll('table', {"class": "solid_1_padding_4_0_tbl"})
        trfromTable2 = sectionTables[1].findAll('tr', limit = 10)
        trfromTable2Size = len(sectionTables[1].findAll('tr', limit = 10))

        for i in range(2, trfromTable2Size):
            tdRows =trfromTable2[i].findAll('td') #for this year rows
            year = tdRows[0].getText()
            if year == last2yearDiviendStr:
                thisyearEps = trfromTable2[i-1].findAll('td')[-3].getText()
                lastyesrEps = tdRows[-3].getText()
                previous2yearEps = trfromTable2[i+1].findAll('td')[-3].getText()
                break


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
            globalsVar.setEPSYearStrList([last2yearDiviendStr, last3yearDiviendStr])
            break
        # avoid for anti-scrapy rules, dont request too mush time in a loop
        time.sleep(random.uniform(7, 11))
        
#-------time measure end---------#
    tEnd = time.time()
    # print ("It cost %f sec to finish" % (tEnd - tStart))

    # print ('All data to csv')
    # print(AllInfoList)
    csvModule.write2excel(AllInfoList)

# if stockid deleted from stockcsv then the same stockid rows in resultcsv must be deleted.
def syncfiledata(stockIdListFromStockCsv, stockIdListFromResultCsv):
    diffList = []
    # print('Before diff two csv stockcsv: {} resultcsv: {} '.format(stockIdListFromStockCsv, stockIdListFromResultCsv))
    if stockIdListFromResultCsv:
        diffList = csvModule.diffList(stockIdListFromStockCsv, stockIdListFromResultCsv)
        if diffList:    
            # print ('diff stock id in two csv: {}'.format(diffList))
            print ('[!! 需更新 !!] 以下追蹤股票有異動 {}，請前往 record 進行更新'.format(diffList))
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
    print('同步完成 stockx resultx')
    return diffList

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
    print('開始同步 stockx resultx')

    diffList = []
    try:
        diffList = syncfiledata(stockIdListFromStockCsv, stockIdListFromResultCsv)
    except PermissionError:
        #syncfiledata will do to_csv so if the data is opening than will throw PermissionError
        sys.exit("[Presmission Error]Probably result.csv is opening by others process")
    except Exception as e:
        input('[!!失敗!!] 跑程式前請將 result.xlsx 關閉')
        sys.exit(1)
    print('開始爬取資料')
    scrapyData(stockIdList)
    print('完成爬取資料')
    if diffList:
        print ('[!! 需更新 !!] 以下追蹤股票有異動 {}，請前往 record 進行更新'.format(diffList))
    input('[!! 成功 !!] 成功產製報表')
