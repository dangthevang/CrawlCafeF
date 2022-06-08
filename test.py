from base import setup as F
import time
import pandas as pd
# web = F.FinancailStatement()
# web.get_Income("AAA",year=2022,month=1,type_="Y",times=10).to_csv("AAA.csv")
import multiprocessing

def KeoBaoCaoTaiChinh(symbol):
  time = 20
  web = F.FinancailStatement()
  df = pd.DataFrame({})
  # t = web.getTable('hose/FCN-cong-ty-co-phan-fecon.chn')
  i = web.get_Income(symbol,year=2021,times=time,type_="Y")
  df = df.append(i,ignore_index=True)
  b = web.get_Balance(symbol,year=2021,times=time,type_="Y")
  df = df.append(b,ignore_index=True)
  c = web.get_CashFlowIndirect(symbol,year=2021,times=time,type_="Y")
  df = df.append(c,ignore_index=True)
  d = web.get_CashFlowDirect(symbol,year=2021,times=time,type_="Y")
  df = df.append(d,ignore_index=True)
  df.to_csv(symbol+".csv",index=False)
  print(symbol,df.columns)
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
  web = F.Listed()
  print(web.List_Listed_Delisted(symbol,link))

def lay_volume(symbol,link):
  web = F.Volume()
  print(web.getVolumeEvent(symbol))

KeoBaoCaoTaiChinh("QBS")
# def multip():
#     data = pd.read_csv("all.csv")
#     data2 = pd.read_excel("List_Com_First (1_4).xlsx",engine="openpyxl")
#     data = data2.merge(data,on="Symbol",how="left")
#     Symbol = data["Symbol"][0:500]
#     Link = data["Link"][0:500]
#     # Symbol = ["A32"]
#     pool = multiprocessing.Pool(processes=2)
#     for symbol in range(len(Symbol)):
#       pool.apply_async(run1,args=(Symbol[symbol],))
#     pool.close()
#     pool.join()

# if __name__ == '__main__':
#     multip()
      
