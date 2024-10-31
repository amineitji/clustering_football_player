import pandas as pd
from sklearn.preprocessing import StandardScaler

class DataExtractor:
    def __init__(self, file_path):
        self.data = pd.read_csv(file_path)


    # Récupérer les joueurs par nom exact
    def get_players_by_name(self, player_names):
        """Obtenir les joueurs par nom (unique ou multiple)."""
        if isinstance(player_names, list):
            return self.data[self.data['player_name'].isin(player_names)]
        else:
            return self.data[self.data['player_name'] == player_names]

    # Récupérer les joueurs par position (simple ou multiple)
    def get_players_by_position(self, positions):
        """Obtenir les joueurs en fonction d'une ou plusieurs positions."""
        if isinstance(positions, list):
            position_filter = '|'.join(positions)
            return self.data[self.data['Position'].str.contains(position_filter, na=False)]
        else:
            return self.data[self.data['Position'] == positions]

    # Récupérer les joueurs par équipe (simple ou multiple)
    def get_players_by_team(self, team_names):
        """Obtenir les joueurs par équipe (unique ou multiple)."""
        if isinstance(team_names, list):
            return self.data[self.data['Team Name'].isin(team_names)]
        else:
            return self.data[self.data['Team Name'] == team_names]

    # Récupérer les joueurs par âge (simple ou multiple)
    def get_players_by_age(self, ages):
        """Obtenir les joueurs par âge (unique ou multiple)."""
        if isinstance(ages, list):
            return self.data[self.data['Age'].isin(ages)]
        else:
            return self.data[self.data['Age'] == ages]

    # Récupérer les joueurs par nom et équipe
    def get_players_by_name_and_team(self, player_names, team_names):
        """Obtenir les joueurs en fonction du nom et de l'équipe."""
        if isinstance(player_names, list):
            name_filter = self.data['player_name'].isin(player_names)
        else:
            name_filter = self.data['player_name'] == player_names

        if isinstance(team_names, list):
            team_filter = self.data['Team Name'].isin(team_names)
        else:
            team_filter = self.data['Team Name'] == team_names

        return self.data[name_filter & team_filter]

    # Récupérer les joueurs par position et âge
    def get_players_by_position_and_age(self, positions, ages):
        """Obtenir les joueurs en fonction de la position et de l'âge."""
        if isinstance(positions, list):
            position_filter = '|'.join(positions)
            position_data = self.data['Position'].str.contains(position_filter, na=False)
        else:
            position_data = self.data['Position'] == positions

        if isinstance(ages, list):
            age_filter = self.data['Age'].isin(ages)
        else:
            age_filter = self.data['Age'] == ages

        return self.data[position_data & age_filter]

    # Récupérer les joueurs par équipe et position
    def get_players_by_team_and_position(self, team_names, positions):
        """Obtenir les joueurs en fonction de l'équipe et de la position."""
        if isinstance(team_names, list):
            team_filter = self.data['Team Name'].isin(team_names)
        else:
            team_filter = self.data['Team Name'] == team_names

        if isinstance(positions, list):
            position_filter = '|'.join(positions)
            position_data = self.data['Position'].str.contains(position_filter, na=False)
        else:
            position_data = self.data['Position'] == positions

        return self.data[team_filter & position_data]

    # Récupérer les joueurs par nom, position, équipe et âge
    def get_players_by_multiple_criteria(self, player_names=None, positions=None, team_names=None, ages=None):
        """Obtenir les joueurs en fonction de plusieurs critères."""
        filtered_data = self.data
        
        if player_names:
            if isinstance(player_names, list):
                filtered_data = filtered_data[filtered_data['player_name'].isin(player_names)]
            else:
                filtered_data = filtered_data[filtered_data['player_name'] == player_names]

        if positions:
            if isinstance(positions, list):
                position_filter = '|'.join(positions)
                filtered_data = filtered_data[filtered_data['Position'].str.contains(position_filter, na=False)]
            else:
                filtered_data = filtered_data[filtered_data['Position'] == positions]

        if team_names:
            if isinstance(team_names, list):
                filtered_data = filtered_data[filtered_data['Team Name'].isin(team_names)]
            else:
                filtered_data = filtered_data[filtered_data['Team Name'] == team_names]

        if ages:
            if isinstance(ages, list):
                filtered_data = filtered_data[filtered_data['Age'].isin(ages)]
            else:
                filtered_data = filtered_data[filtered_data['Age'] == ages]

        return filtered_data

    def filter_features(self, player_data, offensive_features, defensive_features):
        """Filtrer les caractéristiques offensives et défensives spécifiées."""
        all_features = offensive_features + defensive_features
        return player_data[all_features].dropna()

    def scale_features(self, features):
        """Standardiser les caractéristiques."""
        scaler = StandardScaler()
        return scaler.fit_transform(features)
