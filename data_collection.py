from bs4 import BeautifulSoup
import requests

BASE_URL = 'https://en.wikipedia.org/'
wc_url = 'wiki/2022_FIFA_World_Cup_squads'
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
    player = {}
    player['position'] = player_table_string[3][1:3]
    player['name'] = player_table_string[5]
    player['dob_string'] = player_table_string[7]
    player['club'] = player_table_string[13].strip()
    print(player)

    player_page = links[1]['href']
    print(player_page)
    player['wiki_page'] = BASE_URL + player_page
    player_page_visit = requests.get(BASE_URL + player_page)
    player_page_parsed = BeautifulSoup(player_page_visit.content, 'html.parser')
    birth_place = player_page_parsed.find('td', class_='birthplace')
    print(birth_place.text)

    # parse and find player's birthplace
    player['birthplace'] = birth_place.text.replace('\n', '')
    # parse links and find country player plays for
    helpful_link_items = player_page_parsed.findAll('td', class_='infobox-data-a')
    player['country'] = helpful_link_items[len(helpful_link_items) -1 ].text.replace('\n', '')
    print('After nav', player)
    players.append(player)

import json
with open('players.json', 'w') as f:
    json.dump(players, f)
