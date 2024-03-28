import requests
from bs4 import BeautifulSoup
import pandas as pd

# 定義函式來抓取資料

def get(url):
    headers={"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    response = requests.get(url,headers=headers)
    if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # 找到表格元素
            table = soup.find('td', class_='t0')
            table = soup.find('table', class_='t01')
            
            if table:
                # 建立空的資料列表
                buy_Rank=[]
                buy_Stock_Name=[]
                buy_Volume=[]
                buy_Change=[]
                sell_Rank=[]
                sell_Stock_Name=[]
                sell_Volume=[]
                sell_Change=[]
                # 找到表格中所有的行
                table0 = soup.find_all('td', class_='t3n0')
                table1 = soup.find_all('td', class_='t3t1')
                table2 = soup.find_all('td', class_='t3n1')
                data = []
                for td in table2:
                    text = td.get_text().strip()
                    if text != '0':
                        data.append(text)
                table2=data
                for i in range(0,100,2):
                    buy_Rank.append(table0[i].text.strip())
                    sell_Rank.append(table0[i+1].text.strip())

                    buy_Stock_Name.append(table1[i].text.strip())
                    sell_Stock_Name.append(table1[i+1].text.strip())
                for i in range(0,199,4):
                    buy_Volume.append(table2[i])
                    buy_Change.append(table2[i+1])
                    

                    sell_Volume.append(table2[i+2])
                    sell_Change.append(table2[i+3])
        
                s1=pd.Series(buy_Rank)
                s2=pd.Series(buy_Stock_Name)
                s3=pd.Series(buy_Volume)
                s4=pd.Series(buy_Change)
                s5=pd.Series(sell_Rank)
                s6=pd.Series(sell_Stock_Name)
                s7=pd.Series(sell_Volume)
                s8=pd.Series(sell_Change)
            
                data={
                    "名次":s1,
                    "股票名稱":s2,
                    "超張數":s3,
                    "收盤價":s4,
                    "  ":"",
                    "名次:":s5,
                    "股票名稱:":s6,
                    "張數:":s7,
                    "收盤價:":s8,
                    }
                return data                     
            else:
                print("找不到表格")
    else:
            print("無法取得頁面")

import requests
from bs4 import BeautifulSoup

def get_day(url):

    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        date_element = soup.find('div', class_='t11')
        if date_element:
            date = date_element.text.strip()
            return date
        else:
            return "日期未找到"
    else:
        return "無法取得網頁內容"


url="https://fubon-ebrokerdj.fbs.com.tw/Z/ZG/ZGK_DD.djhtm"
day = get_day(url)
data=get(url)
df=pd.DataFrame(data)
print(f"------------買超----------投信-{day}------------賣超-------------------")
print(df.to_string(index=False))

# 等待用戶輸入，保持終端窗口打開
input("按下 Enter 鍵退出...")