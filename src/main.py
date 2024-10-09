from data_extractor import DataExtractor
from data_visualizer import DataVisualizer

def main():
    file_path = 'data/cleaned_scouting_report.csv'
    
    # Initialiser les classes
    data_extractor = DataExtractor(file_path)
    
    # Sélectionner un joueur par son nom
    player_name = "Jack Grealish"
    selected_player = data_extractor.get_player_data(player_name)
    
    # Obtenir les positions et les joueurs correspondants
    position_players = data_extractor.get_position_data(player_name)
    
    # Caractéristiques offensives et défensives
    offensive_features = ['Passes progressives']
    defensive_features = ['Possessions progressives']
    
    # Filtrer les caractéristiques et standardiser les données
    filtered_features = data_extractor.filter_features(position_players, offensive_features, defensive_features)
    scaled_features = data_extractor.scale_features(filtered_features)
    
    # Visualisation des données
    visualizer = DataVisualizer(scaled_features, position_players)
    
    # Tracer les joueurs pour une position spécifique
    visualizer.plot_player(player_name, selected_player['Position'].values[0].split(','))
    
    # Comparaison entre plusieurs joueurs
    player_names = ["Jack Grealish", "Phil Foden", "Mason Mount"]
    visualizer.plot_comparison(player_names)

if __name__ == "__main__":
    main()
