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
import time
year = time.strftime('%Y') # or "%y"
if '2019' == year:
    print('same')