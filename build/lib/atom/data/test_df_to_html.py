import pandas as pd
import sqlite3



connection = sqlite3.connect(r'D:\Workspace\JiYuan\Atom\Demo\test\atom.db').cursor()
df = pd.read_sql('SELECT * FROM DataInformation',connection.connection)
df.to_html('datatest.html')