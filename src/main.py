import argparse
from data_extractor import DataExtractor
from data_visualizer import DataVisualizer

def main():
    # Choisir la fonction à exécuter
    print("Choisissez une fonction à exécuter :")
    print("1. Visualiser les joueurs d'une équipe")
    print("2. Comparer un joueur avec les autres de son poste (clustering)")
    print("3. Comparer un joueur de référence avec plusieurs autres (clustering multiple)")
    print("4. Comparer plusieurs joueurs indépendamment des postes (PCA)")

    choice = input("Entrez le numéro de l'option (1, 2, 3 ou 4) : ")

    # Charger les données
    file_path = 'data/cleaned_scouting_report.csv'
    data_extractor = DataExtractor(file_path)

    if choice == '1':
        # Option 1 : Visualiser les joueurs d'une équipe
        team_name = input("Entrez le nom de l'équipe : ")
        player_data = data_extractor.get_players_by_team(team_name)

        if player_data.empty:
            print(f"Aucun joueur trouvé pour l'équipe {team_name}.")
            return

        # Caractéristiques offensives et défensives
        offensive_features = ['Passes progressives']
        defensive_features = ['Possessions progressives']
        
        # Filtrer les données
        filtered_features = player_data[offensive_features + defensive_features].dropna()

        # Initialiser le visualiseur et afficher
        visualizer = DataVisualizer(filtered_features, player_data, color1="#000000", color2="#3b3700")
        visualizer.plot_players_by_team(team_name)

    elif choice == '2':
        # Option 2 : Comparer un joueur avec les autres de son poste
        player_name = input("Entrez le nom du joueur : ")

        # Définir les caractéristiques à utiliser
        offensive_features = [
            'Buts (sans les pénaltys)', 'npxG: xG sans les pénaltys', 'Passes décisives', 
            'xAG: Prévu(s) Buts assistés', 'npxG + xAG', 'Actions menant à un tir', 
            'Total des tirs', 'Passes progressives', 'Possessions progressives', 'Dribbles réussis'
        ]
        defensive_features = [
            'Tacles', 'Interceptions', 'Balles contrées', 'Dégagements', 'Duel aérien gagnés'
        ]

        # Appeler la méthode de comparaison via clustering
        visualizer = DataVisualizer(offensive_features, defensive_features, color1="#000000", color2="#3b3700")
        visualizer.clustering_player_comparison(player_name, data_extractor.data, offensive_features, defensive_features)

    elif choice == '3':
        # Option 3 : Comparer un joueur de référence avec plusieurs autres
        player_names_input = input("Entrez les noms des joueurs séparés par des virgules (le premier sera le joueur de référence) : ")

        # Transformer la chaîne de caractères en liste de joueurs
        player_names = [name.strip() for name in player_names_input.split(',')]

        # Vérifier qu'il y a au moins deux joueurs pour comparer
        if len(player_names) < 2:
            print("Veuillez entrer au moins deux joueurs pour comparer.")
            return

        # Définir les caractéristiques à utiliser
        offensive_features = [
            'Buts (sans les pénaltys)', 'npxG: xG sans les pénaltys', 'Passes décisives', 
            'xAG: Prévu(s) Buts assistés', 'npxG + xAG', 'Actions menant à un tir', 
            'Total des tirs', 'Passes progressives', 'Possessions progressives', 'Dribbles réussis'
        ]
        defensive_features = [
            'Tacles', 'Interceptions', 'Balles contrées', 'Dégagements', 'Duel aérien gagnés'
        ]

        # Appeler la méthode de comparaison multiple avec le premier joueur comme référence
        visualizer = DataVisualizer(offensive_features, defensive_features, color1="#000000", color2="#3b3700")
        visualizer.clustering_multiple_players_comparison_with_reference(player_names, data_extractor.data, offensive_features, defensive_features)

    elif choice == '4':
        # Option 4 : Comparer plusieurs joueurs avec PCA uniquement
        player_names_input = input("Entrez les noms des joueurs séparés par des virgules : ")

        # Transformer la chaîne de caractères en liste de joueurs
        player_names = [name.strip() for name in player_names_input.split(',')]

        # Vérifier qu'il y a au moins deux joueurs pour comparer
        if len(player_names) < 2:
            print("Veuillez entrer au moins deux joueurs pour comparer.")
            return

        # Définir les caractéristiques à utiliser
        offensive_features = [
            'Buts (sans les pénaltys)', 'npxG: xG sans les pénaltys', 'Passes décisives', 
            'xAG: Prévu(s) Buts assistés', 'npxG + xAG', 'Actions menant à un tir', 
            'Total des tirs', 'Passes progressives', 'Possessions progressives', 'Dribbles réussis'
        ]
        defensive_features = [
            'Tacles', 'Interceptions', 'Balles contrées', 'Dégagements', 'Duel aérien gagnés'
        ]

        # Appeler la nouvelle méthode de clustering avec PCA
        visualizer = DataVisualizer(offensive_features, defensive_features, color1="#000000", color2="#3b3700")
        visualizer.clustering_players_pca_comparison(player_names, data_extractor.data, offensive_features, defensive_features)

    else:
        print("Option invalide. Veuillez entrer 1, 2, 3 ou 4.")

if __name__ == "__main__":
    main()
