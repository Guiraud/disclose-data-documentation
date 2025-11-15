"""
Exemple 3 : Filtrer les documents par département
==================================================

Ce script montre comment rechercher des documents liés à un ou plusieurs
départements français.
"""

from documentcloud import DocumentCloud

# Initialiser le client
client = DocumentCloud()
PROJECT_ID = 219834

# Choisir un département (code à 2 chiffres)
department = "75"  # Paris

# Construire la requête avec filtre sur le département
query = f'+project:{PROJECT_ID} +status:"success" +data_departments:"{department}"'

print(f"Recherche des documents pour le département : {department}\n")
print(f"Requête : {query}\n")

# Effectuer la recherche
results = client.documents.search(query)

print(f"Nombre de documents trouvés : {results.count}\n")

# Afficher un échantillon des résultats
for i, doc in enumerate(results[:15], 1):
    print(f"{i}. {doc.title}")

    if hasattr(doc, 'data') and doc.data:
        authority = doc.data.get('authority', 'N/A')
        category = doc.data.get('category', 'N/A')
        pub_date = doc.data.get('publication_date', 'N/A')
        departments = doc.data.get('departments', [])

        print(f"   Autorité : {authority}")
        print(f"   Catégorie : {category}")
        print(f"   Date : {pub_date}")
        print(f"   Départements concernés : {', '.join(departments)}")
    print()

print("\n" + "="*70)
print("Recherche multi-départements")
print("="*70)

# Exemple de recherche sur plusieurs départements
departments_list = ["35", "56"]  # Ille-et-Vilaine et Morbihan (Bretagne)

# Pour chercher des documents touchant AU MOINS UN de ces départements
query_multi = f'+project:{PROJECT_ID} +status:"success" '
query_multi += f'(+data_departments:"{departments_list[0]}" OR +data_departments:"{departments_list[1]}")'

print(f"\nRequête multi-départements : {query_multi}")

results_multi = client.documents.search(query_multi)
print(f"Documents touchant la Bretagne (35 ou 56) : {results_multi.count}")
