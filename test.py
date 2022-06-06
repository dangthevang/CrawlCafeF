from base import setup as F
import time

# web = F.FinancailStatement()
# web.get_Income("AAA",year=2022,month=1,type_="Y",times=10).to_csv("AAA.csv")
import multiprocessing

def run1(symbol):
  web = F.FinancailStatement()
  web.get_Income(symbol,year=2022,month=1,type_="Y",times=3).to_csv(symbol+".csv")
  # web.driver.close()

def multip():
    Symbol = ["AAA","DLG","QBS","VNM"]
    pool = multiprocessing.Pool(processes=2)
    for symbol in Symbol:
      pool.apply_async(run1,args=(symbol,))
    pool.close()
    pool.join()

if __name__ == '__main__':
    multip()
      
