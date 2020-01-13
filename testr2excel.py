import csvModule
import stockv2

# print(csvModule.readStockInfoFromExcel())
stockIdList = stockv2.getStockIdInfoList()
stockIdListFromStockCsv = list(map(int, stockIdList))

stockIdListFromResultCsv = csvModule.getdatalistfromcolumnXlsx('股號', 'result')

print ('stockcsv {} resultcsv {}'.format(stockIdListFromStockCsv, stockIdListFromResultCsv))

stockv2.syncfiledata(stockIdListFromStockCsv, stockIdListFromResultCsv)

stockv2.scrapyData(stockIdList)