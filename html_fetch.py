#!/usr/bin/env python

# for this program will be fetching a link from SQLite DB and then parsing the html from that page into the database
# this could probably be merged into the initial gmail_parse but will keep it seperate for now

import sqlite3
from bs4 import BeautifulSoup
import ssl
from urllib.parse import urljoin
from urllib.parse import urlparse
from urllib.request import urlopen

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

conn = sqlite3.connect('parsed_link.sqlite')
cur = conn.cursor()

# Steps

# Fetch a link from the DB and follow the link

# Use beautiful soup to parse the html of interest into the db

# Once in the data base need to extract the relevant information into some kind of format that can be parsed with pandas as a df but this could be a seperate program again.