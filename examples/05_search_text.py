"""
Exemple 5 : Recherche textuelle dans les documents
===================================================

Ce script montre comment rechercher des documents contenant des mots-clés
spécifiques dans leur contenu ou leur titre.
"""

from documentcloud import DocumentCloud

# Initialiser le client
client = DocumentCloud()
PROJECT_ID = 219834

print("="*70)
print("Recherche textuelle dans les documents")
print("="*70)

# Exemple 1 : Recherche d'un mot-clé simple
keyword = "lithium"
query = f'+project:{PROJECT_ID} +status:"success" {keyword}'

print(f"\n1. Recherche du mot-clé : '{keyword}'")
results = client.documents.search(query)
print(f"   Nombre de documents trouvés : {results.count}")

# Afficher quelques résultats
if results:
    print("\n   Exemples de documents contenant 'lithium' :")
    for i, doc in enumerate(results[:5], 1):
        print(f"   {i}. {doc.title}")
        if hasattr(doc, 'data') and doc.data:
            authority = doc.data.get('authority', 'N/A')
            pub_date = doc.data.get('publication_date', 'N/A')
            print(f"      Autorité : {authority}")
            print(f"      Date : {pub_date}")
        print()

# Exemple 2 : Recherche dans le titre du dossier uniquement
print("\n2. Recherche de 'lithium' dans le titre du dossier uniquement")
query = f'+project:{PROJECT_ID} +status:"success" description:{keyword}'

results = client.documents.search(query)
print(f"   Nombre de dossiers trouvés : {results.count}")

# Exemple 3 : Recherche avec plusieurs mots-clés (ET logique)
print("\n3. Recherche avec plusieurs mots-clés : 'éolien' ET 'parc'")
query = f'+project:{PROJECT_ID} +status:"success" éolien parc'

results = client.documents.search(query)
print(f"   Nombre de documents trouvés : {results.count}")

# Exemple 4 : Recherche avec OU logique
print("\n4. Recherche avec OU logique : 'éolien' OU 'solaire'")
query = f'+project:{PROJECT_ID} +status:"success" (éolien OR solaire)'

results = client.documents.search(query)
print(f"   Nombre de documents trouvés : {results.count}")

# Exemple 5 : Recherche d'une expression exacte
print("\n5. Recherche d'expression exacte : \"parc éolien\"")
query = f'+project:{PROJECT_ID} +status:"success" "parc éolien"'

results = client.documents.search(query)
print(f"   Nombre de documents trouvés : {results.count}")

# Exemple 6 : Combinaison recherche textuelle + filtre
print("\n6. Recherche combinée : 'éolien' dans les documents de Bretagne")
query = f'+project:{PROJECT_ID} +status:"success" éolien +data_authority:"Préfecture de région Bretagne"'

results = client.documents.search(query)
print(f"   Nombre de documents trouvés : {results.count}")

print("\n" + "="*70)
print("Astuces pour la recherche textuelle :")
print("="*70)
print("  mot1 mot2        : Documents contenant mot1 ET mot2")
print("  mot1 OR mot2     : Documents contenant mot1 OU mot2")
print("  \"expression\"     : Recherche d'expression exacte")
print("  -mot             : Exclure un mot")
print("  description:mot  : Chercher dans le titre du dossier uniquement")
