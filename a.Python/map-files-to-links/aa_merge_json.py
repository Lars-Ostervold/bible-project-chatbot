'''
Merges all the json files in this folder into one json.
The output json will be the master map file for the chatbot.

Also deletes specified keywords from the json files before merging them.
'''

import os
import json


# Specify the folder path
folder_path = '.'

# Specify the keywords to delete
keywords_to_delete = ['Study Notes', 'Script References', '  ']

# Initialize an empty dictionary to store the merged JSON data
merged_data = {}

# Iterate over all the files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.json'):
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'r') as file:
            data = json.load(file)
            # Iterate over the items in the dictionary
            for key, value_list in data.items():
                # Iterate over the strings in the value list
                for i in range(len(value_list)):
                    # Replace the keywords in the string
                    for keyword in keywords_to_delete:
                        value_list[i] = value_list[i].replace(keyword, '')
            # Merge the JSON data into the merged_data dictionary
            merged_data.update(data)

# Write the merged JSON data to a file
output_file = os.path.join(folder_path, 'aaa_all_link_maps.json')
with open(output_file, 'w') as file:
    json.dump(merged_data, file)

print('Merged JSON file created:', output_file)