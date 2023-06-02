#!/usr/bin/env python

''' This program is parsing html to a json formatted property specifications
dictionary which is saved back into the SQLite DB for later use in the property analysis model '''

import sqlite3
from bs4 import BeautifulSoup
import json
import os

conn = sqlite3.connect('property_analysis_db.sqlite')
cur = conn.cursor()

all_properties = {}
# input how many listings to process
# TODO improve this process as in some cases just want to process all so either 1-5 to check script or other option is all or 3rd option is break
many = 0
while True:
    if ( many < 1 ) :
        sval = input('Number of properties to process:')
        if ( len(sval) < 1 ) : break
        many = int(sval)
    many = many - 1

    # TODO add a try except to check if there are any unparsed rows and proceed accordingly (if all have been parsed then just print that and quit)
    # Fetch html from the DB parse and extract values
    cur.execute('SELECT id,html FROM Urls WHERE parsed is NULL ORDER BY RANDOM() LIMIT 1')
    # iterate through the rows in the DB and extract property specifications data
    for row in cur:
        id = row[0]
        html = str(row[1])
        soup = BeautifulSoup(html, "html.parser")

        # instantiate master dict()
        property_specs = {}

        # extract listing_type, suburb, city, province, listing_number from meta data
        meta_tag = soup.find('meta', {'property': 'al:ios:url'})
        if meta_tag:
            url = meta_tag['content'].split('/')
            listing_type = url[3]
            suburb = url[4]
            city = url[5]
            province = url[6]
            listing_number = url[8]
        else:
            print("Meta tag not found.")

        # write data to property_specs dict    
        property_specs= {'Listing Type': listing_type, 'Suburb': suburb, 'City': city,
                         'Province': province} 

        # extract purchase price
        price_text = None
        price_div = soup.find('span', class_="p24_price")
        if price_div:
            if price_text is None:    
                price_text = price_div.text.strip()
        else:
            print('Price not found')

        # write price to property_specs    
        property_specs['Price'] = price_text

        # extract purchase price
        blurb_text = None
        blurb_div = soup.find('span', class_="p24_title")
        if blurb_div:
            if blurb_text is None:   
                blurb_text = blurb_div.text.strip()
        else:
            print('Blurb not found')

        # write blurb to property_specs    
        property_specs['Blurb'] = blurb_text
        
        # Move on to extracting specs from the overview table
        # parse relevant property information located in property overview table with class='row p24_propertyOverviewRow'     
        table_rows = soup.find_all('div', class_='row p24_propertyOverviewRow') # this creates a list from each row of the table

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

            # Serialize json
            specs_json = json.dumps(property_specs)

            # If property_id is not in all_properties, create an empty list
            if property_id not in all_properties:
                all_properties[property_id] = property_specs  

        # store the property specs in SQLite DB in json format
        cur.execute('''UPDATE Urls SET json = ?, parsed = ? WHERE id = ? ''', ( str(specs_json), 1, id, ))
        conn.commit()

all_properties_json = json.dumps(all_properties, indent=4)

# print(property_specs)   # Print the final property_specs dictionary after the loop
print(all_properties_json)  # Print the final all_properties dictionary after the loop

# Write data to a json file
# Check if the file exists or not
if os.path.isfile('all_properties.json') and os.stat('all_properties.json').st_size != 0:
    # Read json file content
    with open('all_properties.json', 'r') as json_file:
        data = json.load(json_file)
else:
    # Create new file with first data if the file does not exist or is empty
    data = all_properties
    with open('all_properties.json', 'w') as json_file:
        json.dump(data, json_file)

# Update the existing json file
data.update(all_properties)

with open('all_properties.json', 'w') as json_file:
    json.dump(data, json_file)