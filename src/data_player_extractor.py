import os
import json
import requests
import csv
from bs4 import BeautifulSoup

class DataPlayerExtractor:
    def __init__(self, url):
        self.url = url
        self.soup = None

    def fetch_data(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            self.soup = BeautifulSoup(response.text, 'html.parser')
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"Other error occurred: {err}")

    def extract_player_name(self):
        if self.soup:
            player_name_tag = self.soup.find('h1')
            return player_name_tag.text.strip() if player_name_tag else "Nom non trouvé"
        return None

    def extract_scouting_report(self):
        if self.soup:
            table = self.soup.find('table')
            if not table:
                print("Table introuvable.")
                return
            
            headers = []
            rows_data = []
            
            # Extraction des en-têtes de tableau
            thead = table.find('thead')
            if thead:
                headers = [th.text.strip() for th in thead.find_all('th')]

            # Extraction des lignes du tableau
            tbody = table.find('tbody')
            if tbody:
                for row in tbody.find_all('tr'):
                    row_data = []
                    for cell in row.find_all(['th', 'td']):
                        row_data.append(cell.text.strip())
                    
                    # Ignorer les lignes vides
                    if any(row_data):
                        rows_data.append(row_data)
            
            return headers, rows_data
        return None

    def save_to_json(self, player_name, headers, rows_data, file_path='data/scouting_report.json'):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        data = {
            'player_name': player_name,
            'headers': headers,
            'stats': rows_data
        }
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"Données sauvegardées dans {file_path}")

    def save_to_csv(self, player_name, rows_data, file_path='data/scouting_report.csv'):
        # Colonnes à utiliser dans le CSV
        columns = ['player_name'] + [row[0] for row in rows_data]

        # Extraire uniquement les valeurs (sans le nom des statistiques)
        values = [player_name] + [row[1] for row in rows_data]

        # Vérifier si le fichier CSV existe déjà
        file_exists = os.path.isfile(file_path)

        # Créer le répertoire 'data' si nécessaire
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Ajouter les données au CSV
        with open(file_path, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if not file_exists:
                # Écrire les en-têtes si le fichier est créé pour la première fois
                writer.writerow(columns)
            # Écrire les données du joueur
            writer.writerow(values)
        
        print(f"Données sauvegardées dans {file_path}")
