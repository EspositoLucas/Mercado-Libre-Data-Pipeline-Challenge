import requests
import json
import datetime
from dotenv import load_dotenv
import os

DATE = str(datetime.date.today()).replace('-','')

def get_most_relevant_items_for_category(category):
    load_dotenv()
    
    url = f"https://api.mercadolibre.com/sites/MLA/search?category={category}" 
    BEARER_TOKEN = os.getenv('BEARER_TOKEN')
    
    if not BEARER_TOKEN:
        raise ValueError("BEARER_TOKEN not found in environment variables")
        
    headers = {'Authorization': f'Bearer {BEARER_TOKEN}'}
    response = requests.get(url, headers=headers).json()
    
    if "results" not in response:
        print(f"API Response: {json.dumps(response, indent=2)[:200]}")
        raise KeyError("'results' key not found in API response")
        
    data = response["results"]

    # Use path relative to Airflow's base directory
    file_path = os.path.join(os.getenv('AIRFLOW_HOME', '/opt/airflow'), 'plugins/tmp/file.tsv')
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    with open(file_path, 'w') as file:
        for item in data:
            _id = getKeyFromItem(item, 'id')
            site_id = getKeyFromItem(item, 'site_id')
            title = getKeyFromItem(item, 'title')
            price = getKeyFromItem(item, 'price')
            available_quantity = getKeyFromItem(item, 'available_quantity') 
            thumbnail = getKeyFromItem(item, 'thumbnail')
        
            print(f"{_id} {site_id} {title} {price} {available_quantity} {thumbnail}")
            file.write(f"{_id}\t{site_id}\t{title}\t{price}\t{available_quantity}\t{thumbnail}\t{DATE}\n")
        
def getKeyFromItem(item, key):
    return str(item[key]).replace('','').strip() if item.get(key) else "null"

def main():
    CATEGORY = "MLA1577"
    get_most_relevant_items_for_category(CATEGORY)

if __name__ == "__main__":
    main()