import pandas as pd
from sklearn.preprocessing import StandardScaler

class DataExtractor:
    def __init__(self, file_path):
        self.data = pd.read_csv(file_path)

    def get_player_data(self, player_name):
        """Obtenir les données d'un seul joueur."""
        return self.data[self.data['player_name'] == player_name]

    def get_position_data(self, player_name):
        """Obtenir les joueurs qui jouent aux mêmes postes que le joueur spécifié."""
        player = self.get_player_data(player_name)
        positions = player['Position'].values[0].split(',')
        if len(positions) > 1:
            position_filter = '|'.join(positions)
            return self.data[self.data['Position'].str.contains(position_filter, na=False)]
        else:
            return self.data[self.data['Position'] == positions[0]]

    def get_players_by_team(self, team_name):
        return self.data[self.data['Team Name'] == team_name]
    
    def get_players_by_position(self, position):
        return self.data[self.data['Position'] == position]
    
    def get_players_by_position_and_team(self, position, team_names=None):
        # Filtrer par position et, si spécifié, par noms d'équipes
        if team_names:
            return self.data[(self.data['Position'] == position) & (self.data['Team Name'].isin(team_names))]
        else:
            return self.data[self.data['Position'] == position]
    

    def filter_features(self, player_data, offensive_features, defensive_features):
        """Filtrer les caractéristiques offensives et défensives spécifiées."""
        all_features = offensive_features + defensive_features
        return player_data[all_features].dropna()

    def scale_features(self, features):
        """Standardiser les caractéristiques."""
        scaler = StandardScaler()
        return scaler.fit_transform(features)
