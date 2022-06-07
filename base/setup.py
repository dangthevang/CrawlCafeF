from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import numpy as np
from bs4 import BeautifulSoup
import pandas as pd
import time
import re

pd.set_option('mode.chained_assignment', None)

class setup():
    def __init__(self) -> None:
        self.year = 0
        self.quater = 0
        self.day = 0
        self.symbol = ""
        try:
            self.reset_driver()
        except:
            self.reset_colab()

    def reset_colab(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome('chromedriver',chrome_options=chrome_options)

    def reset_driver(self, path="C:/webdrive/chromedriver.exe"):
        self.driver = webdriver.Chrome(executable_path=path)
    def reset_driver(self, path="C:/webdrive/chromedriver.exe"):
        self.driver = webdriver.Chrome(executable_path=path)
       

    def request_link(self,link,time=5):
        try:
            self.driver.set_page_load_timeout(time)
            self.driver.get(link)
        except:
            self.request_link(link,10)

    def format(self, time):
        s = time.split("-")
        self.year = int(s[0])
        self.quater = int(s[1])//3+1
        self.day = int(s[2])
        return self.year, self.quater
    
    def click_something_by_xpath(self, something):
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, something))
            )
            element.click()
        except:
            self.driver.refresh()
            pass

    def click_something_by_id(self, something):
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, something))
            )
            element.click()
        except:
            self.driver.refresh()
            pass

class ListCompany(setup):
    def __init__(self):
        super().__init__()
        self.link = "https://s.cafef.vn/du-lieu-doanh-nghiep.chn"
        self.request_link(self.link)
        self.table = None
        self.drop_field = ["QUỸ",  "CHỨNG QUYỀN", "NGÂN HÀNG", "BẢO HIỂM","TRÁI PHIẾU","'","CHỨNG KHOÁN"]
    def get_all_symbol(self):
        self.click_something_by_xpath('//*[@id="CafeF_ThiTruongNiemYet_Trang"]/a[2]')
        time.sleep(2)
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        arr = soup.find_all("table")
        table = pd.read_html(str(arr))[4]
        Link = []
        count = 0
        for element in arr[4].find_all("a"):
            count +=1
            if count %2 ==1:
                Link.append(element["href"])
        table["Link"] = Link
        table = table.rename(columns = {"MÃ CK":"Symbol","TÊN CÔNG TY":"Name Company","SÀN":"Exchange"})
        table = table.drop(columns=["GIÁ"])
        self.table = table
        return table

    def LocTheoSan(self,t):
        if t == "OTC":
            return False
        return True
    def LocTheoLoaiCongTy(self,t):
        t = t.upper()
        for i in self.drop_field:
            if t.find(i) != -1:
                return False
        return True

    def xetDk(self,san,name):
        return self.LocTheoSan(san) and self.LocTheoLoaiCongTy(name)

    def filter_data(self, arr=[]):
        if len(arr) != 0:
            self.drop_field = arr
        self.table["Don't Remove"] = self.table.apply(lambda row: self.xetDk(row['Exchange'],row["Name Company"]),axis=1)
        self.table = self.table[self.table["Don't Remove"]!=False].reset_index(drop=True)
        return self.table.drop(columns=["Don't Remove"])

class FinancailStatement(setup):
    def __init__(self):
        super().__init__()
        self.link = "https://s.cafef.vn/bao-cao-tai-chinh/AAA/IncSta/2021/1/0/0/ket-qua-hoat-dong-kinh-doanh-cong-ty-co-phan-nhua-an-phat-xanh.chn"
        self.driver.get(self.link)

    def setup_link(self, symbol, year,month,day, type_):
        # time = self.format(time)
        if type_ == "Y":
            time = "/".join([str(year), "0", "0", "0"])
        elif type_ == "Q":
            time = "/".join([str(year), str(month//3+1), "0", "0"])
        else:
            pass
        self.link = self.link.replace(
            "AAA", symbol).replace("2021/1/0/0", time)

    def get_Balance(self,symbol, year=2021,month=1,day=1, type_="Y", times=1):
        self.setup_link(symbol, year,month,day, type_)
        self.request_link(self.link)
        self.clickBalance()
        return self.getData(times)

    def get_Income(self,symbol, year=2021,month=1,day=1, type_="Y", times=1):
        self.setup_link(symbol, year,month,day, type_)
        self.request_link(self.link)
        self.clickIncome()
        return self.getData(times)
    
    def get_CashFlowIndirect(self,symbol, year=2021,month=1,day=1, type_="Y", times=1):
        self.setup_link(symbol, year,month,day, type_)
        self.request_link(self.link)
        self.clickCashFlowIndirect()
        return self.getData(times)
    
    def get_CashFlowDirect(self,symbol, year=2021,month=1,day=1, type_="Y", times=1):
        self.setup_link(symbol, year,month,day, type_)
        self.request_link(self.link)
        self.clickCashFlowDirect()
        return self.getData(times)
    
    def getData(self,  times=1):
        df = pd.DataFrame({"field": []})
        while times != 0:
            times -= 1
            df1 = self.getTable()
            col_key = []
            for i in df1:
              if i in df.columns:
                col_key.append(i)
            df = pd.merge(df, df1, on="field", how="outer")
            self.clickPerious()
        return df

    def getTable(self):
        page_sourse = self.driver.page_source
        soup = BeautifulSoup(page_sourse, "html.parser")
        table = soup.find('table', {'id': 'tblGridData'})
        header = pd.read_html(str(table), displayed_only=False)
        time = np.array_str(header[0][4].values)
        table = soup.find('table', {'id': 'tableContent'})
        financial = pd.read_html(str(table), displayed_only=False)
        df = financial[0][[0, 4]]
        df = df.dropna(subset=[0])
        df = df.rename(columns={0:"field",
                                4:time})
        stt = 0
        dict_ = {}
        for i in df.index:
            df["field"][i] = ''.join([i for i in df["field"][i] if not i.isdigit()])
            dict_[df["field"][i]] = 0
        
        for i in df.index:
          dict_[df["field"][i]]+=1
          df["field"][i] = df["field"][i]+"__"+str(dict_[df["field"][i]])
        return df

    def clickPerious(self):
        self.click_something_by_xpath(
            '//*[@id="tblGridData"]/tbody/tr/td[1]/div/a[1]')

    def clickAfter(self):
        self.click_something_by_xpath(
            '//*[@id="tblGridData"]/tbody/tr/td[1]/div/a[2]')

    def clickBalance(self):
        self.click_something_by_id("aNhom1")

    def clickIncome(self):
        self.click_something_by_id("aNhom2")

    def clickCashFlowIndirect(self):
        self.click_something_by_id("aNhom3")

    def clickCashFlowDirect(self):
        self.click_something_by_id("aNhom4")

    def click4Quater(self):
        self.click_something_by_id("rdo4")

    def click4Year(self):
        self.click_something_by_id("rdo0")

    def clickHalfYear(self):
        self.click_something_by_id("rdo2")

class Volume(setup):
    def __init__(self):
        super().__init__()
        self.link = "https://s.cafef.vn/"
        # self.new = 
    def setup_link(self, link):
        self.link = self.link + link
    def getVolumeNow(self,link):
        self.setup_link(link)
        self.request_link(self.link,5)
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH,'//*[@id="content"]/div/div[6]/div[5]/div/ul'))
            )
        finally:
            pass
        soup = str(element.get_attribute('innerHTML'))
        text = BeautifulSoup(soup, 'html.parser')
        title = []
        value = []
        for i in text.find_all("div",{"class":"l"}):
            title.append(i.b.text)
        for i in text.find_all("div",{"class":"r"}):
            value.append(i.text.replace("\r","").replace("\n","").replace(",","").replace("  ",''))
        return pd.DataFrame({"Title":title,"Value":value})

    def getVolumeNew(self,symbol):
        self.request_link("https://s.cafef.vn/Ajax/Events_RelatedNews_New.aspx?symbol=*&floorID=0&configID=0&PageIndex=1&PageSize=1000&Type=2".replace("*",symbol),5)
        self.driver.get(self.link)
        text = BeautifulSoup(soup, 'html.parser')

class Dividend(setup):
    def __init__(self):
        super().__init__()
        self.link = "https://s.cafef.vn/"
        self.new = None

    def setup_link(self, link):
        # https://s.cafef.vn/hose/AAA-cong-ty-co-phan-nhua-an-phat-xanh.chn
        self.link = self.link + link

    def get_new(self,link):
        self.setup_link(link)
        self.request_link(self.link,10)
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        t = soup.find_all("div",attrs={"class":"middle"})
        t1 = t[0].text
        self.new = t1.split("-")
        return self.new
    
    def FilterData(self,link):
        list_ = []
        self.get_new(link)
        for new in self.new:
            try:
                day = re.search(r'(\d+/\d+/\d+)',new).group(1)
                index_stock = new.find("Cổ tức bằng Cổ phiếu")
                index_money = new.find("Cổ tức bằng Tiền")
                scale,money = '-1','-1' 
                if index_stock != -1:
                    scale = re.search(r'(\d+:\d+)',new[index_stock:]).group(1)
                if index_money != -1:
                    money = re.search(r'([+-]?([0-9]*[.])?[0-9]+%)',new[index_money:]).group(1)
                list_.append({"Time":day,"Stock":scale,"Money":money})
            except:
                continue
        return pd.DataFrame.from_records(list_)

class Close(setup):
    pass

class Listed(setup):

    def __init__(self):
        super().__init__()
        self.link = "https://s.cafef.vn/"
        # self.new = 
    def setup_link(self, link):
        self.link = self.link + link

    def getVolumeNow(self,link):
        self.setup_link(link)
        self.request_link(self.link,5)
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH,'//*[@id="content"]/div/div[6]/div[5]/div/ul'))
            )
        finally:
            pass
        soup = str(element.get_attribute('innerHTML'))
        text = BeautifulSoup(soup, 'html.parser')
        title = []
        value = []
        for i in text.find_all("div",{"class":"l"}):
            title.append(i.b.text)
        for i in text.find_all("div",{"class":"r"}):
            value.append(i.text.replace("\r","").replace("\n","").replace(",","").replace("  ",''))
        return pd.DataFrame({"Title":title,"Value":value})
    