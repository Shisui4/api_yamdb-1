import csv, sqlite3

con = sqlite3.connect('api_yamdb/api_yamdb/db.sqlite3')
cur = con.cursor()
cur.execute("""CREATE TABLE category (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            slug TEXT
)""")

with open('api_yamdb/api_yamdb/static/data/category.csv','r', encoding="utf8") as f:
    dr = csv.DictReader(f, delimiter=";")
    to_db = [(i['name'], i['slug']) for i in dr]

cur.executemany("INSERT INTO category (name, slug) VALUES (?, ?);", to_db)
con.commit()
con.close()