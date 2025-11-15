"""
Exemple 1 : Recherche basique de documents
===========================================

Ce script montre comment effectuer une recherche simple dans la collection
Disclose Data et afficher les résultats.
"""

from documentcloud import DocumentCloud

# Initialiser le client DocumentCloud
client = DocumentCloud()

# ID du projet Disclose Data
PROJECT_ID = 219834

# Recherche basique : tous les documents avec status "success"
query = f"+project:{PROJECT_ID} +status:\"success\""

print(f"Requête : {query}\n")

# Effectuer la recherche (limité à 10 résultats pour l'exemple)
results = client.documents.search(query)

print(f"Nombre total de documents : {results.count}")
print(f"\nPremiers 10 résultats :\n")

# Afficher les 10 premiers résultats
for i, doc in enumerate(results[:10], 1):
    print(f"{i}. {doc.title}")
    print(f"   URL : {doc.canonical_url}")
    print(f"   Pages : {doc.pages}")
    print(f"   Date de publication : {doc.publish_at}")
    print()

# Exemple d'accès aux métadonnées personnalisées
print("\nExemple de métadonnées pour le premier document :")
if results:
    first_doc = results[0]
    print(f"Titre : {first_doc.title}")

    # Les métadonnées personnalisées sont dans first_doc.data
    if hasattr(first_doc, 'data') and first_doc.data:
        print(f"Autorité : {first_doc.data.get('authority', 'N/A')}")
        print(f"Catégorie : {first_doc.data.get('category', 'N/A')}")
        print(f"Départements : {first_doc.data.get('departments', 'N/A')}")
        print(f"Date de publication : {first_doc.data.get('publication_date', 'N/A')}")
