"""
Visualisation 5 : Tableau de bord complet
==========================================

Ce script crée un tableau de bord complet avec plusieurs visualisations
pour avoir une vue d'ensemble de la collection.
"""

from documentcloud import DocumentCloud
import matplotlib.pyplot as plt
from collections import Counter
import numpy as np

# Configuration matplotlib
plt.style.use('seaborn-v0_8-darkgrid')

# Initialiser le client
client = DocumentCloud()
PROJECT_ID = 219834

print("="*70)
print("CRÉATION DU TABLEAU DE BORD DISCLOSE DATA")
print("="*70)

print("\nRécupération des documents...")
query = f'+project:{PROJECT_ID} +status:"success"'
results = client.documents.search(query)

print(f"Documents trouvés : {results.count}")
print("Analyse en cours...\n")

# Collecter toutes les données
authorities = []
categories = []
departments = []
dates = []
pages_list = []

for i, doc in enumerate(results[:1000]):
    if i % 100 == 0 and i > 0:
        print(f"  {i} documents analysés...")

    # Pages
    if doc.pages:
        pages_list.append(doc.pages)

    if hasattr(doc, 'data') and doc.data:
        # Autorité
        authority = doc.data.get('authority')
        if authority:
            authorities.append(authority)

        # Catégorie
        category = doc.data.get('category')
        if category:
            categories.append(category)

        # Départements
        doc_depts = doc.data.get('departments', [])
        departments.extend(doc_depts)

        # Dates
        pub_date = doc.data.get('publication_date')
        if pub_date:
            try:
                year = pub_date.split('-')[0]
                dates.append(year)
            except:
                pass

print("\nCréation du tableau de bord...")

# Créer la figure
fig = plt.figure(figsize=(20, 12))
fig.suptitle('TABLEAU DE BORD DISCLOSE DATA - Autorités Environnementales',
             fontsize=18, fontweight='bold', y=0.98)

gs = fig.add_gridspec(3, 3, hspace=0.4, wspace=0.3)

# 1. Statistiques générales (en haut à gauche)
ax1 = fig.add_subplot(gs[0, 0])
ax1.axis('off')

stats_text = f"""
STATISTIQUES GÉNÉRALES

Documents analysés : {len(results[:1000]):,}
Total documents : {results.count:,}

Pages totales : {sum(pages_list):,}
Moyenne pages/doc : {np.mean(pages_list):.1f}

Autorités uniques : {len(set(authorities))}
Départements concernés : {len(set(departments))}
"""

ax1.text(0.1, 0.5, stats_text, fontsize=12, verticalalignment='center',
         family='monospace', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

# 2. Top 5 autorités (en haut au milieu)
ax2 = fig.add_subplot(gs[0, 1])
if authorities:
    auth_counts = Counter(authorities)
    top_5 = auth_counts.most_common(5)
    auths, counts = zip(*top_5)

    # Tronquer les noms
    labels = [a[:25] + '...' if len(a) > 25 else a for a in auths]

    ax2.barh(range(len(labels)), counts, color='steelblue')
    ax2.set_yticks(range(len(labels)))
    ax2.set_yticklabels(labels, fontsize=9)
    ax2.set_title('Top 5 Autorités', fontweight='bold')
    ax2.invert_yaxis()

    for i, count in enumerate(counts):
        ax2.text(count, i, f' {count}', va='center', fontsize=9)

# 3. Catégories (en haut à droite)
ax3 = fig.add_subplot(gs[0, 2])
if categories:
    cat_counts = Counter(categories)
    cats, counts = zip(*cat_counts.most_common())

    colors = ['#ff9999', '#66b3ff', '#99ff99']
    wedges, texts, autotexts = ax3.pie(counts, labels=cats, autopct='%1.1f%%',
                                         colors=colors[:len(cats)], startangle=90)

    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')

    ax3.set_title('Répartition par Catégorie', fontweight='bold')

# 4. Évolution temporelle (ligne du milieu, large)
ax4 = fig.add_subplot(gs[1, :])
if dates:
    date_counts = Counter(dates)
    years = sorted(date_counts.keys())
    counts = [date_counts[year] for year in years]

    ax4.plot(years, counts, marker='o', linewidth=2, markersize=8, color='coral')
    ax4.fill_between(range(len(years)), counts, alpha=0.3, color='coral')
    ax4.set_xlabel('Année')
    ax4.set_ylabel('Nombre de documents')
    ax4.set_title('Évolution temporelle des publications', fontweight='bold', fontsize=12)
    ax4.grid(alpha=0.3)
    ax4.set_xticks(range(len(years)))
    ax4.set_xticklabels(years, rotation=45)

# 5. Top 10 départements (en bas à gauche)
ax5 = fig.add_subplot(gs[2, 0])
if departments:
    dept_counts = Counter(departments)
    top_10 = dept_counts.most_common(10)
    depts, counts = zip(*top_10)

    ax5.bar(range(len(depts)), counts, color='green', alpha=0.7)
    ax5.set_xticks(range(len(depts)))
    ax5.set_xticklabels(depts, fontsize=9)
    ax5.set_ylabel('Documents')
    ax5.set_title('Top 10 Départements', fontweight='bold')
    ax5.grid(axis='y', alpha=0.3)

# 6. Distribution des pages (en bas au milieu)
ax6 = fig.add_subplot(gs[2, 1])
if pages_list:
    # Filtrer les outliers extrêmes pour une meilleure visualisation
    pages_filtered = [p for p in pages_list if p <= 200]

    ax6.hist(pages_filtered, bins=30, color='purple', alpha=0.7, edgecolor='black')
    ax6.set_xlabel('Nombre de pages')
    ax6.set_ylabel('Fréquence')
    ax6.set_title('Distribution du nombre de pages', fontweight='bold')
    ax6.axvline(np.mean(pages_list), color='red', linestyle='--',
                linewidth=2, label=f'Moyenne: {np.mean(pages_list):.1f}')
    ax6.legend()
    ax6.grid(axis='y', alpha=0.3)

# 7. Informations complémentaires (en bas à droite)
ax7 = fig.add_subplot(gs[2, 2])
ax7.axis('off')

# Top 3 de chaque catégorie
info_text = "TOP 3 PAR CATÉGORIE\n\n"

if authorities:
    auth_counts = Counter(authorities)
    info_text += "Autorités :\n"
    for i, (auth, count) in enumerate(auth_counts.most_common(3), 1):
        short_auth = auth[:20] + '...' if len(auth) > 20 else auth
        info_text += f"{i}. {short_auth}\n   ({count} docs)\n"

info_text += "\nDépartements :\n"
if departments:
    dept_counts = Counter(departments)
    for i, (dept, count) in enumerate(dept_counts.most_common(3), 1):
        info_text += f"{i}. Dept. {dept} ({count})\n"

ax7.text(0.05, 0.95, info_text, fontsize=9, verticalalignment='top',
         family='monospace', bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))

# Sauvegarder
output_file = 'comprehensive_dashboard.png'
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"\n✓ Tableau de bord sauvegardé : {output_file}")

print("\n" + "="*70)
print("TABLEAU DE BORD CRÉÉ AVEC SUCCÈS")
print("="*70)

plt.show()
