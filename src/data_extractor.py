import pandas as pd
from sklearn.preprocessing import StandardScaler

class DataExtractor:
    def __init__(self, file_path):
        self.data = pd.read_csv(file_path)

    def get_player_data(self, player_name):
        return self.data[self.data['player_name'] == player_name]

    def get_position_data(self, player_name):
        player = self.get_player_data(player_name)
        positions = player['Position'].values[0].split(',')
        if len(positions) > 1:
            position_filter = '|'.join(positions)
            return self.data[self.data['Position'].str.contains(position_filter, na=False)]
        else:
            return self.data[self.data['Position'] == positions[0]]

    def filter_features(self, position_data, offensive_features, defensive_features):
        all_features = offensive_features + defensive_features
        return position_data[all_features].dropna()

    def scale_features(self, features):
        scaler = StandardScaler()
        return scaler.fit_transform(features)

