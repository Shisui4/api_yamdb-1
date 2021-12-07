import csv
import sqlite3

from django.core.management.base import BaseCommand, CommandError
from .models import Genre

DB_PATH = 'db.sqlite3.db'
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS genre (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            slug TEXT);
""")

CSV_PATH = 'static/data/genre.csv'

with open(CSV_PATH, 'r', encoding='utf8') as csv_file:
    dr = csv.DictReader(csv_file, delimiter=',')
    to_db = [(i['id'], i['name'], i['slug']) for i in dr]

cur.executemany("INSERT INTO genre (id, name, slug) VALUES (?, ?, ?);", to_db)
conn.commit()
conn.close()
