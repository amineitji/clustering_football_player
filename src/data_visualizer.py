import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors
import os

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
