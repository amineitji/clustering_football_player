from data_extractor import DataExtractor

def main():
    # URL de la page de Toni Kroos sur FBref
    url = "https://fbref.com/fr/joueurs/6ce1f46f/Toni-Kroos"
    
    # Créer une instance de DataExtractor avec l'URL
    extractor = DataExtractor(url)

    # Récupérer les données de la page
    extractor.fetch_data()

    # Extraire le nom du joueur
    player_name = extractor.extract_player_name()
    print(f"Nom du joueur: {player_name}")

    # Extraire les statistiques du rapport de scouting
    scouting_report = extractor.extract_scouting_report()

    # Si les données ont été extraites, les sauvegarder dans un fichier JSON et CSV
    if scouting_report:
        headers, rows_data = scouting_report
        print("En-têtes:", headers)
        for row in rows_data:
            print("Ligne:", row)
        
        # Sauvegarder dans un fichier JSON
        extractor.save_to_json(player_name, headers, rows_data, 'data/scouting_report.json')

        # Sauvegarder dans un fichier CSV
        extractor.save_to_csv(player_name, rows_data, 'data/scouting_report.csv')

if __name__ == "__main__":
    main()
