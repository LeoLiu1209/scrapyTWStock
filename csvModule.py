import pandas as pd
import os
import time
import datetime
import numpy as np
import globalsVar

currentWorkSpace = os.getcwd()


def write2csv(AllInfoList):
    dataFilePath = currentWorkSpace+'/result.csv'
    # to do : eps 年會有問題改直接抓欄位 => 
    currentYear = str(int(globalsVar.EPSYearStrList[0])+1)
    previousYear = globalsVar.EPSYearStrList[0]
    previous2Years = globalsVar.EPSYearStrList[1]

    print ('previous {} previous2year {}'.format(previousYear, previous2Years)) 
    # get alltitle
    allTitleList = getuserdefinetitle()
    #將股利從西元轉明國年
    RocPreviousYeay = convertToRocYear(globalsVar.DiviendYearStrList[0])
    RocPrevious2Year = convertToRocYear(globalsVar.DiviendYearStrList[1])
    # program define title
    programDefineTitleList=['股號', '收盤價', RocPrevious2Year+'股票股利', RocPrevious2Year+'現金股利',RocPreviousYeay+'股票股利', RocPreviousYeay+'現金股利', previous2Years+'年EPS', previousYear+'年EPS', currentYear+'年EPS']
    # find diff title 
    userDefineTitleList = diffList(allTitleList, programDefineTitleList)
    print ('User define title: {}'.format(userDefineTitleList))
    print ('all Title  {}'.format(allTitleList))
    
    # data must be 2d, other pd.DataFrame will meet exception
    df = pd.DataFrame(data=AllInfoList, columns=programDefineTitleList)
    AllInfoListSize = len(AllInfoList)
    # build dict to keep user define title and value
    dictuserdefine = {}

    if len(getdatalistfromcolumn('股號')) == 0:
        # df = pd.DataFrame(data=AllInfoList, columns=allTitleList)
        # set default value if first title scrapy and already had user define title
        userDefineRowsSize = ['Na'] * AllInfoListSize
        # assign user define data to column
        for userDefineKey in userDefineTitleList:
            df[userDefineKey] = userDefineRowsSize
    else :
        print ('len AllingoList {}'.format(len(AllInfoList)))
        for userDefineColumnValues in userDefineTitleList:
            value = getdatalistfromcolumn(userDefineColumnValues)
            # add new stock in stockcsv and set count how many rows user define value we have to set to na
            # ex  1260   1
            #     2260   na   => AllInfoListSize =2 val = 1 so we need to set one more rows to na
            # list [1,2] + list [3,4] => [1,2,3,4]
            dictuserdefine[userDefineColumnValues]=value + ['Na'] * (AllInfoListSize - len(value))
        print ('user define dict {}'.format(dictuserdefine))
 
        # assign user define data to column
        for userDefineKey in userDefineTitleList:
            df[userDefineKey] = dictuserdefine[userDefineKey]

    # encoding to big5 for zh-tw
    df.to_csv(dataFilePath, encoding='big5', index=False)
    print ('Done Scrapy with {} stockId.'.format(len(AllInfoList)))

def mockwrite2csv(AllInfoList):
    dataFilePath = os.getcwd()+'/test/result.csv'
    # get alltitle
    allTitleList = getuserdefinetitle()
    # add '.csv' at the end of the current workspace path
    programDefineTitleList=['股號', '收盤價', '股票股利', '現金股利', '2018年EPS', '2019年EPS']
    # find diff title 
    userDefineTitleList = diffList(allTitleList, programDefineTitleList)
    print ('userdefine')
    print (userDefineTitleList)
    # build dict to keep user define title and value
    dictuserdefine = {}
    for userDefineColumnValues in userDefineTitleList:
        value = getdatalistfromcolumn(userDefineColumnValues)
        dictuserdefine[userDefineColumnValues]=value
    print ('user define dict')
    print (dictuserdefine)

    # data must be 2d, other pd.DataFrame will meet exception
    df = pd.DataFrame(data=AllInfoList, columns=programDefineTitleList)

    # assign user define data to column
    for userDefineKey in userDefineTitleList:
        df[userDefineKey] = dictuserdefine[userDefineKey]

    # encoding to big5 for zh-tw
    df.to_csv(dataFilePath, encoding='big5', index=False)
    # print ('Done!!')

def readStockInfoFromCSV():
    StockIdandNameList = []
    dataFilePath = currentWorkSpace+'/stock.csv'
    df = pd.read_csv(dataFilePath, encoding='utf-8', sep = "\t")
    #get col 'Info' data and convert to list
    StockIdandNameList = list(df.loc[:, 'Info'])
    return StockIdandNameList

def mockreadStockInfoFromCSV():
    mydata = []
    dataFilePath = currentWorkSpace+'/test/stock.csv'
    df = pd.read_csv(dataFilePath, encoding='utf-8', sep = "\t")
    #get col 'Info' data and convert to list
    mydata = list(df.loc[:, 'Info']) 
    return mydata

def getuserdefinetitle():
    dataFilePath = currentWorkSpace+'/result.csv'
    df = pd.read_csv(dataFilePath, encoding='big5')
    # print (df.columns.values.tolist())
    return df.columns.values.tolist()

def getdatalistfromcolumn(columeName):
    dataFilePath = currentWorkSpace+'/result.csv'
    df = pd.read_csv(dataFilePath, encoding='big5', keep_default_na=False)
    # df[columeName] = df[columeName].replace(np.nan, "cc")
    StockIdandNameList = list(df.loc[:, columeName])
    return StockIdandNameList

def diffList(list1, list2):
    return list(set(list1).symmetric_difference(set(list2)))

def convertToRocYear(year):
    return str(int(year)-1911)