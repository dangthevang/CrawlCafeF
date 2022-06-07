from base import setup as F
import time
import pandas as pd
# web = F.FinancailStatement()
# web.get_Income("AAA",year=2022,month=1,type_="Y",times=10).to_csv("AAA.csv")
import multiprocessing

def run1(symbol):
  web = F.FinancailStatement()
  df = pd.DataFrame({})
  # t = web.getTable('hose/FCN-cong-ty-co-phan-fecon.chn')
  i = web.get_Income(symbol,year=2021,times=20,type_="Y")
  df = df.append(i,ignore_index=True)
  b = web.get_Balance(symbol,year=2021,times=20,type_="Y")
  df = df.append(b,ignore_index=True)
  c = web.get_CashFlowIndirect(symbol,year=2021,times=20,type_="Y")
  df = df.append(c,ignore_index=True)
  d = web.get_CashFlowDirect(symbol,year=2021,times=20,type_="Y")
  df = df.append(d,ignore_index=True)
  df.to_csv("Data/Financail/"+symbol+".csv",index=False)
  # web.driver.close()
def run2(symbol,link):
  web = F.Dividend()
  df = pd.DataFrame({})
  # t = web.getTable('hose/FCN-cong-ty-co-phan-fecon.chn')
  df = web.FilterData(link)
  df.to_csv("Data/Dividend/"+symbol+".csv",index=False)
  # web.driver.close()
def run3(symbol,link):
  web = F.Volume()
  df = pd.DataFrame({})
  # t = web.getTable('hose/FCN-cong-ty-co-phan-fecon.chn')
  df = web.getVolumeNow(link)
  df.to_csv("Data/Volume/"+symbol+".csv",index=False)
  # web.driver.close()
def multip():
    data = pd.read_csv("all.csv")
    Symbol = data["Symbol"][0:500]
    Link = data["Link"][0:500]
    # Symbol = ["A32"]
    pool = multiprocessing.Pool(processes=3)
    for symbol in range(len(Symbol)):
      pool.apply_async(run3,args=(Symbol[symbol],Link[symbol],))
    pool.close()
    pool.join()

if __name__ == '__main__':
    multip()
      
