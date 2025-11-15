"""
Exemple 4 : Filtrer les documents par période de publication
=============================================================

Ce script montre comment rechercher des documents publiés dans une période
donnée en utilisant les filtres de date de DocumentCloud.
"""

from documentcloud import DocumentCloud
from datetime import datetime, timedelta

# Initialiser le client
client = DocumentCloud()
PROJECT_ID = 219834

print("="*70)
print("Recherche par période de publication")
print("="*70)

# Exemple 1 : Documents publiés en janvier 2024
print("\n1. Documents publiés en janvier 2024")
query = f'+project:{PROJECT_ID} +status:"success" +publish_at:["2024-01-01T00:00:00Z" TO "2024-02-01T00:00:00Z"]'

results = client.documents.search(query)
print(f"   Nombre de documents : {results.count}")

# Exemple 2 : Documents publiés dans les 30 derniers jours
print("\n2. Documents publiés dans les 30 derniers jours")
query = f'+project:{PROJECT_ID} +status:"success" +publish_at:[NOW-30DAYS TO NOW]'

results = client.documents.search(query)
print(f"   Nombre de documents : {results.count}")

# Exemple 3 : Documents publiés en 2023
print("\n3. Documents publiés en 2023")
query = f'+project:{PROJECT_ID} +status:"success" +publish_at:["2023-01-01T00:00:00Z" TO "2024-01-01T00:00:00Z"]'

results = client.documents.search(query)
print(f"   Nombre de documents : {results.count}")

# Afficher quelques exemples
if results:
    print("\n   Exemples de documents :")
    for i, doc in enumerate(results[:5], 1):
        pub_date = "N/A"
        if hasattr(doc, 'data') and doc.data:
            pub_date = doc.data.get('publication_date', 'N/A')

        print(f"   {i}. {doc.title}")
        print(f"      Date : {pub_date}")

# Exemple 4 : Documents publiés avant une date spécifique
print("\n4. Documents publiés avant le 1er janvier 2023")
query = f'+project:{PROJECT_ID} +status:"success" +publish_at:[* TO "2023-01-01T00:00:00Z"]'

results = client.documents.search(query)
print(f"   Nombre de documents : {results.count}")

# Exemple 5 : Documents publiés après une date spécifique
print("\n5. Documents publiés après le 1er janvier 2024")
query = f'+project:{PROJECT_ID} +status:"success" +publish_at:["2024-01-01T00:00:00Z" TO *]'

results = client.documents.search(query)
print(f"   Nombre de documents : {results.count}")

print("\n" + "="*70)
print("Opérateurs de date DocumentCloud disponibles :")
print("="*70)
print("  NOW          : Date et heure actuelles")
print("  NOW-1DAY     : Il y a 1 jour")
print("  NOW-7DAYS    : Il y a 7 jours")
print("  NOW-1MONTH   : Il y a 1 mois")
print("  NOW-1YEAR    : Il y a 1 an")
print("  *            : N'importe quelle date")
print("  [DATE TO *]  : Après une date")
print("  [* TO DATE]  : Avant une date")
