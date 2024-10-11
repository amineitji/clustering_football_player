🧵 Thread : Le Clustering et l’Analyse en Composantes Principales dans le football data – Qui pour remplacer Mbappé au PSG ? ⚽🔍

1/ Le défi : Le potentiel départ de Kylian Mbappé du PSG ouvre une question cruciale : qui pourrait le remplacer ? En combinant l'ACP et le clustering, nous allons explorer les données pour découvrir les joueurs qui se rapprochent le plus de son profil dans les 5 grands championnats européens. 🌍📊 #DataFoot

2/ Étape 1 : Collecte des données
Nous avons à notre disposition une large base de données regroupant les performances détaillées des joueurs européens. Ces données couvrent des aspects variés comme les actions offensives, défensives, les passes, les dribbles et bien d’autres statistiques clés qui permettent d'évaluer les joueurs dans toute leur complexité.

3/ Étape 2 : Uniformisation des profils
Avant d’analyser, il est nécessaire de filtrer les joueurs qui occupent des positions similaires à celle de Mbappé, pour s'assurer que nous comparons les bons profils. Cela nous permet de concentrer notre analyse sur les attaquants ou les joueurs qui ont un rôle proche de celui de Mbappé, afin d’obtenir des résultats cohérents.

4/ Étape 3 : Standardisation des données
Pour rendre les données comparables, nous procédons à une standardisation. En effet, certaines statistiques (comme les buts) sont mesurées différemment que d’autres (comme les interceptions). Cette étape assure que toutes les variables ont le même poids dans l’analyse, en éliminant les biais dus aux unités de mesure.

5/ Étape 4 : L'Analyse en Composantes Principales (ACP)
L'ACP est une méthode statistique qui permet de simplifier la complexité des données sans perdre leur richesse. Au lieu d’analyser des dizaines de statistiques séparément, l’ACP regroupe ces informations en un petit nombre de composantes principales. Ces composantes capturent l’essentiel des variations entre les joueurs.

6/ Les détails de l'ACP : L’ACP fonctionne en cherchant les axes qui maximisent la variance dans les données. Chaque axe représente une nouvelle "dimension" dans laquelle les performances des joueurs sont projetées. Pour notre analyse, deux composantes principales suffisent à résumer la plupart des caractéristiques offensives et défensives des joueurs, offrant une vision claire et simplifiée des performances de chacun.

(📷 Schéma de l'ACP avec deux composantes principales)

7/ Étape 5 : Le Clustering, ou comment regrouper les joueurs
Une fois les données simplifiées par l'ACP, nous appliquons un algorithme de clustering pour regrouper les joueurs en clusters. Le clustering nous permet de diviser les joueurs en groupes distincts, basés sur leurs similarités statistiques. Cela facilite l’identification de profils de joueurs comparables.

8/ Les détails du Clustering : Le clustering, ici réalisé avec l'algorithme K-Means, cherche à minimiser la distance entre les joueurs d'un même cluster, tout en maximisant la distance entre les clusters différents. Chaque joueur est ainsi placé dans le groupe qui lui correspond le mieux, en fonction de son style de jeu global.

(📷 Schéma des clusters de joueurs)

9/ Étape 6 : Identifier le cluster de Mbappé
Grâce au clustering, nous identifions le cluster auquel appartient Mbappé. Ce groupe regroupe des joueurs ayant un impact offensif majeur, capables de créer des opportunités, marquer des buts, et influencer les phases de transition. C’est au sein de ce cluster que nous allons chercher son remplaçant idéal.

10/ Étape 7 : Mesurer la proximité avec Mbappé
Pour évaluer qui est le joueur le plus proche de Mbappé, nous calculons la distance entre lui et les autres membres de son cluster. Cette distance est un indicateur de similarité : plus elle est faible, plus le joueur partage des caractéristiques communes avec Mbappé.

11/ Résultats : Les joueurs les plus proches
Après avoir calculé les distances, voici les joueurs qui se rapprochent le plus de Mbappé, en termes de style de jeu et de performances statistiques :

    1️⃣ João Félix
    2️⃣ Marcus Rashford
    3️⃣ Leroy Sané
    4️⃣ Vinícius Júnior
    5️⃣ Jadon Sancho

Ces joueurs partagent des qualités offensives et un style de jeu dynamique similaire à celui de Mbappé.

12/ Étape 8 : L’interprétation des résultats pour le PSG
Grâce à cette analyse, le PSG peut identifier des joueurs qui non seulement ont des statistiques similaires à Mbappé, mais qui pourraient également s’intégrer dans leur schéma de jeu. Cette approche, guidée par les données, permet d’optimiser le processus de recrutement, en basant les décisions sur des faits objectifs.

13/ Conclusion : L’impact du Clustering et de l'ACP dans le football
L’utilisation conjointe de l’ACP et du clustering dans l’analyse des données footballistiques permet d’aller bien au-delà de l’observation traditionnelle. Ces méthodes nous offrent une perspective objective et précise sur les performances des joueurs, et ouvrent la voie à une prise de décision éclairée dans des situations aussi complexes que le remplacement de Mbappé.