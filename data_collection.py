from bs4 import BeautifulSoup
import requests

def get_valid_year():
    while True:
        try:
            year = int(input("Enter a World Cup year (1930-2022, every 4 years, excluding 1942 and 1946): "))
            if year >= 1930 and year <= 2022 and (year - 1930) % 4 == 0 and year not in [1942, 1946]:
                return year
            else:
                print("Invalid year. Please enter a valid World Cup year.")
        except ValueError:
            print("Invalid input. Please enter a numeric year.")


# Prompt user for the World Cup year
wc_year = get_valid_year()

BASE_URL = 'https://en.wikipedia.org/'
wc_url = f'wiki/{wc_year}_FIFA_World_Cup_squads'
squads = requests.get(BASE_URL + wc_url)
soup = BeautifulSoup(squads.content, 'html.parser')
player_class = 'nat-fs-player'
results = soup.find_all('tr', class_=player_class)

results_temp = results[0:27]
players = []
# number, position, Name, DOB String, caps, goals, Club
for res in results:
    links = res.find_all('a')
    player_table_string = res.text.split('\n')
    print(len(player_table_string))
    print("\n")
    print(player_table_string)
    player = {}
    player['position'] = player_table_string[3][1:3]
    player['name'] = player_table_string[5]
    player['dob_string'] = player_table_string[7]
    # usually second to last item
    player['club'] = player_table_string[len(player_table_string) -2].strip()
    print(player)

    player_page = links[1]['href']
    print(player_page)
    player['wiki_page'] = BASE_URL + player_page
    player_page_visit = requests.get(BASE_URL + player_page)
    player_page_parsed = BeautifulSoup(player_page_visit.content, 'html.parser')
    birth_place = player_page_parsed.find('td', class_='birthplace')
    if birth_place is not None:
        print("raw birth place " + str(birth_place))

        # parse and find player's birthplace, may need to handle null values
        player['birthplace'] = birth_place.text.replace('\n', '')
    else:
        player['birthplace'] = None
    # parse links and find country player plays for
    helpful_link_items = player_page_parsed.findAll('td', class_='infobox-data-a')
    player['country'] = helpful_link_items[len(helpful_link_items) -1 ].text.replace('\n', '')
    print('After nav', player)
    players.append(player)

import json

with open(f'{wc_year}_players.json', 'w') as f:
    json.dump(players, f)
