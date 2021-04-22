from bs4 import BeautifulSoup
import requests
import pandas as pd
import datetime
from firebase import firebase

url = 'https://www.psx.com.pk/market-summary/'
page = requests.get(url)
html = page.text
soup = BeautifulSoup(html, 'lxml')
trs = soup.findAll('tr')
df = pd.read_excel('stock_companies.xlsx')
values = df.values

data = []

for i in range(len(values)):
  ticker = values[i][0].split(' - ')[0]
  psx_name = values[i][2]

  for j in trs[4:]:
    try:
      if psx_name in j.td.text:
        substring = j.text.split('\n')[4:10]
        open_val = str(float(substring[0]))
        high = str(float(substring[1]))
        low = str(float(substring[2]))
        close = str(float(substring[3]))
        change = str(float(substring[4]))
        vol = substring[5]
        curr_date = datetime.date.today().strftime('%d-%b-%Y')
        data_dict = {'Open': open_val,
                     'High': high,
                     'Low': low,
                     'Close': close,
                     'Change': change,
                     'Volume': vol,
                     'Date': curr_date}
        data.append([ticker, data_dict])
        break
    except:
      pass

fb = firebase.FirebaseApplication('https://historicaldatafyp-default-rtdb.firebaseio.com/', None)
for i in range(len(data)):
  ticker = data[i][0]
  data = data[i][1]
  vals = fb.get('historicaldatafyp-default-rtdb/Stocks/'+ticker,'')
  next_index = df.index.max()+1
  res = fb.put('historicaldatafyp-default-rtdb/Stocks/'+ticker,str(next_index),data)
  print(res)

#fb.post('historicaldatafyp-default-rtdb/Stocks/runtime',str(datetime.date.today()))
