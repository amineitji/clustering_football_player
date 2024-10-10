from data_extractor import DataExtractor
from data_visualizer import DataVisualizer

def main():
    file_path = 'data/cleaned_scouting_report.csv'
    
    # Initialiser les classes
    data_extractor = DataExtractor(file_path)
    
    # Exemple de liste de joueurs à afficher
    team_name = "Lyon"

    # Obtenir les données pour la liste de joueurs sans filtrer par position
    player_data = data_extractor.get_players_by_team(team_name)
    
    # Caractéristiques offensives et défensives
    offensive_features = ['Passes progressives']
    defensive_features = ['Possessions progressives']
    
    # Pas besoin de PCA : nous allons juste utiliser ces caractéristiques directement
    filtered_features = player_data[offensive_features + defensive_features].dropna()
    
    # Initialiser le visualiseur
    visualizer = DataVisualizer(filtered_features, player_data, color1="#000000", color2="#3b3700")
    
    # Afficher les joueurs de la liste
    visualizer.plot_players_by_team(team_name)


if __name__ == "__main__":
    main()
