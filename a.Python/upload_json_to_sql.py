import os
import json
from supabase import create_client, Client

# Load the JSON file
with open('C:\\Users\\Oster\\Projects\\bible-project-chatbot\\aaa_all_link_maps.json', 'r') as f:
    data = json.load(f)

# Create a Supabase client
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# Iterate over the data and send it to Supabase
for file_name, info in data.items():
    link, title = info
    payload = {
        'file_name': file_name,
        'link': link,
        'title': title,
    }
    supabase.table('source-links').insert(payload).execute()