import pymysql
import pandas as pd

# Connect to your MySQL database
connection = pymysql.connect(
        host='localhost',
        user='root',
        password='admin@123',
        database='food_wastage_solutn'
    )
cur = connection.cursor() 
query = """ """ 
cur.execute(query)
# Fetch and load into DataFrame
data = cur.fetchall() 
df = pd.DataFrame() 
print(df)