"""
Visualisation 3 : Analyse par autorité environnementale
========================================================

Ce script analyse et visualise la distribution des documents par autorité
environnementale.
"""

from documentcloud import DocumentCloud
import matplotlib.pyplot as plt
from collections import Counter

# Configuration matplotlib
plt.style.use('seaborn-v0_8-pastel')
plt.rcParams['figure.figsize'] = (16, 10)

# Initialiser le client
client = DocumentCloud()
PROJECT_ID = 219834

print("Récupération des documents...")
query = f'+project:{PROJECT_ID} +status:"success"'
results = client.documents.search(query)

print(f"Documents trouvés : {results.count}")
print("Analyse des autorités...")

# Collecter les autorités
authorities = []

for i, doc in enumerate(results[:1000]):
    if i % 100 == 0 and i > 0:
        print(f"  {i} documents analysés...")

    if hasattr(doc, 'data') and doc.data:
        authority = doc.data.get('authority')
        if authority:
            authorities.append(authority)

# Compter les occurrences
authority_counts = Counter(authorities)

# Créer la visualisation
fig, ax = plt.subplots(figsize=(14, 10))

# Top 15 autorités
top_15 = authority_counts.most_common(15)
if top_15:
    auths, counts = zip(*top_15)

    # Tronquer les noms trop longs
    labels = []
    for auth in auths:
        if len(auth) > 50:
            labels.append(auth[:47] + '...')
        else:
            labels.append(auth)

    # Créer le graphique
    colors = plt.cm.tab20(range(len(labels)))
    bars = ax.barh(range(len(labels)), counts, color=colors)

    ax.set_yticks(range(len(labels)))
    ax.set_yticklabels(labels, fontsize=9)
    ax.set_xlabel('Nombre de documents', fontsize=12)
    ax.set_title('Top 15 des autorités environnementales par nombre de documents',
                 fontsize=14, fontweight='bold', pad=20)
    ax.invert_yaxis()

    # Ajouter les valeurs
    for i, count in enumerate(counts):
        ax.text(count, i, f' {count}', va='center', fontweight='bold')

    # Ajouter une grille
    ax.grid(axis='x', alpha=0.3)

plt.tight_layout()

# Sauvegarder
output_file = 'authority_distribution.png'
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"\n✓ Graphique sauvegardé : {output_file}")

# Afficher les statistiques
print("\nStatistiques par autorité :")
print(f"  Nombre d'autorités différentes : {len(authority_counts)}")
print(f"  Total de documents : {sum(authority_counts.values())}")
print(f"\nTop 10 autorités :")
for i, (auth, count) in enumerate(authority_counts.most_common(10), 1):
    percentage = (count / sum(authority_counts.values())) * 100
    print(f"  {i:2d}. {auth[:60]:<60s} : {count:4d} ({percentage:5.2f}%)")

plt.show()
