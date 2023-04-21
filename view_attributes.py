import json

# Open the JSON file for reading
with open('all_properties.json', 'r') as f:
    # Load the JSON data from the file
    all_properties = json.load(f)

attribute_list = []
for key in all_properties.values():
    for attribute in key:       
        if attribute not in attribute_list:
            attribute_list.append(attribute)
            print(attribute)
