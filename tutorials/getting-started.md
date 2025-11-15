# Tutoriel : Débuter avec l'API Disclose Data

Bienvenue ! Ce tutoriel vous guidera pas à pas pour utiliser l'API Disclose Data et interroger la collection de documents des autorités environnementales françaises.

## Table des matières

1. [Prérequis](#prérequis)
2. [Installation](#installation)
3. [Premier pas : recherche simple](#premier-pas--recherche-simple)
4. [Filtrer les résultats](#filtrer-les-résultats)
5. [Accéder aux métadonnées](#accéder-aux-métadonnées)
6. [Recherche avancée](#recherche-avancée)
7. [Exporter les données](#exporter-les-données)
8. [Aller plus loin](#aller-plus-loin)

---

## Prérequis

Avant de commencer, assurez-vous d'avoir :

- **Python 3.7 ou supérieur** installé sur votre ordinateur
- Des connaissances de base en Python
- Une connexion Internet

### Vérifier votre installation Python

Ouvrez un terminal et tapez :

```bash
python --version
```

ou

```bash
python3 --version
```

Vous devriez voir quelque chose comme `Python 3.9.7` ou une version supérieure.

---

## Installation

### Méthode 1 : Avec uv (recommandé - ultra rapide)

[uv](https://github.com/astral-sh/uv) est un gestionnaire de paquets Python extrêmement rapide développé par Astral.

#### Étape 1 : Installer uv

```bash
# Sur macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Sur Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

#### Étape 2 : Créer un environnement virtuel et installer les dépendances

```bash
# Créer un environnement virtuel
uv venv

# L'activer (sur macOS/Linux)
source .venv/bin/activate

# L'activer (sur Windows)
.venv\Scripts\activate

# Installer python-documentcloud
uv pip install python-documentcloud
```

Ou, si vous avez cloné ce dépôt :

```bash
uv pip install -r requirements.txt
```

#### Étape 3 : Vérifier l'installation

Créez un fichier `test.py` avec ce code :

```python
from documentcloud import DocumentCloud

print("✓ Installation réussie !")
```

Exécutez-le :

```bash
python test.py
```

Si vous voyez "✓ Installation réussie !", vous êtes prêt !

---

### Méthode 2 : Avec pip classique

Si vous préférez utiliser pip :

```bash
# Créer un environnement virtuel
python -m venv disclose-env

# L'activer (sur macOS/Linux)
source disclose-env/bin/activate

# L'activer (sur Windows)
disclose-env\Scripts\activate

# Installer les dépendances
pip install python-documentcloud

# Ou si vous avez cloné le dépôt
pip install -r requirements.txt
```

---

### Dépannage installation

#### Problème avec pyenv : "python: command not found"

Si vous utilisez `pyenv` et obtenez cette erreur avec uv :

```
error: Failed to inspect Python interpreter
pyenv: python: command not found
```

**Solution 1 : Spécifier python3**
```bash
uv pip install --python python3 python-documentcloud
```

**Solution 2 : Configurer pyenv global**
```bash
# Voir les versions disponibles
pyenv versions

# Définir une version par défaut (remplacez 3.12.4 par votre version)
pyenv global 3.12.4

# Vérifier
python --version
```

**Solution 3 : Créer un environnement virtuel d'abord**
```bash
# uv créera automatiquement un venv avec Python détecté
uv venv

# Activer le venv
source .venv/bin/activate  # macOS/Linux
# ou
.venv\Scripts\activate  # Windows

# Installer les dépendances (dans le venv, pas de problème)
uv pip install python-documentcloud
```

---

## Premier pas : recherche simple

### Objectif

Récupérer et afficher les 10 premiers documents de la collection.

### Code

Créez un fichier `mon_premier_script.py` :

```python
from documentcloud import DocumentCloud

# 1. Initialiser le client DocumentCloud
client = DocumentCloud()

# 2. ID du projet Disclose Data
PROJECT_ID = 219834

# 3. Créer une requête simple
query = f"+project:{PROJECT_ID} +status:\"success\""

# 4. Effectuer la recherche
print("Recherche en cours...")
results = client.documents.search(query)

# 5. Afficher le nombre de résultats
print(f"\nNombre total de documents : {results.count}")

# 6. Afficher les 10 premiers documents
print("\nPremiers documents :\n")
for i, doc in enumerate(results[:10], 1):
    print(f"{i}. {doc.title}")
    print(f"   URL : {doc.canonical_url}")
    print()
```

### Exécution

```bash
python mon_premier_script.py
```

### Explications

- `DocumentCloud()` : Crée un client pour communiquer avec l'API
- `PROJECT_ID = 219834` : L'identifiant du projet Disclose Data sur DocumentCloud
- `+project:219834` : Filtre pour ne chercher que dans ce projet
- `+status:"success"` : Filtre pour n'avoir que les documents correctement importés
- `results.count` : Le nombre total de documents trouvés
- `results[:10]` : Les 10 premiers résultats

---

## Filtrer les résultats

### Par autorité environnementale

```python
from documentcloud import DocumentCloud

client = DocumentCloud()
PROJECT_ID = 219834

# Chercher les documents de Bretagne
authority = "Préfecture de région Bretagne"
query = f'+project:{PROJECT_ID} +status:"success" +data_authority:"{authority}"'

results = client.documents.search(query)

print(f"Documents de {authority} : {results.count}")

for doc in results[:5]:
    print(f"- {doc.title}")
```

### Par département

```python
from documentcloud import DocumentCloud

client = DocumentCloud()
PROJECT_ID = 219834

# Chercher les documents concernant Paris (75)
department = "75"
query = f'+project:{PROJECT_ID} +status:"success" +data_departments:"{department}"'

results = client.documents.search(query)

print(f"Documents concernant le département {department} : {results.count}")

for doc in results[:5]:
    print(f"- {doc.title}")
```

### Par catégorie

```python
from documentcloud import DocumentCloud

client = DocumentCloud()
PROJECT_ID = 219834

# Chercher uniquement les "Avis"
category = "Avis"
query = f'+project:{PROJECT_ID} +status:"success" +data_category:"{category}"'

results = client.documents.search(query)

print(f"Documents de catégorie '{category}' : {results.count}")
```

---

## Accéder aux métadonnées

Chaque document possède des métadonnées riches. Voici comment y accéder :

```python
from documentcloud import DocumentCloud

client = DocumentCloud()
PROJECT_ID = 219834

query = f'+project:{PROJECT_ID} +status:"success"'
results = client.documents.search(query)

# Prendre le premier document
doc = results[0]

print(f"Titre : {doc.title}")
print(f"Pages : {doc.pages}")
print(f"URL : {doc.canonical_url}")

# Accéder aux métadonnées personnalisées
if hasattr(doc, 'data') and doc.data:
    print(f"\nMétadonnées personnalisées :")
    print(f"  Autorité : {doc.data.get('authority', 'N/A')}")
    print(f"  Catégorie : {doc.data.get('category', 'N/A')}")
    print(f"  Date de publication : {doc.data.get('publication_date', 'N/A')}")

    # Les départements sont une liste
    departments = doc.data.get('departments', [])
    if departments:
        print(f"  Départements : {', '.join(departments)}")

    print(f"  Source : {doc.data.get('source_page_url', 'N/A')}")
```

### Métadonnées disponibles

Les principales métadonnées dans `doc.data` :

- `authority` : Autorité environnementale
- `category` : Catégorie (Avis, Cadrage, Cas par Cas)
- `departments` : Liste des départements concernés
- `publication_date` : Date de publication (YYYY-MM-DD)
- `source_page_url` : URL de la page source
- `source_file_url` : URL du fichier original

---

## Recherche avancée

### Recherche textuelle

Chercher des documents contenant un mot-clé :

```python
from documentcloud import DocumentCloud

client = DocumentCloud()
PROJECT_ID = 219834

# Chercher "lithium" dans tous les documents
keyword = "lithium"
query = f'+project:{PROJECT_ID} +status:"success" {keyword}'

results = client.documents.search(query)

print(f"Documents contenant '{keyword}' : {results.count}")

for doc in results[:5]:
    print(f"- {doc.title}")
```

### Recherche par période

```python
from documentcloud import DocumentCloud

client = DocumentCloud()
PROJECT_ID = 219834

# Documents publiés en 2024
query = f'+project:{PROJECT_ID} +status:"success" +publish_at:["2024-01-01T00:00:00Z" TO "2024-12-31T23:59:59Z"]'

results = client.documents.search(query)

print(f"Documents de 2024 : {results.count}")
```

### Recherche combinée

Combinez plusieurs critères :

```python
from documentcloud import DocumentCloud

client = DocumentCloud()
PROJECT_ID = 219834

# Documents sur l'éolien, en Bretagne, en 2024
query = f'''
+project:{PROJECT_ID}
+status:"success"
éolien
+data_authority:"Préfecture de région Bretagne"
+publish_at:["2024-01-01T00:00:00Z" TO "2024-12-31T23:59:59Z"]
'''.replace('\n', ' ')

results = client.documents.search(query)

print(f"Résultats : {results.count}")

for doc in results[:10]:
    if hasattr(doc, 'data') and doc.data:
        pub_date = doc.data.get('publication_date', 'N/A')
        print(f"- {doc.title} ({pub_date})")
```

---

## Exporter les données

### Export simple en CSV

```python
from documentcloud import DocumentCloud
import csv

client = DocumentCloud()
PROJECT_ID = 219834

# Recherche
query = f'+project:{PROJECT_ID} +status:"success" éolien'
results = client.documents.search(query)

# Export CSV
with open('documents_eolien.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)

    # En-tête
    writer.writerow(['Titre', 'Autorité', 'Départements', 'Date', 'URL'])

    # Données
    for doc in results[:100]:  # Limité à 100
        authority = ''
        departments = ''
        pub_date = ''

        if hasattr(doc, 'data') and doc.data:
            authority = doc.data.get('authority', '')
            deps = doc.data.get('departments', [])
            departments = ', '.join(deps)
            pub_date = doc.data.get('publication_date', '')

        writer.writerow([
            doc.title,
            authority,
            departments,
            pub_date,
            doc.canonical_url
        ])

print("✓ Export terminé : documents_eolien.csv")
```

### Export avec pandas (pour l'analyse)

```python
from documentcloud import DocumentCloud
import pandas as pd

client = DocumentCloud()
PROJECT_ID = 219834

query = f'+project:{PROJECT_ID} +status:"success"'
results = client.documents.search(query)

# Créer une liste de dictionnaires
data = []
for doc in results[:100]:
    record = {
        'titre': doc.title,
        'pages': doc.pages,
        'url': doc.canonical_url,
    }

    if hasattr(doc, 'data') and doc.data:
        record['autorité'] = doc.data.get('authority', '')
        record['catégorie'] = doc.data.get('category', '')
        record['départements'] = ', '.join(doc.data.get('departments', []))
        record['date'] = doc.data.get('publication_date', '')

    data.append(record)

# Créer un DataFrame
df = pd.DataFrame(data)

# Exporter
df.to_csv('export_pandas.csv', index=False, encoding='utf-8')

# Afficher quelques statistiques
print(f"Documents : {len(df)}")
print(f"Moyenne pages : {df['pages'].mean():.1f}")
print(f"\nRépartition par catégorie :")
print(df['catégorie'].value_counts())
```

---

## Aller plus loin

### Exercices pratiques

**Exercice 1 : Votre région**

Modifiez le code pour chercher tous les documents concernant votre région.

**Exercice 2 : Analyse temporelle**

Créez un graphique montrant le nombre de documents publiés par mois.

**Exercice 3 : Top mots-clés**

Cherchez les documents pour différents mots-clés (éolien, solaire, lithium, etc.) et comparez les résultats.

### Ressources supplémentaires

- **Exemples de code** : Consultez le dossier [`examples/`](../examples/)
- **Scripts utilitaires** : Utilisez les scripts dans [`scripts/`](../scripts/)
- **Visualisations** : Voir [`visualizations/`](../visualizations/)
- **Documentation API** : [README principal](../README.md)
- **DocumentCloud** : [Documentation officielle](https://www.documentcloud.org/help/api/)

### Bonnes pratiques

1. **Limitez vos requêtes** : Utilisez des filtres pour ne récupérer que ce dont vous avez besoin
2. **Testez d'abord** : Commencez par des petites requêtes avant de tout exporter
3. **Gérez les erreurs** : Ajoutez des `try/except` pour gérer les problèmes de connexion
4. **Respectez l'API** : N'envoyez pas trop de requêtes simultanées

### Exemple avec gestion d'erreurs

```python
from documentcloud import DocumentCloud

try:
    client = DocumentCloud()
    results = client.documents.search('+project:219834 +status:"success"')
    print(f"✓ {results.count} documents trouvés")

except Exception as e:
    print(f"✗ Erreur : {e}")
    print("Vérifiez votre connexion Internet")
```

---

## Besoin d'aide ?

- **Email** : data@disclose.ngo
- **Documentation** : [README.md](../README.md)
- **Exemples** : Consultez les fichiers dans `examples/`

Bon code ! 🚀
