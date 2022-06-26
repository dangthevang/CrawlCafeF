from bs4 import BeautifulSoup
import requests
import pandas as pd
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
pd.set_option('mode.chained_assignment', None)
import json


class Close():    
    def __init__(self,symbol="AAA",end='09/06/2022'):
        super().__init__()
        self.URL_CLOSE = "https://www.stockbiz.vn/Stocks/AAA/LookupQuote.aspx?Date=".replace("AAA",symbol)
        self.HEADERS = {'content-type': 'application/x-www-form-urlencoded', 'User-Agent': 'Mozilla'}
        self.symbol=symbol
        self.date = end
    
    def fix_url(self):
        return  self.URL_CLOSE+self.date

    def DownloadClose(self):
        return self.download_one_close().drop_duplicates(subset=['Ngày'])

    def download_batch(self,url):
        rs = requests.get(url, headers = self.HEADERS)
        soup = BeautifulSoup(rs.content, 'html.parser')
        table = soup.find_all('table',{"class":"dataTable"})
        stock_slice_batch = pd.read_html(str(table))[0]
        return stock_slice_batch

    def download_one_close(self):
        stock_data = pd.DataFrame({})
        for i in range(1000):
            stock_slice_batch = self.download_batch(self.fix_url())
            stock_data = pd.concat([stock_data, stock_slice_batch], axis=0)
            try:
              self.date = stock_slice_batch["Ngày"].values[-1]
              date_end_batch = stock_slice_batch["Ngày"].values[2]
            except:
                break
        return stock_data