# Bot Clash Royale - Code Explanation

## Configuration
### Adapting to Screen Dimensions
Avant de commencer à utiliser le bot, tu dois adapter les coordonnées aux dimensions de l'écran de ton téléphone pour optimiser le placement des cartes. Modifie les variables suivantes dans le code selon la taille et la résolution de ton écran :

```python
y_nilieu = 350  # Coordonnée Y pour le milieu du terrain
x_gauche = 90   # Coordonnée X pour le côté gauche du terrain
x_droit = 340   # Coordonnée X pour le côté droit du terrain
y_tour = 400    # Coordonnée Y pour la position de la tour
y_fin = 600     # Coordonnée Y pour la fin du terrain
```

Ces ajustements sont cruciaux pour que le bot fonctionne correctement et effectue des placements précis de cartes.

## Details of the Code

### Class: `bot`
- **Purpose**: T'aider à automatiser les décisions en fonction de l'état de la partie.
- **Methods**:
  - `__init__`: Initialise les dictionnaires d'état internes `A` et `E`.
  - `get_action(state)`: Méthode principale qui analyse l'état du jeu et décide de l'action à prendre, utilisant plusieurs sous-fonctions pour des décisions spécifiques.

### Key Functions and Decision Processes:

- **`tank_adc(cartes_jouables)`**:
  - Détermine la meilleure carte à jouer, en évaluant les cartes en termes de rôle défensif (`tank`) et offensif (`adc`).
  - Retourne les indices des cartes à jouer en fonction de leur efficacité calculée.

- **`poser(i, position)`**:
  - Exécute l'action de poser une carte sur le terrain.
  - Gère l'historique des positions des cartes jouées.

- **`position_relative(v, largeur, hauteur)`**:
  - Calcule la position relative sur le champ de bataille pour optimiser le placement des troupes.

- **Strategic Use of Numpy Arrays**:
  - Gère les statistiques du champ de bataille telles que DPS et points de vie dans des matrices numpy pour des décisions rapides et efficaces.

- **Decision Making Based on Game State**:
  - Analyse l'état actuel du jeu pour faire des choix stratégiques entre attaque et défense.
  - Utilise des ratios de défense à l'attaque pour choisir entre renforcer la défense ou augmenter la pression offensive.

### Game State Analysis:
- La méthode `get_action` décompose l'état du jeu en éléments utilisables pour prendre des décisions en fonction de la disponibilité de l'élixir, de l'état des tours, de la présence de cartes spécifiques, etc.

## Logic Flow:
1. **Initial State Check**: Vérifie si le bot est dans un état de jeu valide.
2. **Data Extraction**: Extrait des informations telles que les cartes jouables et l'état des tours.
3. **Strategic Decisions**: Détermine si le bot doit défendre ou attaquer en fonction des calculs des DPS et des points de vie sur le champ de bataille.
4. **Action Execution**: Choisit et exécute l'action de poser une carte sur le terrain.
