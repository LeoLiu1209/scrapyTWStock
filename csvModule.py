import pandas as pd
import os
import time
import datetime
import numpy as np
import globalsVar

currentWorkSpace = os.getcwd()


def write2csv(AllInfoList):
    dataFilePath = currentWorkSpace+'/result.csv'
    # to do : eps 年會有問題改直接抓欄位
    currentYear = str(int(globalsVar.EPSYearStrList[0])+1)
    previousYear = globalsVar.EPSYearStrList[0]
    previous2Years = globalsVar.EPSYearStrList[1]

    # get alltitle
    allTitleList = getuserdefinetitle()
    # add '.csv' at the end of the current workspace path
    programDefineTitleList=['股號', '收盤價', '股票股利', '現金股利', previousYear+'年EPS', currentYear+'年EPS']
    # find diff title 
    userDefineTitleList = diffList(allTitleList, programDefineTitleList)
    print ('userdefine')
    print (userDefineTitleList)
    print ('allTitleList[0]')
    print (allTitleList[0])
    
    # data must be 2d, other pd.DataFrame will meet exception
    df = pd.DataFrame(data=AllInfoList, columns=programDefineTitleList)

    # build dict to keep user define title and value
    dictuserdefine = {}
    # 判斷是否有stock資料 不然 df[userdefine] 會壞掉
    if len(getdatalistfromcolumn('股號')) == 0:
        df = pd.DataFrame(data=AllInfoList, columns=allTitleList)
    else :
        for userDefineColumnValues in userDefineTitleList:
            value = getdatalistfromcolumn(userDefineColumnValues)
            dictuserdefine[userDefineColumnValues]=value
        print ('user define dict')
        print (dictuserdefine)
    
        # assign user define data to column
        for userDefineKey in userDefineTitleList:
            df[userDefineKey] = dictuserdefine[userDefineKey]

    # encoding to big5 for zh-tw
    df.to_csv(dataFilePath, encoding='big5', index=False)
    # print ('Done!!')

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
    print ('show columns vale')
    print (StockIdandNameList)
    return StockIdandNameList

def diffList(list1, list2):
    return (list(set(list1) - set(list2)))
