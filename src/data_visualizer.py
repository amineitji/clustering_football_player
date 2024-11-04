import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors
import os
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist
from matplotlib.gridspec import GridSpec
import pandas as pd

class DataVisualizer:
    def __init__(self, features, players_data, color1="#FFFFFF", color2="#D4CAE1"):
        self.features = features
        self.players_data = players_data
        self.color1 = color1  # Couleur du début du gradient
        self.color2 = color2  # Couleur de fin du gradient

    def create_gradient_background(self, fig):
        """Crée un fond en dégradé vertical pour l'ensemble de la figure."""
        # Créer un gradient vertical (de haut en bas)
        gradient = np.linspace(0, 1, 256).reshape(-1, 1)
        gradient = np.hstack((gradient, gradient))

        # Créer un colormap personnalisé à partir des couleurs hexadécimales
        cmap = mcolors.LinearSegmentedColormap.from_list("", [self.color1, self.color2])

        # Ajouter un axe qui occupe toute la figure
        ax = fig.add_axes([0, 0, 1, 1])

        # Désactiver les axes
        ax.axis('off')

        # Appliquer le gradient vertical avec les couleurs choisies
        ax.imshow(gradient, aspect='auto', cmap=cmap, extent=[0, 1, 0, 1], zorder=-1)

    def customize_axes(self, ax):
        """Personnalise les axes avec des contours blancs et épais."""
        for spine in ax.spines.values():
            spine.set_edgecolor('white')  # Couleur blanche
            spine.set_linewidth(2.5)  # Épaisseur du contour

    def plot_players_by_team(self, team_name, threshold_distance=1):
        """Affiche tous les joueurs d'une équipe donnée dans un graphique."""
        # Créer une figure avec des dimensions adaptées pour les appareils mobiles
        fig = plt.figure(figsize=(16, 9))  # Largeur 16, hauteur 9 pour un ajustement mobile

        # Créer le fond en dégradé pour l'ensemble de la figure
        self.create_gradient_background(fig)

        # Ajouter un axe pour le graphique principal, avec un fond transparent
        ax = fig.add_subplot(111, facecolor='none')  # Fond transparent

        # Extraire les colonnes pour les passes progressives (X) et les possessions progressives (Y)
        x_values = self.features['Passes progressives']
        y_values = self.features['Possessions progressives']

        # Filtrer les données pour ne garder que les joueurs de l'équipe donnée
        filtered_players = self.players_data[self.players_data['Team Name'] == team_name]

        if filtered_players.empty:
            print(f"Aucun joueur trouvé pour l'équipe {team_name}.")
            return

        # Tracer les joueurs de l'équipe filtrée
        scatter = ax.scatter(x_values, y_values, color='red', edgecolor='black', s=200, zorder=1)

        # Ajuster les limites de l'axe
        ax.set_xlim(np.floor(np.min(x_values)) - 1, np.ceil(np.max(x_values)) + 1)
        ax.set_ylim(np.floor(np.min(y_values)) - 1, np.ceil(np.max(y_values)) + 1)

        # Afficher les noms des joueurs de l'équipe
        displayed_names = []
        for i, row in filtered_players.iterrows():
            name = row['player_name']
            x, y = row['Passes progressives'], row['Possessions progressives']

            # Éviter la superposition des noms avec une condition moins stricte
            if not any(np.linalg.norm([x - dx, y - dy]) < (threshold_distance / 2) for dx, dy in displayed_names):
                ax.text(x + 0.2, y + 0.1, name, fontsize=12, ha='right', va='bottom', fontweight='bold', color='white', zorder=3)
                displayed_names.append((x, y))

        # Ajouter le titre en blanc et en gras
        ax.set_title(f'Projection des Passes et des Possessions progressives ({team_name})', fontsize=25, color='white', fontweight='bold')

        # Ajouter les labels des axes en blanc et en gras avec détails supplémentaires
        ax.set_xlabel('Passes progressives (par 90")', fontsize=16, color='white', fontweight='bold')
        ax.set_ylabel('Possessions progressives (par 90")', fontsize=16, color='white', fontweight='bold')

        # Ajouter l'étiquette Twitter
        ax.text(0.5, 0.75, f"@TarbouchData", fontsize=14, color='white', fontweight='bold', ha='left', transform=ax.transAxes, alpha=0.8)

        # Appliquer la personnalisation des axes (contours blancs et épais)
        self.customize_axes(ax)

        # Ajouter les ticks des axes (graduations) en blanc
        ax.tick_params(axis='x', colors='white', labelsize=14)  # Ticks en blanc et taille des labels réduite
        ax.tick_params(axis='y', colors='white', labelsize=14)

        # Appliquer les ticks pour montrer les valeurs de progression moyenne par match (seulement des entiers)
        ax.set_xticks(np.arange(np.floor(np.min(x_values)), np.ceil(np.max(x_values)) + 1, 1))
        ax.set_yticks(np.arange(np.floor(np.min(y_values)), np.ceil(np.max(y_values)) + 1, 1))

        # Sauvegarder le fichier et afficher le graphique
        plt.savefig(f"viz_data/projection_passes_possessions_{team_name}.jpeg", format='jpeg', dpi=300)
        plt.show()



    def plot_players_by_position(self, position_player, team_names=None, threshold_distance=1):
        """Affiche tous les joueurs d'un poste donné dans un graphique, avec un filtre d'équipes spécifié."""
        # Créer une figure avec des dimensions adaptées pour les appareils mobiles
        fig = plt.figure(figsize=(16, 9))  # Largeur 16, hauteur 9 pour un ajustement mobile

        # Créer le fond en dégradé pour l'ensemble de la figure
        self.create_gradient_background(fig)

        # Ajouter un axe pour le graphique principal, avec un fond transparent
        ax = fig.add_subplot(111, facecolor='none')  # Fond transparent

        # Extraire les colonnes pour les passes progressives (X) et les possessions progressives (Y)
        x_values = self.features['Passes progressives']
        y_values = self.features['Possessions progressives']

        # Filtrer les données pour ne garder que les joueurs du poste donné
        filtered_players = self.players_data[self.players_data['Position'] == position_player]

        # Appliquer un filtre sur les équipes, si `team_names` est spécifié
        if team_names is not None:
            filtered_players = filtered_players[filtered_players['Team Name'].isin(team_names)]

        if filtered_players.empty:
            print(f"Aucun joueur trouvé pour le poste {position_player} avec les équipes spécifiées.")
            return

        # Tracer les joueurs de l'équipe filtrée
        scatter = ax.scatter(x_values, y_values, color='red', edgecolor='black', s=200, zorder=1)

        # Ajuster les limites de l'axe
        ax.set_xlim(np.floor(np.min(x_values)) - 1, np.ceil(np.max(x_values)) + 1)
        ax.set_ylim(np.floor(np.min(y_values)) - 1, np.ceil(np.max(y_values)) + 1)

        # Afficher les noms des joueurs de l'équipe
        displayed_names = []
        for i, row in filtered_players.iterrows():
            name = row['player_name']
            x, y = row['Passes progressives'], row['Possessions progressives']

            # Éviter la superposition des noms avec une condition plus stricte pour x que pour y
            x_threshold = threshold_distance / 1.5 # Distance plus importante pour x
            y_threshold = threshold_distance / 3.25  # Distance moins stricte pour y

            if not any(
                np.abs(x - dx) < x_threshold and np.abs(y - dy) < y_threshold
                for dx, dy in displayed_names
            ):
                ax.text(x + 0.2, y + 0.1, name, fontsize=12, ha='right', va='bottom', fontweight='bold', color='white', zorder=3)
                displayed_names.append((x, y))


        # Ajouter le titre en blanc et en gras
        ax.set_title(f'Projection des Passes et des Possessions progressives - {position_player}', fontsize=25, color='white', fontweight='bold')

        # Ajouter les labels des axes en blanc et en gras
        ax.set_xlabel('Passes progressives (par 90")', fontsize=16, color='white', fontweight='bold')
        ax.set_ylabel('Possessions progressives (par 90")', fontsize=16, color='white', fontweight='bold')

        # Ajouter l'étiquette Twitter
        ax.text(0.5, 0.75, f"@TarbouchData", fontsize=14, color='white', fontweight='bold', ha='left', transform=ax.transAxes, alpha=0.8)

        # Personnaliser les axes avec des contours blancs et épais
        self.customize_axes(ax)

        # Ajouter les ticks des axes en blanc
        ax.tick_params(axis='x', colors='white', labelsize=14)
        ax.tick_params(axis='y', colors='white', labelsize=14)

        # Ajouter des ticks pour afficher les valeurs entières
        ax.set_xticks(np.arange(np.floor(np.min(x_values)), np.ceil(np.max(x_values)) + 1, 1))
        ax.set_yticks(np.arange(np.floor(np.min(y_values)), np.ceil(np.max(y_values)) + 1, 1))

        # Sauvegarder l'image et afficher le graphique
        plt.savefig(f"viz_data/projection_passes_possessions_{position_player}.jpeg", format='jpeg', dpi=300)
        plt.show()

    def clustering_player_comparison(self, player_name, data, offensive_features, defensive_features):
        """Effectuer un clustering et comparer un joueur avec ses pairs au même poste, avec 2 colonnes et fond en dégradé."""
        output_dir = 'viz_data/clustering'
        os.makedirs(output_dir, exist_ok=True)

        # Sélectionner un joueur par son nom
        selected_player = data[data['player_name'] == player_name]

        if selected_player.empty:
            print(f"Le joueur {player_name} n'a pas été trouvé.")
            return

        # Obtenir la position du joueur
        positions = selected_player['Position'].values[0].split(',')

        # Vérifier les positions et filtrer les joueurs
        if len(positions) > 1:
            position_filter = '|'.join(positions)
            position_players = data[data['Position'].str.contains(position_filter, na=False)]
        else:
            position_players = data[data['Position'] == positions[0]]

        # Filtrer les caractéristiques et standardiser
        position_players = position_players.dropna(subset=offensive_features + defensive_features)
        scaler_offensive = StandardScaler()
        scaler_defensive = StandardScaler()

        offensive_scaled = scaler_offensive.fit_transform(position_players[offensive_features])
        defensive_scaled = scaler_defensive.fit_transform(position_players[defensive_features])

        # PCA pour les variables offensives et défensives
        pca_offensive = PCA(n_components=1)
        offensive_component = pca_offensive.fit_transform(offensive_scaled)

        pca_defensive = PCA(n_components=1)
        defensive_component = pca_defensive.fit_transform(defensive_scaled)

        # Ajouter les composantes PCA au DataFrame
        position_players['PCA_Component_1'] = offensive_component.flatten()
        position_players['PCA_Component_2'] = defensive_component.flatten()

        # Clustering avec KMeans
        kmeans = KMeans(n_clusters=1)
        position_players['cluster'] = kmeans.fit_predict(np.column_stack([offensive_component, defensive_component]))

        # Calculer les distances par rapport au joueur sélectionné
        selected_player_pca = position_players[position_players['player_name'] == player_name][['PCA_Component_1', 'PCA_Component_2']].values
        distances = cdist(selected_player_pca, position_players[['PCA_Component_1', 'PCA_Component_2']].values, metric='euclidean').flatten()
        position_players['distance_to_selected'] = distances
        sorted_players = position_players.sort_values(by='distance_to_selected')

        # Créer une figure avec une répartition 80%-20% pour les colonnes
        fig = plt.figure(figsize=(16, 9))
        gs = GridSpec(1, 2, width_ratios=[3, 1], wspace=0.3)  # 80% pour le graphique, 20% pour le tableau

        # Créer le fond en dégradé pour l'ensemble de la figure
        self.create_gradient_background(fig)

        # Colonne de gauche : graphique des clusters (80%)
        ax1 = fig.add_subplot(gs[0], facecolor='none')  # Fond transparent

        # Afficher les clusters dans l'axe de gauche
        scatter = ax1.scatter(
            position_players['PCA_Component_1'], position_players['PCA_Component_2'], 
            c=position_players['cluster'], s=100, cmap='rainbow', edgecolor='black', linewidth=1.5, zorder=2
        )

        # Identifiez le cluster du joueur sélectionné
        selected_cluster = position_players[position_players['player_name'] == player_name]['cluster'].values[0]
        selected_cluster_points = position_players[position_players['cluster'] == selected_cluster][['PCA_Component_1', 'PCA_Component_2']].values

        
        # Mettre en évidence le cluster du joueur sélectionné
        ax1.scatter(
            selected_cluster_points[:, 0], 
            selected_cluster_points[:, 1], 
            color='yellow', edgecolor='black', linewidth=1.5, s=150, label='Cluster du joueur sélectionné', zorder=3
        )

        # Montrer où se trouve le joueur sélectionné dans son cluster avec une croix plus épaisse
        ax1.scatter(
            selected_player_pca[0, 0], 
            selected_player_pca[0, 1], 
            color='red', marker='x', s=200, label=f'{player_name} (Joueur sélectionné)', zorder=4, linewidth=4, edgecolors='black'
        )

        # Si le joueur a plusieurs positions, les afficher séparées par une virgule
        positions_str = ', '.join(positions) if len(positions) > 1 else positions[0]
        
        # Ajouter le titre en blanc et en gras avec les positions correctement affichées
        ax1.set_title(f'Clustering des joueurs à la position : {positions_str}', fontsize=25, color='white', fontweight='bold')


        # Ajouter les labels des axes en blanc et en gras avec détails supplémentaires
        ax1.set_xlabel('Contribution Offensive (PCA Composante 1)', fontsize=16, color='white', fontweight='bold')
        ax1.set_ylabel('Contribution Défensive (PCA Composante 2)', fontsize=16, color='white', fontweight='bold')

        # Appliquer la personnalisation des axes (contours blancs et épais)
        self.customize_axes(ax1)

        # Ajouter les ticks des axes (graduations) en blanc
        ax1.tick_params(axis='x', colors='white', labelsize=14)
        ax1.tick_params(axis='y', colors='white', labelsize=14)

        # Ajuster automatiquement les limites des axes en fonction des données
        ax1.set_xlim(np.floor(np.min(position_players['PCA_Component_1'])) - 1, np.ceil(np.max(position_players['PCA_Component_1'])) + 1)
        ax1.set_ylim(np.floor(np.min(position_players['PCA_Component_2'])) - 1, np.ceil(np.max(position_players['PCA_Component_2'])) + 1)
        
        # Ajouter l'étiquette Twitter
        ax1.text(0.5, 0.75, f"@TarbouchData", fontsize=14, color='white', fontweight='bold', ha='left', transform=ax1.transAxes, alpha=0.8)

        # Afficher la légende avec du texte en blanc
        legend = ax1.legend()
        plt.setp(legend.get_texts(), color='black')

        # Colonne de droite : tableau des joueurs les plus proches (20%)
        ax2 = fig.add_subplot(gs[1], facecolor='none')  # Fond transparent
        ax2.axis('tight')
        ax2.axis('off')

        # Sélectionner les 10 joueurs les plus proches du même cluster
        closest_players = sorted_players[sorted_players['cluster'] == selected_cluster][['player_name', 'distance_to_selected']].head(10)
        closest_players = closest_players[closest_players['player_name'] != player_name]

        # Convertir les distances en arrondissant à 2 décimales
        closest_players['distance_to_selected'] = closest_players['distance_to_selected'].round(2)

        # Créer un tableau dans la colonne de droite avec des cases transparentes sauf l'en-tête
        table_data = closest_players.values
        table = ax2.table(cellText=table_data, colLabels=['Nom', f'Distance - {player_name}'], cellLoc='center', loc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(11)
        table.scale(2, 4.1)  # Augmenter la taille du tableau (hauteur et largeur)

        # Appliquer des bordures blanches et épaisses, et un texte gras pour le tableau
        for key, cell in table.get_celld().items():
            cell.set_edgecolor('white')  # Bordure blanche
            cell.set_linewidth(3)  # Bordures épaisses
            cell.set_text_props(weight='bold', color='white')  # Texte gras
            if key[0] == 0:  # En-tête
                cell.set_facecolor('#3b3700')  # Couleur de l'en-tête
                cell.set_text_props(color='white')  # Texte en blanc pour l'en-tête
            else:
                cell.set_facecolor('none')  # Cases transparentes pour les autres lignes


        # Calculer les extrémums et les noms des joueurs associés pour PCA_Component_1 et PCA_Component_2
        min_pca1_row = position_players.loc[position_players['PCA_Component_1'].idxmin()]
        max_pca1_row = position_players.loc[position_players['PCA_Component_1'].idxmax()]
        min_pca2_row = position_players.loc[position_players['PCA_Component_2'].idxmin()]
        max_pca2_row = position_players.loc[position_players['PCA_Component_2'].idxmax()]

        # Afficher les extrémums avec le nom des joueurs
        print(f"Extrémum de PCA_Component_1: min = {min_pca1_row['PCA_Component_1']} ({min_pca1_row['player_name']}), max = {max_pca1_row['PCA_Component_1']} ({max_pca1_row['player_name']})")
        print(f"Extrémum de PCA_Component_2: min = {min_pca2_row['PCA_Component_2']} ({min_pca2_row['player_name']}), max = {max_pca2_row['PCA_Component_2']} ({max_pca2_row['player_name']})")

        # Sauvegarder le fichier et afficher le graphique
        plt.subplots_adjust(left=0.05)

        plt.savefig(f"{output_dir}/clustering_{player_name}_styled.png", format='png')
        plt.show()

    

    def clustering_multiple_players_comparison_with_reference(self, player_names, data, offensive_features, defensive_features):
        """Effectuer un clustering et comparer le premier joueur avec les autres de la liste."""
        output_dir = 'viz_data/clustering'
        os.makedirs(output_dir, exist_ok=True)

        valid_players = data['player_name'].isin(player_names)
        selected_players = data[valid_players]

        if selected_players.empty:
            print(f"Aucun des joueurs {', '.join(player_names)} n'a été trouvé.")
            return

        # Obtenir les positions des joueurs (on prend la première position du premier joueur pour simplifier)
        positions = selected_players['Position'].values[0].split(',')

        # Vérifier les positions et filtrer les joueurs
        if len(positions) > 1:
            position_filter = '|'.join(positions)
            position_players = data[data['Position'].str.contains(position_filter, na=False)]
        else:
            position_players = data[data['Position'] == positions[0]]

        # Filtrer les caractéristiques et standardiser
        position_players = position_players.dropna(subset=offensive_features + defensive_features)
        scaler_offensive = StandardScaler()
        scaler_defensive = StandardScaler()

        offensive_scaled = scaler_offensive.fit_transform(position_players[offensive_features])
        defensive_scaled = scaler_defensive.fit_transform(position_players[defensive_features])

        # PCA pour les variables offensives et défensives
        pca_offensive = PCA(n_components=1)
        offensive_component = pca_offensive.fit_transform(offensive_scaled)

        pca_defensive = PCA(n_components=1)
        defensive_component = pca_defensive.fit_transform(defensive_scaled)

        # Ajouter les composantes PCA au DataFrame
        position_players['PCA_Component_1'] = offensive_component.flatten()
        position_players['PCA_Component_2'] = defensive_component.flatten()

        # Clustering avec KMeans
        kmeans = KMeans(n_clusters=3)
        position_players['cluster'] = kmeans.fit_predict(np.column_stack([offensive_component, defensive_component]))

        # Le premier joueur est la référence
        reference_player = player_names[0]
        reference_player_pca = position_players[position_players['player_name'] == reference_player][['PCA_Component_1', 'PCA_Component_2']].values

        # Calculer les distances du joueur de référence avec les autres
        other_players = player_names[1:]  # Exclure le joueur de référence
        other_players_pca = position_players[position_players['player_name'].isin(other_players)][['PCA_Component_1', 'PCA_Component_2']].values

        distances = cdist(reference_player_pca, other_players_pca, metric='euclidean').flatten()

        # Créer une figure avec une répartition 60%-40% pour les colonnes
        fig = plt.figure(figsize=(16, 9))
        gs = GridSpec(1, 2, width_ratios=[3, 1], wspace=0.3)  # 60% pour le graphique, 40% pour le tableau

        # Créer le fond en dégradé pour l'ensemble de la figure
        self.create_gradient_background(fig)

        # Colonne de gauche : graphique des clusters (60%)
        ax1 = fig.add_subplot(gs[0], facecolor='none')  # Fond transparent
    
        # Afficher les clusters dans l'axe de gauche
        scatter = ax1.scatter(
            position_players['PCA_Component_1'], 
            position_players['PCA_Component_2'], 
            c=position_players['cluster'], 
            s=100, cmap='rainbow', edgecolor='black', linewidth=1.5, zorder=1
        )
    
        # Mettre en évidence le joueur de référence avec une croix jaune
        ref_scatter = ax1.scatter(
            reference_player_pca[0, 0], 
            reference_player_pca[0, 1], 
            color='yellow', marker='x', s=300, 
            zorder=4, linewidth=4, edgecolors='black', label=f'{reference_player} (Référence)'
        )
    
        # Ajouter une croix rouge pour chaque autre joueur sélectionné
        comp_scatters = []
        for player in other_players:
            player_pca = position_players[position_players['player_name'] == player][['PCA_Component_1', 'PCA_Component_2']].values
            comp_scatter = ax1.scatter(
                player_pca[0, 0], 
                player_pca[0, 1], 
                color='red', marker='x', s=300, 
                zorder=4, linewidth=4, edgecolors='black'
            )
            comp_scatters.append(comp_scatter)
    
        # Si le joueur a plusieurs positions, les afficher séparées par une virgule
        positions_str = ', '.join(positions) if len(positions) > 1 else positions[0]
    
        # Ajouter le titre en blanc et en gras avec les positions correctement affichées
        ax1.set_title(f'Clustering des joueurs pour la position : {positions_str}', fontsize=25, color='white', fontweight='bold')
    
        # Ajouter les labels des axes en blanc et en gras avec détails supplémentaires
        ax1.set_xlabel('Contribution Offensive (PCA Composante 1)', fontsize=16, color='white', fontweight='bold')
        ax1.set_ylabel('Contribution Défensive (PCA Composante 2)', fontsize=16, color='white', fontweight='bold')
    
        # Appliquer la personnalisation des axes (contours blancs et épais)
        self.customize_axes(ax1)
    
        # Ajouter les ticks des axes (graduations) en blanc
        ax1.tick_params(axis='x', colors='white', labelsize=14)
        ax1.tick_params(axis='y', colors='white', labelsize=14)
    
        # Ajuster automatiquement les limites des axes en fonction des données
        ax1.set_xlim(np.floor(np.min(position_players['PCA_Component_1'])) - 1, np.ceil(np.max(position_players['PCA_Component_1'])) + 1)
        ax1.set_ylim(np.floor(np.min(position_players['PCA_Component_2'])) - 1, np.ceil(np.max(position_players['PCA_Component_2'])) + 1)
    
        # Ajouter l'étiquette Twitter
        ax1.text(0.5, 0.75, f"@TarbouchData", fontsize=14, color='white', fontweight='bold', ha='left', transform=ax1.transAxes, alpha=0.8)
    
        # Ajouter la légende avec croix jaune et rouge
        legend_labels = [f'{player_names[0]} (Référence)', 'Joueurs comparés']
        legend_handles = [ref_scatter, comp_scatter]  # Un exemple d'un seul scatter rouge suffira pour la légende
        legend = ax1.legend(legend_handles, legend_labels, loc='upper right')
        plt.setp(legend.get_texts(), color='black')
    

        # Colonne de droite : tableau des distances entre le joueur de référence et les autres (40%)
        ax2 = fig.add_subplot(gs[1], facecolor='none')  # Fond transparent
        ax2.axis('tight')
        ax2.axis('off')

        # Créer un tableau avec deux colonnes : Joueur, Distance avec {Joueur de référence}
        closest_players = pd.DataFrame({
            'Nom': other_players,
            f'Distance - {reference_player}': distances.round(2)
        })

        # Créer un tableau dans la colonne de droite
        table_data = closest_players.values
        table = ax2.table(cellText=table_data, colLabels=['Nom', f'Distance - {reference_player}'], cellLoc='center', loc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(11)
        table.scale(2, 4.1)  # Augmenter la taille du tableau (hauteur et largeur)

        # Appliquer des bordures blanches et épaisses, et un texte gras pour le tableau
        for key, cell in table.get_celld().items():
            cell.set_edgecolor('white')  # Bordure blanche
            cell.set_linewidth(3)  # Bordures épaisses
            cell.set_text_props(weight='bold', color='white')  # Texte gras
            if key[0] == 0:  # En-tête
                cell.set_facecolor('#3b3700')  # Couleur de l'en-tête
                cell.set_text_props(color='white')  # Texte en blanc pour l'en-tête
            else:
                cell.set_facecolor('none')  # Cases transparentes pour les autres lignes

        # Sauvegarder le fichier et afficher le graphique
        plt.subplots_adjust(left=0.05)
        plt.savefig(f"{output_dir}/clustering_{reference_player}_vs_others_styled.png", format='png')
        plt.show()

    def clustering_players_pca_comparison(self, player_names, data, offensive_features, defensive_features, threshold_distance=1):
        """Effectuer un PCA sur une liste de joueurs sélectionnés et les afficher sur un graphique."""
        output_dir = 'viz_data/clustering'
        os.makedirs(output_dir, exist_ok=True)
    
        # Sélectionner les joueurs par leurs noms qui sont présents dans les données
        valid_players = data['player_name'].isin(player_names)
        selected_players = data[valid_players]
    
        # Vérifier s'il y a des joueurs valides
        if selected_players.empty:
            print(f"Aucun des joueurs sélectionnés n'a été trouvé dans les données.")
            return
    
        # Récupérer la liste des joueurs valides (ceux qui existent dans le DataFrame)
        valid_player_names = selected_players['player_name'].tolist()
    
        # Afficher un message pour les joueurs qui ne sont pas trouvés dans les données
        missing_players = [name for name in player_names if name not in valid_player_names]
        if missing_players:
            print(f"Les joueurs suivants n'ont pas été trouvés et seront ignorés : {', '.join(missing_players)}")
    
        # Filtrer les caractéristiques et standardiser
        selected_players = selected_players.dropna(subset=offensive_features + defensive_features)
        scaler_offensive = StandardScaler()
        scaler_defensive = StandardScaler()
    
        offensive_scaled = scaler_offensive.fit_transform(selected_players[offensive_features])
        defensive_scaled = scaler_defensive.fit_transform(selected_players[defensive_features])
    
        # PCA pour les variables offensives et défensives
        pca_offensive = PCA(n_components=1)
        offensive_component = pca_offensive.fit_transform(offensive_scaled)
    
        pca_defensive = PCA(n_components=1)
        defensive_component = pca_defensive.fit_transform(defensive_scaled)
    
        # Ajouter les composantes PCA au DataFrame
        selected_players['PCA_Component_1'] = offensive_component.flatten()
        selected_players['PCA_Component_2'] = defensive_component.flatten()
    
        # Le premier joueur est la référence (s'il est parmi les joueurs valides)
        reference_player = valid_player_names[0]
        reference_player_pca = selected_players[selected_players['player_name'] == reference_player][['PCA_Component_1', 'PCA_Component_2']].values
    
        # Créer la figure
        fig = plt.figure(figsize=(16, 9))  # Taille pour appareils mobiles
        self.create_gradient_background(fig)  # Fond en dégradé
    
        # Ajouter un axe pour le graphique principal, avec un fond transparent
        ax = fig.add_subplot(111, facecolor='none')  # Fond transparent
    
        # Afficher les joueurs avec des points (pas de croix)
        scatter = ax.scatter(
            selected_players['PCA_Component_1'], 
            selected_players['PCA_Component_2'], 
            color='red', edgecolor='black', s=200, zorder=1
        )
    
        # Ajuster les limites des axes
        ax.set_xlim(np.floor(np.min(selected_players['PCA_Component_1'])) - 1, np.ceil(np.max(selected_players['PCA_Component_1'])) + 1)
        ax.set_ylim(np.floor(np.min(selected_players['PCA_Component_2'])) - 1, np.ceil(np.max(selected_players['PCA_Component_2'])) + 1)
    
        # Ajouter les noms des joueurs
        displayed_names = []
        for i, row in selected_players.iterrows():
            name = row['player_name']
            x, y = row['PCA_Component_1'], row['PCA_Component_2']
    
            # Éviter la superposition des noms en vérifiant la distance entre les points
            if not any(np.linalg.norm([x - dx, y - dy]) < threshold_distance/3 for dx, dy in displayed_names):
                ax.text(x + 0.2, y + 0.1, name, fontsize=12, ha='right', va='bottom', fontweight='bold', color='white', zorder=3)
                displayed_names.append((x, y))
    
        # Ajouter le titre en blanc et en gras
        ax.set_title(f'PCA des joueurs sélectionnés', fontsize=25, color='white', fontweight='bold')
    
        # Ajouter les labels des axes en blanc et en gras
        ax.set_xlabel('Contribution Offensive (PCA Composante 1)', fontsize=16, color='white', fontweight='bold')
        ax.set_ylabel('Contribution Défensive (PCA Composante 2)', fontsize=16, color='white', fontweight='bold')
    
        # Ajouter l'étiquette Twitter
        ax.text(0.5, 0.75, f"@TarbouchData", fontsize=14, color='white', fontweight='bold', ha='left', transform=ax.transAxes, alpha=0.8)
    
        # Appliquer la personnalisation des axes (contours blancs et épais)
        self.customize_axes(ax)
    
        # Ajouter les ticks des axes en blanc
        ax.tick_params(axis='x', colors='white', labelsize=14)
        ax.tick_params(axis='y', colors='white', labelsize=14)
    
        # Sauvegarder le fichier et afficher le graphique
        plt.savefig(f"{output_dir}/pca_comparison_selected_styled.png", format='png', dpi=300)
        plt.show()
    
    def compare_teams(self, team1_name, team2_name, threshold_distance=1):
            """Compare deux équipes en affichant les joueurs sur un graphique basé sur création d'occasions (tentatives) et finition (réussites)."""

            # Créer une figure avec des dimensions adaptées pour les appareils mobiles
            fig = plt.figure(figsize=(16, 9))  # Largeur 16, hauteur 9 pour un ajustement mobile

            # Créer le fond en dégradé pour l'ensemble de la figure
            self.create_gradient_background(fig)

            # Ajouter un axe pour le graphique principal, avec un fond transparent
            ax = fig.add_subplot(111, facecolor='none')  # Fond transparent

            # Extraire les colonnes pour la création d'occasions (x) et la finition (y)
            x_values = self.features['npxG: xG sans les pénaltys']  # Exemple de tentatives: npxG (expected goals sans pénaltys)
            y_values = self.features['Buts (sans les pénaltys)']  # Exemple de réussite: Buts sans pénaltys

            # Filtrer les données pour chaque équipe
            team1_players = self.players_data[self.players_data['Team Name'] == team1_name]
            team2_players = self.players_data[self.players_data['Team Name'] == team2_name]

            if team1_players.empty:
                print(f"Aucun joueur trouvé pour l'équipe {team1_name}.")
                return

            if team2_players.empty:
                print(f"Aucun joueur trouvé pour l'équipe {team2_name}.")
                return

            # Tracer les joueurs de l'équipe 1 avec des points rouges
            team1_scatter = ax.scatter(team1_players['npxG: xG sans les pénaltys'], team1_players['Buts (sans les pénaltys)'],
                                       color='red', edgecolor='black', s=200, zorder=1, label=team1_name)

            # Tracer les joueurs de l'équipe 2 avec des points bleus
            team2_scatter = ax.scatter(team2_players['npxG: xG sans les pénaltys'], team2_players['Buts (sans les pénaltys)'],
                                       color='blue', edgecolor='black', s=200, zorder=1, label=team2_name)

            # Ajuster les limites de l'axe en fonction des données
            ax.set_xlim(np.floor(np.min(x_values)) - 1, np.ceil(np.max(x_values)) + 1)
            ax.set_ylim(np.floor(np.min(y_values)) - 1, np.ceil(np.max(y_values)) + 1)

            # Afficher les noms des joueurs des deux équipes
            displayed_names = []

            # Affichage des noms pour l'équipe 1
            for i, row in team1_players.iterrows():
                name = row['player_name']
                x, y = row['npxG: xG sans les pénaltys'], row['Buts (sans les pénaltys)']

                if not any(np.linalg.norm([x - dx, y - dy]) < (threshold_distance / 2) for dx, dy in displayed_names):
                    ax.text(x + 0.2, y + 0.1, name, fontsize=12, ha='right', va='bottom', fontweight='bold', color='white', zorder=3)
                    displayed_names.append((x, y))

            # Affichage des noms pour l'équipe 2
            for i, row in team2_players.iterrows():
                name = row['player_name']
                x, y = row['npxG: xG sans les pénaltys'], row['Buts (sans les pénaltys)']

                if not any(np.linalg.norm([x - dx, y - dy]) < (threshold_distance / 2) for dx, dy in displayed_names):
                    ax.text(x + 0.2, y + 0.1, name, fontsize=12, ha='right', va='bottom', fontweight='bold', color='white', zorder=3)
                    displayed_names.append((x, y))

            # Ajouter le titre en blanc et en gras
            ax.set_title(f'Comparaison - ({team1_name} vs {team2_name})', fontsize=25, color='white', fontweight='bold')

            # Ajouter les labels des axes en fonction des nouvelles variables
            ax.set_xlabel('Création d\'occasions (npxG - expected goals sans pénaltys)', fontsize=16, color='white', fontweight='bold')
            ax.set_ylabel('Finition des occasions (Buts sans pénaltys)', fontsize=16, color='white', fontweight='bold')

            # Ajouter l'étiquette Twitter
            ax.text(0.5, 0.75, f"@TarbouchData", fontsize=14, color='white', fontweight='bold', ha='left', transform=ax.transAxes, alpha=0.8)

            # Appliquer la personnalisation des axes (contours blancs et épais)
            self.customize_axes(ax)

            # Ajouter les ticks des axes (graduations) en blanc
            ax.tick_params(axis='x', colors='white', labelsize=14)
            ax.tick_params(axis='y', colors='white', labelsize=14)

            # Ajouter les ticks pour montrer les valeurs de progression moyenne par match (seulement des entiers)
            ax.set_xticks(np.arange(np.floor(np.min(x_values)), np.ceil(np.max(x_values)) + 1, 1))
            ax.set_yticks(np.arange(np.floor(np.min(y_values)), np.ceil(np.max(y_values)) + 1, 1))

            # Ajouter la légende pour indiquer les équipes
            ax.legend(loc='upper left', fontsize=14, facecolor='white', framealpha=0.5)

            # Sauvegarder le fichier et afficher le graphique
            plt.savefig(f"viz_data/comparaison_tentatives_reussites_{team1_name}_vs_{team2_name}.jpeg", format='jpeg', dpi=300)
            plt.show()

    def compare_teams(self, team1_name, team2_name, threshold_distance=1):
        """Compare deux équipes en affichant les joueurs sur un graphique basé sur création d'occasions (tentatives) et finition (réussites)."""
        
        # Créer une figure avec des dimensions adaptées pour les appareils mobiles
        fig = plt.figure(figsize=(16, 9))  # Largeur 16, hauteur 9 pour un ajustement mobile
        
        # Créer le fond en dégradé pour l'ensemble de la figure
        self.create_gradient_background(fig)
        
        # Ajouter un axe pour le graphique principal, avec un fond transparent
        ax = fig.add_subplot(111, facecolor='none')  # Fond transparent
        
        # Filtrer les données pour chaque équipe
        team1_players = self.players_data[self.players_data['Team Name'] == team1_name]
        team2_players = self.players_data[self.players_data['Team Name'] == team2_name]
    
        if team1_players.empty:
            print(f"Aucun joueur trouvé pour l'équipe {team1_name}.")
            return
    
        if team2_players.empty:
            print(f"Aucun joueur trouvé pour l'équipe {team2_name}.")
            return
        
        # Combiner les données des deux équipes pour calculer les valeurs min/max
        combined_data = pd.concat([team1_players, team2_players])
    
        # Extraire les colonnes pour la création d'occasions (x) et la finition (y)
        x_values = combined_data['npxG: xG sans les pénaltys']
        y_values = combined_data['Buts (sans les pénaltys)']
    
        # Tracer les joueurs de l'équipe 1 avec des points rouges
        team1_scatter = ax.scatter(team1_players['npxG: xG sans les pénaltys'], team1_players['Buts (sans les pénaltys)'],
                                   color='red', edgecolor='black', s=200, zorder=1, label=team1_name)
    
        # Tracer les joueurs de l'équipe 2 avec des points bleus
        team2_scatter = ax.scatter(team2_players['npxG: xG sans les pénaltys'], team2_players['Buts (sans les pénaltys)'],
                                   color='blue', edgecolor='black', s=200, zorder=1, label=team2_name)
    
        # Ajuster automatiquement les limites de l'axe en fonction des valeurs min/max
        x_min, x_max = np.floor(x_values.min()) - 1 , np.ceil(x_values.max()) + 1
        y_min, y_max = np.floor(y_values.min()) - 1 , np.ceil(y_values.max()) + 1
        ax.set_xlim(x_min, x_max)
        ax.set_ylim(y_min, y_max)
    
        # Afficher les noms des joueurs des deux équipes
        displayed_names = []
    
        # Affichage des noms pour l'équipe 1
        for i, row in team1_players.iterrows():
            name = row['player_name']
            x, y = row['npxG: xG sans les pénaltys'], row['Buts (sans les pénaltys)']
    
            if not any(np.linalg.norm([x - dx, y - dy]) < (threshold_distance / 10) for dx, dy in displayed_names):
                ax.text(x + 0.2, y + 0.1, name, fontsize=12, ha='right', va='bottom', fontweight='bold', color='white', zorder=3)
                displayed_names.append((x, y))
    
        # Affichage des noms pour l'équipe 2
        for i, row in team2_players.iterrows():
            name = row['player_name']
            x, y = row['npxG: xG sans les pénaltys'], row['Buts (sans les pénaltys)']
    
            if not any(np.linalg.norm([x - dx, y - dy]) < (threshold_distance / 2) for dx, dy in displayed_names):
                ax.text(x + 0.2, y + 0.1, name, fontsize=12, ha='right', va='bottom', fontweight='bold', color='white', zorder=3)
                displayed_names.append((x, y))
    
        # Ajouter le titre en blanc et en gras
        ax.set_title(f'Comparaison - ({team1_name} vs {team2_name})', fontsize=25, color='white', fontweight='bold')
    
        # Ajouter les labels des axes en fonction des nouvelles variables
        ax.set_xlabel('Création d\'occasions (npxG - expected goals sans pénaltys)', fontsize=16, color='white', fontweight='bold')
        ax.set_ylabel('Finition des occasions (Buts sans pénaltys)', fontsize=16, color='white', fontweight='bold')
    
        # Ajouter l'étiquette Twitter
        ax.text(0.5, 0.75, f"@TarbouchData", fontsize=14, color='white', fontweight='bold', ha='left', transform=ax.transAxes, alpha=0.8)
    
        # Appliquer la personnalisation des axes (contours blancs et épais)
        self.customize_axes(ax)
    
        # Ajouter les ticks des axes (graduations) en blanc
        ax.tick_params(axis='x', colors='white', labelsize=14)
        ax.tick_params(axis='y', colors='white', labelsize=14)
    
        # Ajouter les ticks pour montrer les valeurs de progression moyenne par match (seulement des entiers)
        ax.set_xticks(np.arange(x_min, x_max + 1, 1))
        ax.set_yticks(np.arange(y_min, y_max + 1, 1))
    
        # Ajouter la légende pour indiquer les équipes
        ax.legend(loc='upper left', fontsize=14, facecolor='white', framealpha=0.5)
    
        # Sauvegarder le fichier et afficher le graphique
        plt.savefig(f"viz_data/comparaison_tentatives_reussites_{team1_name}_vs_{team2_name}.jpeg", format='jpeg', dpi=300)
        plt.show()
    
    def compare_teams(self, team1_name, team2_name, threshold_distance=1):
        """Compare deux équipes en affichant les joueurs sur un graphique basé sur création d'occasions (tentatives) et finition (réussites)."""

        # Créer une figure avec des dimensions adaptées pour les appareils mobiles
        fig = plt.figure(figsize=(16, 9))  # Largeur 16, hauteur 9 pour un ajustement mobile

        # Créer le fond en dégradé pour l'ensemble de la figure
        self.create_gradient_background(fig)

        # Ajouter un axe pour le graphique principal, avec un fond transparent
        ax = fig.add_subplot(111, facecolor='none')  # Fond transparent

        # Filtrer les données pour chaque équipe
        team1_players = self.players_data[self.players_data['Team Name'] == team1_name]
        team2_players = self.players_data[self.players_data['Team Name'] == team2_name]

        # Exclure les joueurs ayant x=0 ou y=0
        team1_players = team1_players[(team1_players['npxG: xG sans les pénaltys'] > 0) & 
                                      (team1_players['Buts (sans les pénaltys)'] > 0)]
        team2_players = team2_players[(team2_players['npxG: xG sans les pénaltys'] > 0) & 
                                      (team2_players['Buts (sans les pénaltys)'] > 0)]

        if team1_players.empty:
            print(f"Aucun joueur trouvé pour l'équipe {team1_name} après filtrage.")
            return

        if team2_players.empty:
            print(f"Aucun joueur trouvé pour l'équipe {team2_name} après filtrage.")
            return

        # Combiner les données des deux équipes pour calculer les valeurs min/max
        combined_data = pd.concat([team1_players, team2_players])

        # Extraire les colonnes pour la création d'occasions (x) et la finition (y)
        x_values = combined_data['npxG: xG sans les pénaltys']
        y_values = combined_data['Buts (sans les pénaltys)']

        # Tracer les joueurs de l'équipe 1 avec des points rouges
        team1_scatter = ax.scatter(team1_players['npxG: xG sans les pénaltys'], team1_players['Buts (sans les pénaltys)'],
                                   color='red', edgecolor='black', s=200, zorder=1, label=team1_name)

        # Tracer les joueurs de l'équipe 2 avec des points bleus
        team2_scatter = ax.scatter(team2_players['npxG: xG sans les pénaltys'], team2_players['Buts (sans les pénaltys)'],
                                   color='blue', edgecolor='black', s=200, zorder=1, label=team2_name)

        # Ajuster automatiquement les limites de l'axe en fonction des valeurs min/max
        x_min, x_max = np.floor(x_values.min()) - 0.1 , np.ceil(x_values.max()) - 1.5
        y_min, y_max = np.floor(y_values.min()) - 0.1 , np.ceil(y_values.max()) - 1.5
        ax.set_xlim(x_min, x_max)
        ax.set_ylim(y_min, y_max)

        # Afficher les noms des joueurs des deux équipes
        displayed_names = []

        # Affichage des noms pour l'équipe 1
        for i, row in team1_players.iterrows():
            name = row['player_name']
            x, y = row['npxG: xG sans les pénaltys'], row['Buts (sans les pénaltys)']

            if not any(np.linalg.norm([x - dx, y - dy]) < (threshold_distance / 100) for dx, dy in displayed_names):
                ax.text(x + 0.02, y + 0.01, name, fontsize=12, ha='right', va='bottom', fontweight='bold', color='white', zorder=3)
                displayed_names.append((x, y))

        # Affichage des noms pour l'équipe 2
        for i, row in team2_players.iterrows():
            name = row['player_name']
            x, y = row['npxG: xG sans les pénaltys'], row['Buts (sans les pénaltys)']

            if not any(np.linalg.norm([x - dx, y - dy]) < (threshold_distance / 100) for dx, dy in displayed_names):
                ax.text(x + 0.02, y + 0.01, name, fontsize=12, ha='right', va='bottom', fontweight='bold', color='white', zorder=3)
                displayed_names.append((x, y))

        # Ajouter le titre en blanc et en gras
        ax.set_title(f'Comparaison - ({team1_name} vs {team2_name})', fontsize=25, color='white', fontweight='bold')

        # Ajouter les labels des axes en fonction des nouvelles variables
        ax.set_xlabel('Création d\'occasions/90 (npxG - expected goals sans pénaltys)', fontsize=16, color='white', fontweight='bold')
        ax.set_ylabel('Finition des occasions/90 (Buts sans pénaltys)', fontsize=16, color='white', fontweight='bold')

        # Ajouter l'étiquette Twitter
        ax.text(0.5, 0.75, f"@TarbouchData", fontsize=14, color='white', fontweight='bold', ha='left', transform=ax.transAxes, alpha=0.8)

        # Appliquer la personnalisation des axes (contours blancs et épais)
        self.customize_axes(ax)

        # Ajouter les ticks des axes (graduations) en blanc
        ax.tick_params(axis='x', colors='white', labelsize=14)
        ax.tick_params(axis='y', colors='white', labelsize=14)

        # Ajouter les ticks pour montrer les valeurs de progression moyenne par match (seulement des entiers)
        ax.set_xticks(np.arange(x_min, x_max + 1, 0.25))
        ax.set_yticks(np.arange(y_min, y_max + 1, 0.25))

        # Ajouter la légende pour indiquer les équipes
        ax.legend(loc='upper left', fontsize=14, facecolor='white', framealpha=0.5)

        # Sauvegarder le fichier et afficher le graphique
        plt.savefig(f"viz_data/comparaison_tentatives_reussites_{team1_name}_vs_{team2_name}.jpeg", format='jpeg', dpi=300)
        plt.show()
