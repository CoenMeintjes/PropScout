#!/usr/bin/env python

# This program is for extracting the relevant property information and storing it in the property analysis database which can then be used for analysis.

import sqlite3
from bs4 import BeautifulSoup
import json

conn = sqlite3.connect('parsed_links.sqlite')
cur = conn.cursor()

all_properties = {}
# input how many listing to process
many = 0
while True:
    if ( many < 1 ) :
        sval = input('How many pages:')
        if ( len(sval) < 1 ) : break
        many = int(sval)
    many = many - 1

    # Fetch html from the DB parse and extract values
    cur.execute('SELECT id,html FROM Urls WHERE parsed is NULL ORDER BY RANDOM() LIMIT 1')
    
    # iterate through the rows and extract data
    for row in cur:
        id = row[0]
        html = str(row[1])
        soup = BeautifulSoup(html, "html.parser")

        # parse relevant property information located in property overview table with class='row p24_propertyOverviewRow'     
        # Find all div elements with class "row p24_propertyOverviewRow"
        table_rows = soup.find_all('div', class_='row p24_propertyOverviewRow') # this creates a list from each row of the table

        property_specs = {}
        # Iterate through the list of rows
        for row in table_rows:
            # Find the div tag with class "p24_propertyOverviewKey" inside the row
            key_div = row.find('div', class_='p24_propertyOverviewKey')

            if key_div:
                # Extract the text inside the key_div
                key_text = key_div.text.strip()
                # print('Key:', key_text)
            else:
                print('Key not found.')
            
            # Find the div tag with class "p24_propertyOverviewKey" inside the row
            val_div = row.find('div', class_='p24_info')
            
            if val_div == None:
                continue
            elif val_div: # Extract the text inside the val_div
                val_text = val_div.text.strip()
                # print('Value:', val_text)
            else:
                print('Value not found.')
            property_specs[key_text] = val_text

            # Get the 'Listing Number' from property_specs
            property_id = property_specs.get('Listing Number')

            # If property_id is not in all_properties, create an empty list
            if property_id not in all_properties:
                all_properties[property_id] = property_specs

        # store the property specs in SQLite DB in json format
        cur.execute('''UPDATE Urls SET json = ?, parsed = ? WHERE id = ? ''', ( str(property_specs), 1, id, ))
        conn.commit()   

# print(property_specs)   # Print the final property_specs dictionary after the loop
print(json.dumps(all_properties, indent=4))  # Print the final all_properties dictionary after the loop

# Save the all_properties dictionary as a JSON file
with open('all_properties.json', 'w') as json_file:
    json.dump(all_properties, json_file)