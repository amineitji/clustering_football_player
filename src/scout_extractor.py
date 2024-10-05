import requests
from bs4 import BeautifulSoup
import string
import re
import json

class ScoutDatabaseExtractor:
    def __init__(self):
        self.base_url = "https://fbref.com"
        self.players = []

    def generate_urls(self):
        # Générer toutes les URLs de la forme https://fbref.com/en/players/aa, ab, ac, ..., zz
        urls = []
        for first_letter in string.ascii_lowercase:
            for second_letter in string.ascii_lowercase:
                url = f"{self.base_url}/en/players/{first_letter}{second_letter}/"
                urls.append(url)
        return urls

    def page_extractor(self, url):
        try:
            # Send a GET request to the URL
            response = requests.get(url)
            # Check if the request was successful
            if response.status_code == 200:
                # Parse the HTML content with BeautifulSoup
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Find the div element with id that starts with "div_" but ignore the numbers
                div_regex = re.compile(r'^div_\d+')
                player_links_section = soup.find('div', {"class": "section_content"}, {"id": div_regex})
                
                if player_links_section:
                    # Find all <p> tags that contain the player information
                    player_entries = player_links_section.find_all('p')
                    
                    for player_entry in player_entries:
                        # Extract the player's name, position, and link
                        name_tag = player_entry.find('a')
                        #TODO : trouver les position
                        position_info = "___" #player_entry.text.split('·')[2].strip() if '·' in player_entry.text else None
                        
                        if name_tag and position_info:
                            player_name = name_tag.text.strip()
                            player_link = self.base_url + name_tag.get('href').strip() + "/"
                            player_position = position_info.split('·')[0]  # Example: 'FW'
                            
                            # Create a dictionary with player info
                            player_data = {
                                "name": player_name,
                                "position": player_position,
                                "link": player_link
                            }
                            
                            # Append the player data to the players list
                            #TODO : verifier si le joueur a un report scout avant de le rajouter à la db
                            self.players.append(player_data)
                else:
                    print(f"No player links found on page {url}")
            else:
                print(f"Failed to retrieve page at {url}, status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while requesting {url}: {e}")

    def extract_all_players(self):
        urls = self.generate_urls()
        for url in urls:
            self.page_extractor(url)
            print(f"Extracted players from {url}")

    def save_to_json(self, filename="data/db_players.json"):
        try:
            with open(filename, 'w') as json_file:
                json.dump(self.players, json_file, indent=4)
            print(f"Players data saved to {filename}")
        except IOError as e:
            print(f"Error saving to file {filename}: {e}")


# Example usage
extractor = ScoutDatabaseExtractor()
extractor.extract_all_players()  # Extract players from all URLs
extractor.save_to_json()  # Save the extracted players to a JSON file

# TODO : il faut passer le les erreurs 429