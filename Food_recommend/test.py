import requests
from bs4 import BeautifulSoup
import pandas as pd

# 目标URL
url = "https://s.askci.com/data/MonthDetail/Index?zbId=a03010h&type=4&isYear=0&month=202407"

# 发送请求获取页面内容
response = requests.get(url)
response.encoding = 'utf-8'  # 根据实际页面编码设置
html_content = response.text

# 解析HTML
soup = BeautifulSoup(html_content, 'html.parser')

# 查找表格
table = soup.find('table')  # 根据实际页面的标签结构选择正确的表格

# 提取表格头部
headers = [header.text for header in table.find_all('th')]

# 提取表格内容
rows = []
for row in table.find_all('tr')[1:]:  # 跳过表头
    rows.append([cell.text for cell in row.find_all('td')])

# 将数据转换为pandas DataFrame
df = pd.DataFrame(rows, columns=headers)

# 显示爬取的表格数据
print(df)

# 可将DataFrame保存为CSV文件
df.to_csv('table_data.csv', index=False)
