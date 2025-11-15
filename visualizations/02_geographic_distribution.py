"""
Visualisation 2 : Distribution géographique
============================================

Ce script crée des visualisations montrant la répartition des documents
par département.
"""

from documentcloud import DocumentCloud
import matplotlib.pyplot as plt
from collections import Counter

# Configuration matplotlib
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['figure.figsize'] = (16, 10)

# Initialiser le client
client = DocumentCloud()
PROJECT_ID = 219834

print("Récupération des documents...")
query = f'+project:{PROJECT_ID} +status:"success"'
results = client.documents.search(query)

print(f"Documents trouvés : {results.count}")
print("Analyse des départements...")

# Collecter les départements
departments = []

for i, doc in enumerate(results[:1000]):
    if i % 100 == 0 and i > 0:
        print(f"  {i} documents analysés...")

    if hasattr(doc, 'data') and doc.data:
        doc_departments = doc.data.get('departments', [])
        departments.extend(doc_departments)

# Compter les occurrences
dept_counts = Counter(departments)

# Créer la figure avec deux visualisations
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8))

# Graphique 1 : Top 20 départements (bar chart)
top_20 = dept_counts.most_common(20)
if top_20:
    depts, counts = zip(*top_20)

    colors = plt.cm.viridis(range(len(depts)))
    bars = ax1.barh(range(len(depts)), counts, color=colors)

    ax1.set_yticks(range(len(depts)))
    ax1.set_yticklabels([f"Département {d}" for d in depts])
    ax1.set_xlabel('Nombre de documents')
    ax1.set_title('Top 20 des départements les plus concernés',
                  fontsize=14, fontweight='bold')
    ax1.invert_yaxis()

    # Ajouter les valeurs
    for i, (dept, count) in enumerate(top_20):
        ax1.text(count, i, f' {count}', va='center')

# Graphique 2 : Camembert des top 10
top_10 = dept_counts.most_common(10)
if top_10:
    depts, counts = zip(*top_10)

    # Ajouter "Autres" si nécessaire
    total = sum(dept_counts.values())
    top_10_total = sum(counts)
    if top_10_total < total:
        depts = list(depts) + ['Autres']
        counts = list(counts) + [total - top_10_total]

    colors = plt.cm.Set3(range(len(depts)))

    wedges, texts, autotexts = ax2.pie(
        counts,
        labels=[f"Dept. {d}" for d in depts],
        autopct='%1.1f%%',
        colors=colors,
        startangle=90
    )

    ax2.set_title('Répartition des documents (Top 10)',
                  fontsize=14, fontweight='bold')

    # Améliorer la lisibilité
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')

plt.tight_layout()

# Sauvegarder
output_file = 'geographic_distribution.png'
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"\n✓ Graphique sauvegardé : {output_file}")

# Afficher les statistiques
print("\nStatistiques géographiques :")
print(f"  Nombre total de départements concernés : {len(dept_counts)}")
print(f"  Total d'occurrences : {sum(dept_counts.values())}")
print(f"\nTop 10 départements :")
for i, (dept, count) in enumerate(dept_counts.most_common(10), 1):
    print(f"  {i:2d}. Département {dept:3s} : {count:4d} documents")

plt.show()
