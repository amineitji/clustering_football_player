import requests
from bs4 import BeautifulSoup
import csv

# URL of the FBref page with the Big 5 European Leagues stats
url = 'https://fbref.com/en/comps/Big5/Big-5-European-Leagues-Stats'

# Send a GET request to fetch the page content
response = requests.get(url)

# Parse the page content using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')
print(soup)

# Find the table that contains team data
team_table = soup.find('table', {'id': 'big5_table'})

# Prepare a list to hold team names and URLs
teams_data = []

# Find all rows in the table body
for row in team_table.find('tbody').find_all('tr'):
    team_cell = row.find('td', {'data-stat': 'team'})
    if team_cell:
        team_name = team_cell.get_text(strip=True)
        team_link = 'https://fbref.com' + team_cell.find('a')['href']
        teams_data.append([team_name, team_link])

# Save the data to a CSV file
with open('data/teams_data.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Team Name', 'Team URL'])
    writer.writerows(teams_data)

print("Data saved to teams_data.csv")


class TeamScraper:
    def __init__(self, url):
        self.url = url

    def scrape_teams(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, 'html.parser')
        team_table = soup.find('table', {'id': 'big5_table'})
        teams_data = []

        for row in team_table.find('tbody').find_all('tr'):
            team_cell = row.find('td', {'data-stat': 'team'})
            if team_cell:
                team_name = team_cell.get_text(strip=True)
                team_link = 'https://fbref.com' + team_cell.find('a')['href']
                teams_data.append([team_name, team_link])

        # Save team data to CSV
        with open('teams_data.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Team Name', 'Team URL'])
            writer.writerows(teams_data)

        print("Teams data saved to teams_data.csv")