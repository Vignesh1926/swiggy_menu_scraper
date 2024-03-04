import requests
import pandas as pd
import sys

def fetch_menu_data(restaurant_id):
    url = f"https://www.swiggy.com/dapi/menu/pl?page-type=REGULAR_MENU&complete-menu=true&lat=18.56&lng=73.95&restaurantId={restaurant_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data from Swiggy API. Status Code: {response.status_code}")
        print(f"Error message:{response.text}")
        return None

def extract_menu_data(menu_json):
    menu_items = []
    for category in menu_json['categories']:
        for item in category['items']:
            menu_item = {
                'Name': item['dishname'],
                'Price': item['price'],
                'Description': item['description'],
                'Category': category['name']
            }
            menu_items.append(menu_item)
    return menu_items

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <restaurant_id>")
        return
    
    restaurant_id = sys.argv[1]
    menu_json = fetch_menu_data(restaurant_id)
    if menu_json:
        menu_items = extract_menu_data(menu_json)
        if menu_items:
            df = pd.DataFrame(menu_items)
            df.to_csv('menu_data.csv', index=False)
            print("Menu data saved to menu_data.csv")
        else:
            print("No menu data found")
    else:
        print("Exiting...")

if  __name__== "__main__":
    main()