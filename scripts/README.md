# Scripts utilitaires Disclose Data

Ce dossier contient des scripts prêts à l'emploi pour interroger et analyser la collection Disclose Data.

## Installation

Installez d'abord les dépendances :

```bash
pip install -r ../requirements.txt
```

## Scripts disponibles

### 🔍 search_documents.py

Rechercher des documents avec différents filtres.

**Usage :**
```bash
python search_documents.py [OPTIONS]
```

**Options :**
- `-k, --keyword` : Mot-clé à rechercher
- `-a, --authority` : Filtrer par autorité environnementale
- `-d, --department` : Filtrer par code département
- `-c, --category` : Filtrer par catégorie (Avis, Cadrage, Cas par Cas)
- `--from-date` : Date de début (YYYY-MM-DD)
- `--to-date` : Date de fin (YYYY-MM-DD)
- `-l, --limit` : Nombre de résultats à afficher (défaut: 50)

**Exemples :**
```bash
# Rechercher des documents sur l'éolien
python search_documents.py --keyword éolien

# Documents de Bretagne
python search_documents.py --authority "Préfecture de région Bretagne"

# Documents sur Paris
python search_documents.py --department 75

# Documents de 2024
python search_documents.py --from-date 2024-01-01 --to-date 2024-12-31

# Recherche combinée
python search_documents.py --keyword lithium --department 973
```

---

### 📊 export_data.py

Exporter des documents vers un fichier CSV pour analyse.

**Usage :**
```bash
python export_data.py [OPTIONS] -o output.csv
```

**Options :**
- `-o, --output` : Fichier CSV de sortie (requis)
- `-k, --keyword` : Mot-clé à rechercher
- `-a, --authority` : Filtrer par autorité
- `-d, --department` : Filtrer par département
- `-c, --category` : Filtrer par catégorie
- `--from-date` : Date de début
- `--to-date` : Date de fin
- `--max-results` : Nombre max de documents (défaut: 1000)

**Exemples :**
```bash
# Exporter tous les documents sur l'éolien
python export_data.py --keyword éolien -o eolien.csv

# Exporter les documents de Paris
python export_data.py --department 75 -o paris.csv

# Exporter les documents de 2024
python export_data.py --from-date 2024-01-01 --to-date 2024-12-31 -o 2024.csv

# Export avec limite
python export_data.py --keyword solaire -o solaire.csv --max-results 500
```

---

### 📈 get_statistics.py

Obtenir des statistiques détaillées sur la collection.

**Usage :**
```bash
python get_statistics.py [OPTIONS]
```

**Options :**
- `-d, --department` : Limiter à un département
- `-y, --year` : Limiter à une année

**Statistiques fournies :**
- Nombre total de documents
- Pages totales et moyenne par document
- Top 10 des autorités environnementales
- Répartition par catégorie
- Top 15 des départements concernés
- Évolution temporelle par année
- Documents les plus récents

**Exemples :**
```bash
# Statistiques globales
python get_statistics.py

# Statistiques pour Paris
python get_statistics.py --department 75

# Statistiques pour 2024
python get_statistics.py --year 2024
```

---

### 🔔 monitor_new_documents.py

Surveiller les nouveaux documents ajoutés récemment.

**Usage :**
```bash
python monitor_new_documents.py [OPTIONS]
```

**Options :**
- `--days` : Nombre de jours à surveiller (défaut: 7)
- `-k, --keyword` : Filtrer par mot-clé
- `-d, --department` : Filtrer par département
- `-a, --authority` : Filtrer par autorité

**Exemples :**
```bash
# Nouveaux documents des 7 derniers jours
python monitor_new_documents.py

# Nouveaux documents du dernier mois
python monitor_new_documents.py --days 30

# Nouveaux documents sur l'éolien
python monitor_new_documents.py --days 14 --keyword éolien

# Nouveaux documents de Bretagne
python monitor_new_documents.py --days 7 --authority "Préfecture de région Bretagne"
```

---

## Automatisation

### Surveillance quotidienne

Créez un script pour recevoir un rapport quotidien :

```bash
#!/bin/bash
# daily_report.sh

python monitor_new_documents.py --days 1 > rapport_$(date +%Y-%m-%d).txt
```

Ajoutez à votre crontab pour exécution quotidienne :
```
0 9 * * * /path/to/daily_report.sh
```

### Export mensuel

```bash
#!/bin/bash
# monthly_export.sh

YEAR=$(date +%Y)
MONTH=$(date +%m)

python export_data.py \
  --from-date "${YEAR}-${MONTH}-01" \
  --to-date "${YEAR}-${MONTH}-31" \
  -o "export_${YEAR}_${MONTH}.csv"
```

## Conseils d'utilisation

1. **Performance** : Pour de grandes requêtes, utilisez `--max-results` pour limiter le nombre de documents traités

2. **Filtres multiples** : Combinez plusieurs filtres pour des recherches précises

3. **Export régulier** : Planifiez des exports réguliers pour suivre l'évolution de la collection

4. **Analyse** : Importez les CSV dans Excel, Google Sheets, ou pandas pour des analyses approfondies

## Support

Pour plus d'informations, consultez la [documentation principale](../README.md) ou contactez data@disclose.ngo
