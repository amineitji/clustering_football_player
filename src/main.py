import argparse
from data_extractor import DataExtractor
from data_visualizer import DataVisualizer

def main():
    # Définir les groupes de positions
    position_groups = {
        '1. Milieu': ['DM', 'CM', 'AM'],
        '2. Attaquant axial': ['CF', 'SS', 'MO'],
        '3. Ailier': ['LW', 'RW', 'RM', 'LM'],
        '4. Défenseur': ['CB'],
        '5. Latéral': ['RB', 'LB'],
    }

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

    # Fonction utilitaire pour obtenir les positions en fonction du numéro du groupe
    def get_positions_by_choice(choice):
        group_key = f"{choice}. "  # Préfixe pour récupérer le bon groupe dans le dictionnaire
        for key in position_groups.keys():
            if key.startswith(group_key):
                return position_groups[key]
        return None

    if choice == '1':
        team_name = input("Entrez le nom de l'équipe : ")
        player_data = data_extractor.get_players_by_team(team_name)

        if player_data.empty:
            print(f"Aucun joueur trouvé pour l'équipe {team_name}.")
            return

        offensive_features = ['Passes progressives']
        defensive_features = ['Possessions progressives']
        
        filtered_features = player_data[offensive_features + defensive_features].dropna()
        visualizer = DataVisualizer(filtered_features, player_data, color1="#000000", color2="#3b3700")
        visualizer.plot_players_by_team(team_name)

    elif choice == '6':
        print("Choisissez un poste :")
        for key in position_groups:
            print(key)
        
        position_choice = input("Entrez le numéro du poste : ")
        positions = get_positions_by_choice(position_choice)

        if not positions:
            print("Poste invalide.")
            return

        team_names_input = input("Entrez les noms des équipes séparés par des virgules (laisser vide pour toutes les équipes) : ")
        team_names = [name.strip() for name in team_names_input.split(',')] if team_names_input else None
    
        player_data = data_extractor.get_players_by_multiple_criteria(player_names=None, positions=positions, team_names=team_names, ages=None)
    
        if player_data.empty:
            print(f"Aucun joueur trouvé pour le poste choisi avec les équipes spécifiées.")
            return
    
        offensive_features = ['Passes progressives']
        defensive_features = ['Possessions progressives']
        
        filtered_features = player_data[offensive_features + defensive_features].dropna()
        visualizer = DataVisualizer(filtered_features, player_data, color1="#000000", color2="#3b3700")
        visualizer.plot_players_by_position(position_choice, team_names=team_names)

    elif choice == '2':
        player_name = input("Entrez le nom du joueur : ")
        print("Choisissez un groupe de poste :")
        for key in position_groups:
            print(key)

        position_choice = input("Entrez le numéro du poste : ")
        positions = get_positions_by_choice(position_choice)

        if not positions:
            print("Poste invalide.")
            return

        if '1' in position_choice: # '1. Milieu': ['DM', 'CM', 'AM']
            offensive_features = [
                'Passes décisives', 'xAG: Prévu(s) Buts assistés', 'npxG + xAG', 'Actions menant à un tir', 
                'Passes progressives', 'Possessions progressives'
            ]
            defensive_features = ['Tacles', 'Interceptions']

        elif '2' in position_choice: # '2. Attaquant axial': ['CF', 'SS', 'MO']
            offensive_features = [
                'Buts (sans les pénaltys)', 'npxG: xG sans les pénaltys', 'Passes décisives', 
                'xAG: Prévu(s) Buts assistés', 'npxG + xAG', 'Actions menant à un tir', 
                'Total des tirs', 'Passes progressives reçues', 'Touches (SurfRépOff)'
            ]
            defensive_features = ['Tacles', 'Interceptions']

        elif '3' in position_choice: # '3. Ailier': ['LW', 'RW', 'RM', 'LM']
            offensive_features = [
                'Buts (sans les pénaltys)', 'npxG: xG sans les pénaltys', 'Passes décisives', 
                'xAG: Prévu(s) Buts assistés', 'npxG + xAG', 'Actions menant à un tir', 
                'Total des tirs', 'Possessions progressives', 'Dribbles réussis',
                'Passes progressives reçues', 'Touches (SurfRépOff)'
            ]
            defensive_features = ['Tacles', 'Interceptions']

        elif '4' in position_choice: # '4. Défenseur': ['CB']
            offensive_features = ['Passes progressives', 'Possessions progressives']
            defensive_features = ['Tacles', 'Interceptions', 'Balles contrées', 'Dégagements', 'Duel aérien gagnés']

        elif '5' in position_choice: #  '5. Latéral': ['RB', 'LB']
            offensive_features = ['Passes progressives', 'Possessions progressives', 'Dribbles réussis', 
                                  'Actions menant à un tir', 'Total des tirs']
            defensive_features = ['Tacles', 'Interceptions', 'Balles contrées', 'Dégagements', 'Duel aérien gagnés']
        else:
            print("Poste invalide.")
            return

        visualizer = DataVisualizer(offensive_features, defensive_features, color1="#000000", color2="#3b3700")
        visualizer.clustering_player_comparison(player_name, data_extractor.data, offensive_features, defensive_features)
        

    elif choice == '3':
        player_names_input = input("Entrez les noms des joueurs séparés par des virgules (le premier sera le joueur de référence) : ")
        player_names = [name.strip() for name in player_names_input.split(',')]

        if len(player_names) < 2:
            print("Veuillez entrer au moins deux joueurs pour comparer.")
            return

        print("Choisissez un groupe de poste :")
        for key in position_groups:
            print(key)

        position_choice = input("Entrez le numéro du poste : ")
        positions = get_positions_by_choice(position_choice)

        if not positions:
            print("Poste invalide.")
            return

        if '1' in position_choice: # '1. Milieu': ['DM', 'CM', 'AM']
            offensive_features = [
                'Passes décisives', 'xAG: Prévu(s) Buts assistés', 'npxG + xAG', 'Actions menant à un tir', 
                'Passes progressives', 'Possessions progressives'
            ]
            defensive_features = ['Tacles', 'Interceptions']

        elif '2' in position_choice: # '2. Attaquant axial': ['CF', 'SS', 'MO']
            offensive_features = [
                'Buts (sans les pénaltys)', 'npxG: xG sans les pénaltys', 'Passes décisives', 
                'xAG: Prévu(s) Buts assistés', 'npxG + xAG', 'Actions menant à un tir', 
                'Total des tirs', 'Passes progressives reçues', 'Touches (SurfRépOff)'
            ]
            defensive_features = ['Tacles', 'Interceptions']

        elif '3' in position_choice: # '3. Ailier': ['LW', 'RW', 'RM', 'LM']
            offensive_features = [
                'Buts (sans les pénaltys)', 'npxG: xG sans les pénaltys', 'Passes décisives', 
                'xAG: Prévu(s) Buts assistés', 'npxG + xAG', 'Actions menant à un tir', 
                'Total des tirs', 'Possessions progressives', 'Dribbles réussis',
                'Passes progressives reçues', 'Touches (SurfRépOff)'
            ]
            defensive_features = ['Tacles', 'Interceptions']

        elif '4' in position_choice: # '4. Défenseur': ['CB']
            offensive_features = ['Passes progressives']
            defensive_features = ['Tacles', 'Interceptions', 'Balles contrées', 'Dégagements', 'Duel aérien gagnés']

        elif '5' in position_choice: #  '5. Latéral': ['RB', 'LB']
            offensive_features = ['Passes progressives', 'Possessions progressives', 'Dribbles réussis', 
                                  'Actions menant à un tir', 'Total des tirs']
            defensive_features = ['Tacles', 'Interceptions', 'Balles contrées', 'Dégagements', 'Duel aérien gagnés']
        else:
            print("Poste invalide.")
            return
        
        visualizer = DataVisualizer(offensive_features, defensive_features, color1="#000000", color2="#3b3700")
        visualizer.clustering_multiple_players_comparison_with_reference(player_names, data_extractor.data, offensive_features, defensive_features)

    elif choice == '4':
        player_names_input = input("Entrez les noms des joueurs séparés par des virgules : ")
        player_names = [name.strip() for name in player_names_input.split(',')]

        if len(player_names) < 2:
            print("Veuillez entrer au moins deux joueurs pour comparer.")
            return

        offensive_features = [
            'Buts (sans les pénaltys)', 'npxG: xG sans les pénaltys', 'Passes décisives', 
            'xAG: Prévu(s) Buts assistés', 'npxG + xAG', 'Actions menant à un tir', 
            'Total des tirs', 'Possessions progressives', 'Dribbles réussis',
            'Passes progressives reçues', 'Touches (SurfRépOff)'
        ]
        defensive_features = ['Tacles', 'Interceptions']

        visualizer = DataVisualizer(offensive_features, defensive_features, color1="#000000", color2="#3b3700")
        visualizer.clustering_players_pca_comparison(player_names, data_extractor.data, offensive_features, defensive_features)

    elif choice == '5':
        team1_name = input("Entrez le nom de la première équipe : ")
        team2_name = input("Entrez le nom de la deuxième équipe : ")

        tentatives = ['npxG: xG sans les pénaltys']
        reussites = ['Buts (sans les pénaltys)']
        
        filtered_features = data_extractor.data[tentatives + reussites].dropna()
        visualizer = DataVisualizer(filtered_features, data_extractor.data, color1="#000000", color2="#3b3700")
        visualizer.compare_teams(team1_name, team2_name)

    else:
        print("Option invalide. Veuillez entrer 1, 2, 3, 4, 5 ou 6.")

if __name__ == "__main__":
    main()
