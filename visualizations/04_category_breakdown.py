"""
Visualisation 4 : Répartition par catégorie
============================================

Ce script analyse la distribution des documents par catégorie
(Avis, Cadrage, Cas par Cas).
"""

from documentcloud import DocumentCloud
import matplotlib.pyplot as plt
from collections import Counter
import numpy as np

# Configuration matplotlib
plt.style.use('seaborn-v0_8-bright')
plt.rcParams['figure.figsize'] = (16, 10)

# Initialiser le client
client = DocumentCloud()
PROJECT_ID = 219834

print("Récupération des documents...")
query = f'+project:{PROJECT_ID} +status:"success"'
results = client.documents.search(query)

print(f"Documents trouvés : {results.count}")
print("Analyse des catégories...")

# Collecter les données
categories = []
pages_by_category = {}

for i, doc in enumerate(results[:1000]):
    if i % 100 == 0 and i > 0:
        print(f"  {i} documents analysés...")

    if hasattr(doc, 'data') and doc.data:
        category = doc.data.get('category')
        if category:
            categories.append(category)

            # Collecter le nombre de pages par catégorie
            if category not in pages_by_category:
                pages_by_category[category] = []
            if doc.pages:
                pages_by_category[category].append(doc.pages)

# Compter les occurrences
category_counts = Counter(categories)

# Créer la figure avec plusieurs visualisations
fig = plt.figure(figsize=(16, 12))
gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)

# Graphique 1 : Camembert
ax1 = fig.add_subplot(gs[0, 0])
if category_counts:
    cats, counts = zip(*category_counts.most_common())

    colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']
    explode = [0.05] * len(cats)

    wedges, texts, autotexts = ax1.pie(
        counts,
        labels=cats,
        autopct='%1.1f%%',
        colors=colors[:len(cats)],
        explode=explode,
        startangle=90,
        textprops={'fontsize': 11, 'weight': 'bold'}
    )

    for autotext in autotexts:
        autotext.set_color('white')

    ax1.set_title('Répartition par catégorie', fontsize=14, fontweight='bold')

# Graphique 2 : Diagramme en barres
ax2 = fig.add_subplot(gs[0, 1])
if category_counts:
    cats, counts = zip(*category_counts.most_common())

    bars = ax2.bar(cats, counts, color=colors[:len(cats)], alpha=0.8)
    ax2.set_ylabel('Nombre de documents', fontsize=11)
    ax2.set_title('Nombre de documents par catégorie', fontsize=14, fontweight='bold')
    ax2.grid(axis='y', alpha=0.3)

    # Ajouter les valeurs
    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', fontweight='bold')

# Graphique 3 : Distribution du nombre de pages par catégorie (boxplot)
ax3 = fig.add_subplot(gs[1, :])
if pages_by_category:
    data_to_plot = []
    labels_to_plot = []

    for cat in sorted(pages_by_category.keys()):
        if pages_by_category[cat]:
            data_to_plot.append(pages_by_category[cat])
            labels_to_plot.append(cat)

    bp = ax3.boxplot(data_to_plot, labels=labels_to_plot, patch_artist=True)

    # Colorier les boîtes
    for patch, color in zip(bp['boxes'], colors[:len(data_to_plot)]):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)

    ax3.set_ylabel('Nombre de pages', fontsize=11)
    ax3.set_title('Distribution du nombre de pages par catégorie',
                  fontsize=14, fontweight='bold')
    ax3.grid(axis='y', alpha=0.3)

# Graphique 4 : Statistiques détaillées
ax4 = fig.add_subplot(gs[2, :])
ax4.axis('off')

# Créer un tableau de statistiques
stats_data = []
headers = ['Catégorie', 'Documents', '%', 'Moy. pages', 'Min pages', 'Max pages']

total_docs = sum(category_counts.values())

for cat in sorted(category_counts.keys()):
    count = category_counts[cat]
    percentage = (count / total_docs) * 100

    if cat in pages_by_category and pages_by_category[cat]:
        pages = pages_by_category[cat]
        avg_pages = np.mean(pages)
        min_pages = min(pages)
        max_pages = max(pages)
    else:
        avg_pages = min_pages = max_pages = 0

    stats_data.append([
        cat,
        f'{count}',
        f'{percentage:.1f}%',
        f'{avg_pages:.1f}',
        f'{min_pages}',
        f'{max_pages}'
    ])

# Créer le tableau
table = ax4.table(cellText=stats_data, colLabels=headers,
                  cellLoc='center', loc='center',
                  colWidths=[0.25, 0.15, 0.1, 0.15, 0.15, 0.15])

table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 2)

# Styliser l'en-tête
for i in range(len(headers)):
    table[(0, i)].set_facecolor('#40466e')
    table[(0, i)].set_text_props(weight='bold', color='white')

# Alterner les couleurs des lignes
for i in range(1, len(stats_data) + 1):
    for j in range(len(headers)):
        if i % 2 == 0:
            table[(i, j)].set_facecolor('#f0f0f0')

ax4.set_title('Statistiques détaillées par catégorie',
              fontsize=14, fontweight='bold', pad=20)

# Sauvegarder
output_file = 'category_breakdown.png'
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"\n✓ Graphique sauvegardé : {output_file}")

# Afficher les statistiques textuelles
print("\nStatistiques par catégorie :")
print(f"  Total de documents : {total_docs}")
for cat in sorted(category_counts.keys()):
    count = category_counts[cat]
    percentage = (count / total_docs) * 100
    print(f"\n  {cat} :")
    print(f"    Documents : {count} ({percentage:.1f}%)")

    if cat in pages_by_category and pages_by_category[cat]:
        pages = pages_by_category[cat]
        print(f"    Pages (moyenne) : {np.mean(pages):.1f}")
        print(f"    Pages (min-max) : {min(pages)}-{max(pages)}")

plt.show()
