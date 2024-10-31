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
    print("5. Comparer deux équipes")
    print("6. Visualiser les joueurs par poste")

    choice = input("Entrez le numéro de l'option (1, 2, 3, 4, 5 ou 6) : ")

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

    elif choice == '6':
        # Option 6 : Visualiser les joueurs par poste avec un filtre d'équipes
        position = input("Entrez le poste des joueurs (ex : Attaquant, Milieu, Défenseur) : ")
        team_names_input = input("Entrez les noms des équipes séparés par des virgules (laisser vide pour toutes les équipes) : ")
    
        # Transformer la chaîne de caractères en liste d'équipes, si non vide
        team_names = [name.strip() for name in team_names_input.split(',')] if team_names_input else None
    
        # Extraire les données des joueurs par poste et équipes spécifiées
        player_data = data_extractor.get_players_by_position_and_team(position, team_names)
    
        if player_data.empty:
            print(f"Aucun joueur trouvé pour le poste {position} avec les équipes spécifiées.")
            return
    
        # Caractéristiques offensives et défensives
        offensive_features = ['Passes progressives']
        defensive_features = ['Possessions progressives']
        
        # Filtrer les données pour les caractéristiques choisies
        filtered_features = player_data[offensive_features + defensive_features].dropna()
    
        # Initialiser le visualiseur et afficher avec le filtre d'équipes
        visualizer = DataVisualizer(filtered_features, player_data, color1="#000000", color2="#3b3700")
        visualizer.plot_players_by_position(position, team_names=team_names)
    

    elif choice == '2':
        # Define features based on position
        # TODO : FAIRE CE SYSTEME AUTOMATIQUEMENT POUR TOUTES FONCTIONS
        # Defender (DF) features
        offensive_features_DF = [
            'Passes progressives', 'Possessions progressives'
        ]
        defensive_features_DF = [
            'Tacles', 'Interceptions', 'Balles contrées', 'Dégagements', 'Duel aérien gagnés'
        ]

        # Midfielder (MF) features
        offensive_features_MF = [
            'Passes décisives', 'xAG: Prévu(s) Buts assistés', 'npxG + xAG', 'Actions menant à un tir', 
            'Passes progressives', 'Possessions progressives', 'Dribbles réussis', 'Passes progressives reçues',
            'Touches (SurfRépOff)'
        ]
        defensive_features_MF = [
            'Tacles', 'Interceptions', 'Duel aérien gagnés'
        ]

        # Forward (FW) features
        offensive_features_FW = [
            'Buts (sans les pénaltys)', 'npxG: xG sans les pénaltys', 'Passes décisives', 
            'xAG: Prévu(s) Buts assistés', 'npxG + xAG', 'Total des tirs', 'Dribbles réussis', 'Passes progressives reçues',
            'Touches (SurfRépOff)'
        ]
        defensive_features_FW = [
            'Interceptions', 'Balles contrées'  # Minimal defensive metrics for forwards
        ]

        # User input for player name and position
        player_name = input("Entrez le nom du joueur : ")
        player_position = input("Entrez le poste du joueur (DF, MF, FW) : ")

        # Select features based on player position
        if player_position == "DF":
            offensive_features = offensive_features_DF
            defensive_features = defensive_features_DF
        elif player_position == "MF":
            offensive_features = offensive_features_MF
            defensive_features = defensive_features_MF
        elif player_position == "FW":
            offensive_features = offensive_features_FW
            defensive_features = defensive_features_FW
        else:
            print("Poste invalide. Veuillez entrer DF, MF ou FW.")
            exit()

        # Call clustering comparison method with appropriate features
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

    elif choice == '5':
        # Option 5 : Comparer deux équipes
        team1_name = input("Entrez le nom de la première équipe : ")
        team2_name = input("Entrez le nom de la deuxième équipe : ")
    
        tentatives = [
            'npxG: xG sans les pénaltys', 
        ]

        reussites = [
            'Buts (sans les pénaltys)',
        ]
    
        # Initialiser le visualiseur avec les données appropriées
        filtered_features = data_extractor.data[tentatives + reussites].dropna()
    
        visualizer = DataVisualizer(filtered_features, data_extractor.data, color1="#000000", color2="#3b3700")
        visualizer.compare_teams(team1_name, team2_name)

    else:
        print("Option invalide. Veuillez entrer 1, 2, 3, 4, 5 ou 6.")

if __name__ == "__main__":
    main()
