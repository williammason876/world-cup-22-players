import requests
import json
import shutil
import os

def main():
    url = 'https://countryflagsapi.com/png/'
    with open('players.json', 'r') as f:
        my_list = json.loads(f.read())
        country_map = {}
        for item in my_list:
            if item['country'] not in country_map:
                country_map[item['country']] = True
                response = requests.get(url + item['country'], stream=True)
                
                flag_path = os.path.join(os.getcwd(), 'world-cup-players/src/assets/flags/')
                with open(flag_path + item['country'] +'.png', 'wb') as out_file:
                    shutil.copyfileobj(response.raw, out_file)
                    del response
                # country_map[item['country']] 

if __name__ == "__main__":
    main()