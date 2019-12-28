import pandas as pd
import os

def write2csv(AllInfoList):
    # add '.csv' at the end of the current workspace path
    dataFilePath = os.getcwd()+'/result.csv'
    titleList=['股號', '收盤價', '股票股利', '現金股利', '去年EPS', '今年EPS']
    # data must be 2d, other pd.DataFrame will meet exception
    df = pd.DataFrame(data=AllInfoList, columns=titleList)
    # encoding to big5 for zh-tw
    df.to_csv(dataFilePath, encoding='big5', index=False)
    print ('Done!!')

def mockwrite2csv():
    mockList = [['1402', '30', '0.8', '0.95', '2.41', '1.69'], ['2330', '338', '1.52', '2.28', '13.54', '8.84']]
     # add '.csv' at the end of the current workspace path
    dataFilePath = os.getcwd()+'/result.csv'
    titleList=['股號', '收盤價', '股票股利', '現金股利', '去年EPS', '今年EPS']
    # data must be 2d, other pd.DataFrame will meet exception
    df = pd.DataFrame(data=mockList, columns=titleList)
    # encoding to big5 for zh-tw
    df.to_csv(dataFilePath, encoding='big5', index=False)
    print ('Done!!')
