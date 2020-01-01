import csvModule
import re
import pandas as pd
import os

# #csvModule.mockwrite2csv()

# # read from CSV and return StockInfoList
# # lista = csvModule.readStockInfoFromCSV()

# #test connect 
# # infolist = csvModule.readStockInfoFromCSV()
# # # print (infolist)
# # alist = []
# # for ele in infolist:
# #     alist.append(re.findall(r'^\d{4,}[a-zA-Z]{0,1}', ele)[0])
   
# # print (alist)

# #test year
# # import time
# # year = time.strftime('%Y') # or "%y"
# # if '2019' == year:
#     # print('same')

# import ua
# import requests
# from bs4 import BeautifulSoup
# import time

# testIdList = ['2330','1216','2880']

# # for stockId in testIdList:
# fakeUA = ua.getFakeUA()
# print (fakeUA)
# # StockDetail.asp contains all the data we need to scrapy
# url = 'https://goodinfo.tw/StockInfo/StockDetail.asp?STOCK_ID='+'qwe1'
# headers = {
#     'accept':'*/*',
#     'accept-encoding':'gzip, deflate, br',
#     'origin': 'https://goodinfo.tw',
#     'User-Agent': fakeUA,
# }
# # make agent pool #todo: make multi agent pool
# r = requests.get(url, headers = headers)
# r.encoding = 'utf-8'
# print(r.status_code)
# soup = BeautifulSoup(r.text, 'html.parser')

# sectionTables = soup.find('table', {"class": "solid_1_padding_3_2_tbl"})
# endprice = sectionTables.findAll('tr', limit=5)[3].find('td').getText()
# print(endprice)
# time.sleep(3)


# print("out")

# import datetime
# now = datetime.datetime.now()
# print (now.year)
# print (now.year-1)


AllInfoList = []

# print(AllInfoList)
# csvModule.write2csv(AllInfoList)

# titleList = csvModule.getuserdefinetitle()

# csvModule.getdatalistfromcolumn()

# singleStockInfo = ['2330','305.5', '1.52', '2.28', '13.54', '8.84']
# AllInfoList = [['2330','305.5', '1.52', '2.28', '13.54', '8.84'], ['2331','305.5', '1.52', '2.28', '13.54', '8.84']]
# aList = csvModule.getdatalistfromcolumn()
# for i in len(aList):
#     singleStockInfo.append(ele)

# # csvModule.write2csv(AllInfoList)
# AllInfoList.append(singleStockInfo)
# csvModule.mockwrite2csv(AllInfoList, titleList)

# csvModule.mockwrite2csv(AllInfoList)
'''
# 保留客戶自定義的欄位步驟
#1 找出程式定義的欄位名稱 和 現有 excel (readcsv) 的欄位 差異之處 => 差異之處就是要保留的欄位
#2 利用 getdatalistfromcolumn 將 colume的val 放進 dict 裡 {'test':[123,456]}
#3 利用 df特性 df['欄位名稱'] = [data] 裝進去就可以把val 放進該 column
#4 寫入 csv
# list1 = ['1','2','test','test02'] 
list1 = csvModule.getuserdefinetitle()
print ('get user define')
print (list1)
list2 = ['股號', '收盤價', '股票股利', '現金股利', '8年EPS', '9年EPS']
list3 = csvModule.diffList(list1, list2)
print ('diff  title')
print (list3)
dictuserdefine = {}
for ele in list3:
    data= csvModule.getdatalistfromcolumn(ele)
    print(data)
    dictuserdefine[ele]=data

print(dictuserdefine)
#  # add '.csv' at the end of the current workspace path
dataFilePath = os.getcwd()+'/test/result.csv'
titleList=['股號', '收盤價', '股票股利', '現金股利', '8年EPS', '9年EPS']
# # data must be 2d, other pd.DataFrame will meet exception
AllInfoList =[['2330', '100', '0', '0', '9', '8'],['2331', '2', '3', '4', '5', '6']]
# print (AllInfoList)
df = pd.DataFrame(data=AllInfoList, columns=titleList)


for ele in list3:
    df[ele] = dictuserdefine[ele]

# # encoding to big5 for zh-tw
df.to_csv(dataFilePath, encoding='big5', index=False)
# print ('Done!!')
'''
AllInfoList =[['2330', '100', '0', '0', '9', '8'],['2331', '2', '3', '4', '5', '6']]
csvModule.write2csv(AllInfoList)
# print (len(csvModule.getdatalistfromcolumn('股號')))