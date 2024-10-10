from data_extractor import DataExtractor
from data_visualizer import DataVisualizer

def main():
    file_path = 'data/cleaned_scouting_report.csv'
    
    # Initialiser les classes
    data_extractor = DataExtractor(file_path)
    
    # Exemple de liste de joueurs à afficher
    #player_names = [
    #    "Willian Pacho", "Achraf Hakimi", "João Neves", "Warren Zaïre-Emery", 
    #    "Bradley Barcola", "Marquinhos", "Lucas Beraldo", 
    #    "Ousmane Dembélé", "Lee Kang-in", "Vitinha", "Marco Asensio", 
    #    "Fabián Ruiz Peña", "Nuno Mendes", "Randal Kolo Muani", 
    #    "Désiré Doué", "Milan Škriniar", "Ibrahim Mbaye", "Yoram Zague", 
    #    "Gonçalo Ramos", "Senny Mayulu", "Naoufel El Hannach", "Carlos Soler", 
    #]

    #player_names = [
    #    "Gerónimo Rulli", "Michael Amir Murillo", "Pierre Højbjerg", "Mason Greenwood", "Luis Henrique", 
    #    "Geoffrey Kondogbia", "Amine Harit", "Lilian Brassier", "Derek Cornelius", "Elye Wahi", 
    #    "Leonardo Balerdi", "Quentin Merlin", "Neal Maupay", "Ismaël Koné", "Valentin Rongier", 
    #    "Pol Lirola", "Ulisses Garcia", "Valentin Carboni", "Jon Rowe", "Adrien Rabiot", 
    #    "Bamo Meïté", "Enzo Sternal", "Faris Pemi Moumbagna", "Keyliane Abdallah", 
    #    "Darryl Bakola", "Salim Ben Seghir", "Jeffrey De Lange", "Emmanuel Koum Mbondo", 
    #    "Gael Lafont", "Roggerio Nyakossi", "Adrien Rabiot"
    #]

    player_names = [
        "Lucas Perri", "Duje Ćaleta-Car", "Clinton Mata", "Ainsley Maitland-Niles",
        "Alexandre Lacazette", "Maxence Caqueret", "Corentin Tolisso", "Moussa Niakhate",
        "Abner", "Nemanja Matić", "Malick Fofana", "Saïd Benrahma", "Georges Mikautadze",
        "Nicolás Tagliafico", "Jordan Veretout", "Rayan Cherki", "Ernest Nuamah", 
        "Gift Orban", "Tanner Tessmann", "Sael Kumbedi", "Wilfried Zaha", 
        "Orel Mangala", "Mahamadou Diawara", "Mama Samba Baldé", "Adryelson", 
        "Warmed Omari", "Rémy Descamps", "Anthony Lopes", "Enzo Molebe", "Justin João"
    ]


    
    # Obtenir les données pour la liste de joueurs sans filtrer par position
    player_data = data_extractor.get_players_from_list(player_names)
    
    # Caractéristiques offensives et défensives
    offensive_features = ['Passes progressives']
    defensive_features = ['Possessions progressives']
    
    # Pas besoin de PCA : nous allons juste utiliser ces caractéristiques directement
    filtered_features = player_data[offensive_features + defensive_features].dropna()
    
    # Initialiser le visualiseur
    visualizer = DataVisualizer(filtered_features, player_data, color1="#000000", color2="#3b3700")
    
    # Afficher les joueurs de la liste
    visualizer.plot_players_from_list(player_names)


if __name__ == "__main__":
    main()
