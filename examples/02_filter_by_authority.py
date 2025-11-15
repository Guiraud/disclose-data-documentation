"""
Exemple 2 : Filtrer les documents par autorité environnementale
================================================================

Ce script montre comment rechercher des documents émis par une autorité
environnementale spécifique.
"""

from documentcloud import DocumentCloud

# Initialiser le client
client = DocumentCloud()
PROJECT_ID = 219834

# Choisir une autorité environnementale
authority = "Préfecture de région Bretagne"

# Construire la requête avec filtre sur l'autorité
query = f'+project:{PROJECT_ID} +status:"success" +data_authority:"{authority}"'

print(f"Recherche des documents de : {authority}\n")
print(f"Requête : {query}\n")

# Effectuer la recherche
results = client.documents.search(query)

print(f"Nombre de documents trouvés : {results.count}\n")

# Afficher les résultats
for i, doc in enumerate(results[:20], 1):
    print(f"{i}. {doc.title}")

    # Afficher les informations de métadonnées si disponibles
    if hasattr(doc, 'data') and doc.data:
        category = doc.data.get('category', 'N/A')
        pub_date = doc.data.get('publication_date', 'N/A')
        departments = doc.data.get('departments', [])

        print(f"   Catégorie : {category}")
        print(f"   Date : {pub_date}")
        if departments:
            print(f"   Départements : {', '.join(departments)}")
    print()

# Liste des autorités disponibles
print("\n" + "="*70)
print("Exemples d'autres autorités disponibles :")
print("="*70)
authorities_examples = [
    "Préfecture de région Bretagne",
    "Préfecture de région Guyane",
    "Préfecture de région Île-de-France",
    "Conseil général de l'environnement et du développement durable",
    "Mission régionale d'autorité environnementale"
]

for auth in authorities_examples:
    print(f"  - {auth}")
