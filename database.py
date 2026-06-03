import pyodbc
# print(pyodbc.drivers())
conn = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=LAPTOP-480JM2PF\SQLEXPRESS;"
    "DATABASE=Expensetracker;"
    "Trusted_Connection=yes;"
)

cursor = conn.cursor()
cursor.execute("""select * from Expenses""")
rows=cursor.featchall()
print(rows)