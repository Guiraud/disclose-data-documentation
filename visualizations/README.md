# Visualisations de données Disclose Data

Ce dossier contient des scripts pour créer des visualisations et analyses graphiques de la collection Disclose Data.

## Prérequis

Installez les dépendances nécessaires :

```bash
pip install -r ../requirements.txt
```

Les bibliothèques de visualisation requises sont :
- `matplotlib` : Création de graphiques
- `seaborn` : Visualisations statistiques avancées
- `pandas` : Manipulation et analyse de données

## Scripts de visualisation

### 01_timeline_visualization.py

**Évolution temporelle des publications**

Crée des graphiques montrant l'évolution du nombre de documents publiés au fil du temps.

**Visualisations créées :**
- Nombre de documents par année (graphique en barres)
- Évolution mensuelle sur les 24 derniers mois (graphique en ligne)

**Exécution :**
```bash
python 01_timeline_visualization.py
```

**Sortie :** `timeline_evolution.png`

---

### 02_geographic_distribution.py

**Distribution géographique**

Analyse la répartition des documents par département français.

**Visualisations créées :**
- Top 20 des départements (graphique en barres horizontales)
- Répartition des documents Top 10 (camembert)

**Exécution :**
```bash
python 02_geographic_distribution.py
```

**Sortie :** `geographic_distribution.png`

---

### 03_authority_analysis.py

**Analyse par autorité environnementale**

Visualise la distribution des documents par autorité environnementale.

**Visualisations créées :**
- Top 15 des autorités par nombre de documents (barres horizontales)
- Statistiques détaillées

**Exécution :**
```bash
python 03_authority_analysis.py
```

**Sortie :** `authority_distribution.png`

---

### 04_category_breakdown.py

**Répartition par catégorie**

Analyse détaillée de la distribution par catégorie (Avis, Cadrage, Cas par Cas).

**Visualisations créées :**
- Camembert de répartition
- Graphique en barres
- Distribution du nombre de pages par catégorie (boxplot)
- Tableau de statistiques détaillées

**Exécution :**
```bash
python 04_category_breakdown.py
```

**Sortie :** `category_breakdown.png`

---

### 05_comprehensive_dashboard.py

**Tableau de bord complet**

Crée un tableau de bord avec une vue d'ensemble complète de la collection.

**Visualisations créées :**
- Statistiques générales
- Top 5 autorités
- Répartition par catégorie
- Évolution temporelle
- Top 10 départements
- Distribution du nombre de pages
- Informations complémentaires

**Exécution :**
```bash
python 05_comprehensive_dashboard.py
```

**Sortie :** `comprehensive_dashboard.png`

---

## Personnalisation

### Modifier le nombre de documents analysés

Par défaut, les scripts analysent les 1000 premiers documents pour des raisons de performance. Pour modifier ce nombre :

```python
for i, doc in enumerate(results[:1000]):  # Changez 1000
```

### Changer les couleurs

Modifiez le style matplotlib au début du script :

```python
plt.style.use('seaborn-v0_8-darkgrid')  # Essayez : ggplot, fivethirtyeight, etc.
```

### Ajuster la taille des graphiques

```python
plt.rcParams['figure.figsize'] = (16, 10)  # Largeur, Hauteur en pouces
```

### Modifier la résolution d'export

```python
plt.savefig(output_file, dpi=300)  # Changez 300 (plus élevé = meilleure qualité)
```

## Exemples d'utilisation avancée

### Créer une visualisation pour une région spécifique

```python
from documentcloud import DocumentCloud
import matplotlib.pyplot as plt

client = DocumentCloud()
PROJECT_ID = 219834

# Filtrer par région (exemple : Bretagne)
query = f'+project:{PROJECT_ID} +status:"success" +data_authority:"Préfecture de région Bretagne"'
results = client.documents.search(query)

# Créer vos visualisations...
```

### Combiner plusieurs filtres

```python
# Documents éoliens en Bretagne en 2024
query = f'''
+project:{PROJECT_ID}
+status:"success"
éolien
+data_authority:"Préfecture de région Bretagne"
+publish_at:["2024-01-01T00:00:00Z" TO "2024-12-31T23:59:59Z"]
'''.replace('\n', ' ')
```

### Exporter en différents formats

```python
# PNG (par défaut)
plt.savefig('graph.png', dpi=300, bbox_inches='tight')

# PDF (vectoriel, bonne qualité)
plt.savefig('graph.pdf', bbox_inches='tight')

# SVG (vectoriel, pour le web)
plt.savefig('graph.svg', bbox_inches='tight')

# JPG (plus petit, avec perte)
plt.savefig('graph.jpg', dpi=300, quality=95, bbox_inches='tight')
```

## Styles matplotlib disponibles

Essayez différents styles pour personnaliser vos graphiques :

```python
# Voir tous les styles disponibles
print(plt.style.available)

# Styles populaires
plt.style.use('seaborn-v0_8-darkgrid')   # Fond gris avec grille
plt.style.use('ggplot')                   # Style ggplot (R)
plt.style.use('fivethirtyeight')          # Style FiveThirtyEight
plt.style.use('bmh')                      # Bayesian Methods for Hackers
plt.style.use('classic')                  # Style matplotlib classique
```

## Conseils

1. **Performance** : Limitez le nombre de documents analysés (par défaut 1000) pour des résultats rapides

2. **Qualité** : Pour des publications, utilisez `dpi=300` ou plus

3. **Interactivité** : Utilisez `plt.show()` pour afficher les graphiques de manière interactive

4. **Automatisation** : Créez un script qui génère tous les graphiques en une fois :

```bash
#!/bin/bash
python 01_timeline_visualization.py
python 02_geographic_distribution.py
python 03_authority_analysis.py
python 04_category_breakdown.py
python 05_comprehensive_dashboard.py
```

## Dépannage

### Erreur : "ModuleNotFoundError: No module named 'matplotlib'"

```bash
pip install matplotlib seaborn
```

### Erreur : "UserWarning: Matplotlib is currently using agg"

Sur certains systèmes sans interface graphique, ajoutez au début du script :

```python
import matplotlib
matplotlib.use('Agg')  # Backend sans affichage
```

### Les graphiques ne s'affichent pas

Assurez-vous que `plt.show()` est appelé à la fin du script.

## Ressources

- [Documentation Matplotlib](https://matplotlib.org/)
- [Galerie Matplotlib](https://matplotlib.org/stable/gallery/index.html)
- [Documentation Seaborn](https://seaborn.pydata.org/)
- [Guide des couleurs](https://matplotlib.org/stable/tutorials/colors/colormaps.html)

## Support

Pour plus d'informations, consultez la [documentation principale](../README.md) ou contactez data@disclose.ngo
