# from CrawlDataCafeF.base.setup import FinancailStatement
from base.setup import FinancailStatement
import pandas as pd

class FormatFinancailStatement(FinancailStatement):
    def __init__(self):
        super().__init__()

    def formatField(self, df):
        dict_ = {}
        for i in df.index:
            df["field"][i] = ''.join(
                [i for i in df["field"][i] if not i.isdigit()])
            dict_[df["field"][i]] = 0

        for i in df.index:
            dict_[df["field"][i]] += 1
            df["field"][i] = df["field"][i]+"__"+str(dict_[df["field"][i]])
        return df

    def getData(self,  times=1):
        df = pd.DataFrame({"field": []})
        while times != 0:
            times -= 1
            df1 = self.getTable()
            col_key = []
            for i in df1:
                if i in df.columns:
                    col_key.append(i)
            df = pd.merge(df, df1, on=col_key, how="outer")
            self.clickPerious()
        return df
