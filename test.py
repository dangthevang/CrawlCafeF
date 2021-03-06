from base import setup as F
import time
import pandas as pd
# web = F.FinancailStatement()
# web.get_Income("AAA",year=2022,month=1,type_="Y",times=10).to_csv("AAA.csv")
import multiprocessing

def KeoBaoCaoTaiChinh(symbol):
  time = 90
  web = F.FinancailStatement()
  # t = web.getTable('hose/FCN-cong-ty-co-phan-fecon.chn')
  i = web.get_Income(symbol,year=2022,times=time,type_="Q")
  print(i)
  b = web.get_Balance(symbol,year=2022,times=time,type_="Q")
  print(b)
  c = web.get_CashFlowIndirect(symbol,year=2022,times=time,type_="Q")
  print(c)
  d = web.get_CashFlowDirect(symbol,year=2022,times=time,type_="Q")
  print(d)
  # web.driver.close()
def KeoCoTuc(symbol,link):
  web = F.Dividend()
  df = pd.DataFrame({})
  # t = web.getTable('hose/FCN-cong-ty-co-phan-fecon.chn')
  df = web.FilterData(link)
  df.to_csv("Data/Dividend/"+symbol+".csv",index=False)
  # web.driver.close()
def LayVoLumeHienTai(symbol,link):
  web = F.Volume()
  df = pd.DataFrame({})
  # t = web.getTable('hose/FCN-cong-ty-co-phan-fecon.chn')
  df = web.getVolumeNow(link)
  df.to_csv("Data/Volume/"+symbol+".csv",index=False)
  # web.driver.close()
def LayDanhSachCongTy():
  web = F.ListCompany()
  web.get_all_symbol().to_csv("TatCaCongTy.csv")


def lay_delisted(symbol,link):
  try:
    df = pd.read_csv("data/"+symbol+".csv")
  except:
    print(symbol)
    web = F.Listed()
    web.List_Listed_Delisted(symbol,link).to_csv("data/"+symbol+".csv")

def lay_volume(symbol,link):
  web = F.Volume()
  print(web.getVolumeEvent(symbol))
def close(symbol):
  try:
    df = pd.read_csv("data/"+symbol+".csv")
  except:
    print(symbol)
    web=F.Close(symbol=symbol)
    return web.DownloadClose()
def close(symbol):
  try:
    df = pd.read_csv(symbol+".csv")
  except:
    web=F.Close(symbol=symbol)
    return web.DownloadCloseFund()
def infor(symbol,link):
  web = F.Listed()
  web.List_Listed_Delisted(symbol,link).to_csv("haha.csv")
KeoBaoCaoTaiChinh("AAA")
# infor("NKD",'hose/NKD-cong-ty-co-phan-che-bien-thuc-pham-kinh-do-mien-bac.chn')
# KeoBaoCaoTaiChinh("AAA")
# symbol="CLM"
# time = 22
# web = F.FinancailStatement()
# i = web.get_Income(symbol,year=2021,times=time,type_="Y")
# print(i)
# close("AAA").to_csv("haha.csv")
# def multip():
#     data = pd.read_csv("TatCaCongTy.csv")
#     # ,engine="openpyxl"
#     data2 = pd.read_csv("AllCompanyDone_(1).csv")
#     data = data2.merge(data,on="Symbol",how="left")
#     Symbol = data["Symbol"][0:]
#     Link = data["Link"][0:]
#     # Symbol = ["A32"]
#     pool = multiprocessing.Pool(processes=2)
#     for symbol in range(len(Symbol)):
#       pool.apply_async(lay_delisted,args=(Symbol[symbol],Link[symbol],))
#     pool.close()
#     pool.join()

# if __name__ == '__main__':
#     multip()
      
