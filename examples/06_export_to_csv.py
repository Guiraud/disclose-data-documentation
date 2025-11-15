"""
Exemple 6 : Exporter les résultats de recherche en CSV
=======================================================

Ce script montre comment exporter les métadonnées des documents vers un
fichier CSV pour analyse ultérieure.
"""

from documentcloud import DocumentCloud
import csv
import json

# Initialiser le client
client = DocumentCloud()
PROJECT_ID = 219834

# Exemple de requête : documents sur l'éolien
query = f'+project:{PROJECT_ID} +status:"success" éolien'

print(f"Requête : {query}")
print("Récupération des documents...")

results = client.documents.search(query)
print(f"Nombre de documents trouvés : {results.count}")

# Nom du fichier de sortie
output_file = "documents_eolien.csv"

# Définir les champs à exporter
fields = [
    'id',
    'title',
    'pages',
    'canonical_url',
    'publish_at',
    'description',  # Nom du dossier
    'authority',
    'category',
    'departments',
    'publication_date',
    'source_page_url',
    'source_file_url'
]

# Créer le fichier CSV
print(f"\nExport vers {output_file}...")

with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fields)

    # Écrire l'en-tête
    writer.writeheader()

    # Écrire les données (limité à 100 pour l'exemple)
    count = 0
    for doc in results[:100]:
        row = {
            'id': doc.id,
            'title': doc.title,
            'pages': doc.pages,
            'canonical_url': doc.canonical_url,
            'publish_at': doc.publish_at,
            'description': getattr(doc, 'description', ''),
        }

        # Ajouter les métadonnées personnalisées
        if hasattr(doc, 'data') and doc.data:
            row['authority'] = doc.data.get('authority', '')
            row['category'] = doc.data.get('category', '')
            # Les départements sont une liste, on les joint avec des virgules
            departments = doc.data.get('departments', [])
            row['departments'] = ', '.join(departments) if departments else ''
            row['publication_date'] = doc.data.get('publication_date', '')
            row['source_page_url'] = doc.data.get('source_page_url', '')
            row['source_file_url'] = doc.data.get('source_file_url', '')
        else:
            row['authority'] = ''
            row['category'] = ''
            row['departments'] = ''
            row['publication_date'] = ''
            row['source_page_url'] = ''
            row['source_file_url'] = ''

        writer.writerow(row)
        count += 1

print(f"Export terminé : {count} documents exportés dans {output_file}")

# Exemple d'export avec pandas (plus puissant pour l'analyse)
print("\n" + "="*70)
print("Export avec pandas (pour analyse de données)")
print("="*70)

try:
    import pandas as pd

    # Créer une liste de dictionnaires
    data = []
    for doc in results[:100]:
        record = {
            'id': doc.id,
            'title': doc.title,
            'pages': doc.pages,
            'url': doc.canonical_url,
            'publish_at': doc.publish_at,
            'dossier': getattr(doc, 'description', ''),
        }

        if hasattr(doc, 'data') and doc.data:
            record.update({
                'authority': doc.data.get('authority', ''),
                'category': doc.data.get('category', ''),
                'departments': ', '.join(doc.data.get('departments', [])),
                'publication_date': doc.data.get('publication_date', ''),
            })

        data.append(record)

    # Créer un DataFrame
    df = pd.DataFrame(data)

    # Exporter en CSV
    pandas_output = "documents_eolien_pandas.csv"
    df.to_csv(pandas_output, index=False, encoding='utf-8')

    print(f"Export pandas terminé : {pandas_output}")

    # Afficher quelques statistiques
    print("\nStatistiques :")
    print(f"  Nombre total de documents : {len(df)}")
    print(f"  Nombre moyen de pages : {df['pages'].mean():.1f}")

    if 'category' in df.columns:
        print(f"\n  Répartition par catégorie :")
        category_counts = df['category'].value_counts()
        for cat, count in category_counts.items():
            print(f"    - {cat}: {count}")

except ImportError:
    print("pandas n'est pas installé. Installez-le avec : pip install pandas")
