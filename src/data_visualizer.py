import matplotlib.pyplot as plt
import numpy as np
from sklearn.decomposition import PCA

class DataVisualizer:
    def __init__(self, scaled_features, players_data):
        self.scaled_features = scaled_features
        self.players_data = players_data
        self.pca = PCA(n_components=2)
        self.pca_components = self.pca.fit_transform(scaled_features)

        self.players_data['PCA_Component_1'] = self.pca_components[:, 0]
        self.players_data['PCA_Component_2'] = self.pca_components[:, 1]

    def plot_player(self, player_name, positions, threshold_distance=1):
        selected_player_pca = self.pca_components[self.players_data['player_name'] == player_name]

        plt.figure(figsize=(14, 8))
        plt.scatter(self.pca_components[:, 0], self.pca_components[:, 1], color='blue', s=30)
        plt.scatter(selected_player_pca[0, 0], selected_player_pca[0, 1], color='green', s=150, zorder=5)

        displayed_names = []
        for i, row in self.players_data.iterrows():
            name = row['player_name']
            x, y = row['PCA_Component_1'], row['PCA_Component_2']

            too_close = False
            for x_disp, y_disp in displayed_names:
                if np.linalg.norm([x - x_disp, y - y_disp]) < threshold_distance:
                    too_close = True
                    break

            if not too_close or player_name == name:
                plt.text(x+0.2, y+0.1, name, fontsize=9, ha='right', va='bottom', fontweight='bold')
                displayed_names.append((x, y))

        plt.title(f'Projection PCA pour les joueurs en {positions[0]} (Joueur sélectionné: {player_name})', fontsize=16)
        plt.xlabel('Progression par la passe (PCA Composante 1)', fontsize=12)
        plt.ylabel('Progression par la conduite de balle (PCA Composante 2)', fontsize=12)
        plt.xticks([])
        plt.yticks([])
        plt.show()

    def plot_comparison(self, player_names, threshold_distance=1):
        plt.figure(figsize=(14, 8))
        plt.scatter(self.pca_components[:, 0], self.pca_components[:, 1], color='blue', s=30)

        displayed_names = []
        for player_name in player_names:
            selected_player_pca = self.pca_components[self.players_data['player_name'] == player_name]
            plt.scatter(selected_player_pca[0, 0], selected_player_pca[0, 1], color='green', s=150, zorder=5)

        for i, row in self.players_data.iterrows():
            name = row['player_name']
            x, y = row['PCA_Component_1'], row['PCA_Component_2']

            too_close = False
            for x_disp, y_disp in displayed_names:
                if np.linalg.norm([x - x_disp, y - y_disp]) < threshold_distance:
                    too_close = True
                    break

            if not too_close or name in player_names:
                plt.text(x+0.2, y+0.1, name, fontsize=9, ha='right', va='bottom', fontweight='bold')
                displayed_names.append((x, y))

        plt.title('Comparaison de joueurs', fontsize=16)
        plt.xlabel('Progression par la passe (PCA Composante 1)', fontsize=12)
        plt.ylabel('Progression par la conduite de balle (PCA Composante 2)', fontsize=12)
        plt.xticks([])
        plt.yticks([])
        plt.show()
