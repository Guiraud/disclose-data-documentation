# Exemples d'utilisation de l'API Disclose Data

Ce dossier contient des exemples de code Python pour interroger la collection de documents Disclose Data via l'API DocumentCloud.

## Prérequis

Installez les dépendances requises :

```bash
pip install -r ../requirements.txt
```

## Liste des exemples

### 01_basic_search.py
Recherche basique de documents et affichage des résultats.

**Concepts couverts :**
- Initialisation du client DocumentCloud
- Recherche simple
- Accès aux métadonnées personnalisées

**Exécution :**
```bash
python 01_basic_search.py
```

### 02_filter_by_authority.py
Filtrer les documents par autorité environnementale.

**Concepts couverts :**
- Filtrage par métadonnée `data_authority`
- Affichage des informations détaillées

**Exécution :**
```bash
python 02_filter_by_authority.py
```

### 03_filter_by_department.py
Filtrer les documents par département français.

**Concepts couverts :**
- Filtrage par métadonnée `data_departments`
- Recherche multi-départements avec opérateur OR

**Exécution :**
```bash
python 03_filter_by_department.py
```

### 04_filter_by_date.py
Filtrer les documents par période de publication.

**Concepts couverts :**
- Utilisation des opérateurs de date DocumentCloud
- Recherche par plage de dates
- Opérateurs relatifs (NOW-30DAYS, etc.)

**Exécution :**
```bash
python 04_filter_by_date.py
```

### 05_search_text.py
Recherche textuelle dans les documents.

**Concepts couverts :**
- Recherche de mots-clés
- Opérateurs logiques (AND, OR)
- Recherche d'expressions exactes
- Combinaison recherche textuelle + filtres

**Exécution :**
```bash
python 05_search_text.py
```

### 06_export_to_csv.py
Exporter les résultats de recherche en CSV.

**Concepts couverts :**
- Export CSV avec le module `csv`
- Export avec pandas pour analyse de données
- Extraction de statistiques

**Exécution :**
```bash
python 06_export_to_csv.py
```

## Personnalisation

Vous pouvez facilement adapter ces exemples en modifiant :
- Les requêtes de recherche
- Les filtres (autorité, département, dates)
- Les champs exportés dans les CSV
- Le nombre de résultats affichés

## Ressources

- [Documentation API DocumentCloud](https://www.documentcloud.org/help/api/)
- [Documentation python-documentcloud](https://documentcloud.readthedocs.io/)
- [Documentation principale du projet](../README.md)
