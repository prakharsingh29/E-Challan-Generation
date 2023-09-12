import sqlite3

conn = sqlite3.connect('Project.db')
c = conn.cursor()
#c.execute("PRAGMA table_info(Challan)")
#c.execute("PRAGMA table_info(Vehicle)")
c.execute('select * from Challan')

print(c.fetchall())
conn.commit()
conn.close()