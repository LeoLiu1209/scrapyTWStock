import pandas as pd
import os
# add '.csv' at the end of the current workspace path
dataFilePath = os.getcwd()+'result.csv'

stockIdList =[['台積電','0.8'],['2330','99']]
# data must be 2d, other pd.DataFrame will meet exception
df = pd.DataFrame(data=stockIdList, columns=['StockID', 'stcokDiv'])
# encoding to big5 for zh-tw
df.to_csv(dataFilePath, encoding='big5', index=False) 
