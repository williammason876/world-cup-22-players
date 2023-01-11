# world-cup-22-players
All rostered players from the 2022 FIFA World Cup mapped to their city of birth

# data generation 1
To generate data run the data_collection.py script which will go to wikipedia.org and click through
all of the world cup 22 squads' players. Generate a list of player json to players.json in the following format

{"position": "GK", "name": "Hern\u00e1n Gal\u00edndez", "dob_string": " (1987-03-30)30 March 1987 (aged 35)", "club": "Aucas", "wiki_page": "https://en.wikipedia.org//wiki/Hern%C3%A1n_Gal%C3%ADndez", "birthplace": "Rosario, Argentina", "country": "Ecuador"}

# get lat lng
You will require a free api key from https://openweathermap.org and place it in the env.sh file:
export api_key=${api_key}

# run
source.env && python3 openweathersearch.py

This will generate the needed lat lngs for players home towns in hometowns.json