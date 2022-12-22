import requests
import json
import os
import urllib
import logging
logging.basicConfig(filename="log.txt")

def lookup(location):
    try:
        request_url =  'http://api.openweathermap.org/geo/1.0/direct?q=' + location +'&limit=5&appid=' + os.environ.get('api_key')

        # print('lookup', location, request_url)

        api_call = requests.get(request_url)
        first_res = api_call.json()[0]
        map = {}
        print('found hometown, ', first_res )
        return {'lat': first_res['lat'], 'lon': first_res['lon']}
    except Exception as e:
        logging.error("Exception trying to find location=" + location)
        return None


def main():
    with open('players.json') as f:
        my_list = json.loads(f.read())
        home_towns = []
        for item in my_list:
            # print(item['birthplace'])
            home_towns.append(item['birthplace'])
        # print(set(home_towns))
        home_town_set = set(home_towns)
        # print(len(home_town_set))
        home_town_map = {}
        for home_town in home_town_set:
            val = lookup(home_town)
            if val is not None:
                home_town_map[home_town] = val
        import json
        with open('hometowns.json', 'w') as f:
            json.dump(home_town_map, f)

if __name__ == "__main__":
    main()