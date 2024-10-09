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

    def plot_players_from_list(self, player_names, threshold_distance=1,):
        # Créer une figure avec des dimensions adaptées pour les appareils mobiles
        fig = plt.figure(figsize=(16, 9))  # Largeur 16, hauteur 9 pour un ajustement mobile

        # Créer le fond en dégradé pour l'ensemble de la figure
        self.create_gradient_background(fig)

        # Ajouter un axe pour le graphique principal, avec un fond transparent
        ax = fig.add_subplot(111, facecolor='none')  # Fond transparent

        # Extraire les colonnes pour les passes progressives (X) et les possessions progressives (Y)
        x_values = self.features['Passes progressives']
        y_values = self.features['Possessions progressives']

        # Filtrer les données pour ne garder que les joueurs dans la liste donnée
        filtered_players = self.players_data[self.players_data['player_name'].isin(player_names)]

        # Tracer les joueurs spécifiés dans la liste filtrée
        scatter = ax.scatter(x_values, y_values, color='red', edgecolor='black', s=200, zorder=1)

        # Ajuster les limites de l'axe
        ax.set_xlim(np.min(x_values) - 1, np.max(x_values) + 1)
        ax.set_ylim(np.min(y_values) - 1, np.max(y_values) + 1)

        # Afficher les noms des joueurs
        displayed_names = []
        for i, row in filtered_players.iterrows():
            name = row['player_name']
            x, y = row['Passes progressives'], row['Possessions progressives']

            # Éviter la superposition des noms avec une condition moins stricte
            if not any(np.linalg.norm([x - dx, y - dy]) < (threshold_distance / 2) for dx, dy in displayed_names):
                ax.text(x + 0.2, y + 0.1, name, fontsize=12, ha='right', va='bottom', fontweight='bold', color='white', zorder=3)
                displayed_names.append((x, y))

        # Ajouter le titre en blanc et en gras
        ax.set_title('Projection des Passes et des Possessions progressives (FBREF)', fontsize=25, color='white', fontweight='bold')

        # Ajouter les labels des axes en blanc et en gras
        ax.set_xlabel('PROGRESSION PAR LA PASSE', fontsize=20, color='white', fontweight='bold')
        ax.set_ylabel('PROGRESSION PAR LA CONDUITE DE BALLE', fontsize=20, color='white', fontweight='bold')

        ax.text(0.5, 0.75, f"@TarbouchData", fontsize=14, color='white', fontweight='bold', ha='left', transform=ax.transAxes, alpha=0.8)

        # Appliquer la personnalisation des axes (contours blancs et épais)
        self.customize_axes(ax)

        # Retirer les ticks des axes pour rendre l'affichage plus propre
        ax.set_xticks([])
        ax.set_yticks([])

        plt.savefig("viz_data/projection_passes_possessions.jpeg", format='jpeg', dpi=300)  # Sauvegarde en format JPEG avec résolution de 300 DPI

        # Afficher le graphique à l'écran
        plt.show()
