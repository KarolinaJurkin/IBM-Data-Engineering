import pandas as pd
from bs4 import BeautifulSoup as bs
import sqlite3
import lxml

url = 'https://web.archive.org/web/20230902185326/https://en.wikipedia.org/wiki/List_of_countries_by_GDP_%28nominal%29'

db_name = 'World_Economies.db'
table_name = 'Countries_by_GDP'
log_file = "etl_project_log.txt"
csv_file = 'Countries_by_GDP.csv'

def load_to_csv(data):
    data.to_csv(csv_file)

tables = pd.read_html(url)
table = tables[3]

# Change text with commas to number!
table.columns = range(table.shape[1]) # replace column headers with numbers
table = table[[0, 2]] # keep only columns 0 and 2
table.columns = ['Country', 'GDP_USD_billion']
table.GDP_USD_billion = (
    pd.to_numeric(
        table.GDP_USD_billion.str.replace(',','',regex = False), # regex false is literal text
        errors = 'coerce' # errors become NA
    ) / 1000
).round(2)

load_to_csv(table)

conn = sqlite3.connect(db_name)
table.to_sql(table_name, conn, if_exists = 'replace', index = False)


q1 = f"select * from {table_name} limit 100 offset 1"
df = pd.read_sql(q1,conn)
conn.close()
print(df)
