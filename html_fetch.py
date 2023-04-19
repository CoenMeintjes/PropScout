#!/usr/bin/env python

# This program is for extracting the relevant property information and storing it in the property analysis database which can then be used for analysis.

import sqlite3
from bs4 import BeautifulSoup

conn = sqlite3.connect('parsed_links.sqlite')
cur = conn.cursor()

# Create the tables using executescript()
cur.executescript('''
DROP TABLE IF EXISTS Properties;

CREATE TABLE Properties (
    id            INTEGER PRIMARY KEY UNIQUE,
    list_number   TEXT
)
''')

# Fetch a link from the DB and follow the link
cur.execute('SELECT html FROM Urls')
# url = list()
for row in cur:
    html = str(row[0])
    soup = BeautifulSoup(html, "html.parser")

    # use relative xPath to find listing number.
    element = soup.find(
        'div', class_='row p24_propertyOverviewRow').find('div', 
               class_='col-6 noPadding').find('div', 
               class_='p24_info')
    list_number = element.text
cur.execute('''INSERT OR IGNORE INTO Properties (list_number)
                            VALUES ( ? )''', ( list_number, ) )
conn.commit()
print(list_number)