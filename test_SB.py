from base import Stock_Biz as F
import pandas as pd
data = pd.read_excel("List_Com_Phase1.xlsx")
for symbol in data["Symbol"]:
  try:
    t = pd.read_csv(f"data/{symbol}.csv")
  except FileNotFoundError:
    try:
      test = F.Close(symbol,"09/06/2022")
      test.DownloadClose().to_csv(f"data/{symbol}.csv")
      print(symbol)
    except ValueError:
      pass