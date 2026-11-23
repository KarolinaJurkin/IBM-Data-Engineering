import pandas as pd
import requests
import sqlite3 
from bs4 import BeautifulSoup as bs

url = 'https://web.archive.org/web/20230902185655/https://en.everybodywiki.com/100_Most_Highly-Ranked_Films'
db_name = 'Movies.db'
table_name = "Top50"
csv_path = "/home/project/top50_movies.csv"
df = pd.DataFrame(columns=["AverageRank", "Title", "Year"])
count = 0 # counter for getting 50 results

html_page = requests.get(url).text
soup = bs(html_page,"html.parser")
tables = soup.find_all('tbody')
rows = tables[0].find_all('tr')

for row in rows:
    if count<50:
        col = row.find_all('td')
        if len(col) != 0: # have to check if there's data in current row (merged rows can be empty)
            dict = {"AverageRank": col[0].contents[0],
                    "Title": col[1].contents[0],
                    "Year": col[2].contents[0]} # contents return immediate child
            df1 = pd.DataFrame(dict, index=[0])
            df = pd.concat([df1, df], ignore_index = True)
            count += 1
    else:
        break

print(df) 

df.to_csv(csv_path)

conn = sqlite3.connect(db_name)
df.to_sql(table_name, conn, if_exists = 'replace', index = False)
conn.close()

