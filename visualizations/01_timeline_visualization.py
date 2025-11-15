"""
Visualisation 1 : Évolution temporelle des publications
========================================================

Ce script crée un graphique montrant l'évolution du nombre de documents
publiés au fil du temps.
"""

from documentcloud import DocumentCloud
import matplotlib.pyplot as plt
from collections import Counter
from datetime import datetime

# Configuration matplotlib pour un meilleur rendu
plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.size'] = 10

# Initialiser le client
client = DocumentCloud()
PROJECT_ID = 219834

print("Récupération des documents...")
query = f'+project:{PROJECT_ID} +status:"success"'
results = client.documents.search(query)

print(f"Documents trouvés : {results.count}")
print("Analyse des dates de publication...")

# Collecter les dates
dates_by_month = Counter()
dates_by_year = Counter()

for i, doc in enumerate(results[:1000]):  # Limité à 1000 pour la performance
    if i % 100 == 0 and i > 0:
        print(f"  {i} documents analysés...")

    if hasattr(doc, 'data') and doc.data:
        pub_date = doc.data.get('publication_date')
        if pub_date:
            try:
                # Format attendu : YYYY-MM-DD
                parts = pub_date.split('-')
                if len(parts) >= 2:
                    year = parts[0]
                    month = f"{parts[0]}-{parts[1]}"

                    dates_by_year[year] += 1
                    dates_by_month[month] += 1
            except:
                pass

# Créer la figure avec deux sous-graphiques
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))

# Graphique 1 : Par année
if dates_by_year:
    years = sorted(dates_by_year.keys())
    counts = [dates_by_year[year] for year in years]

    ax1.bar(years, counts, color='steelblue', alpha=0.8)
    ax1.set_xlabel('Année')
    ax1.set_ylabel('Nombre de documents')
    ax1.set_title('Nombre de documents publiés par année', fontsize=14, fontweight='bold')
    ax1.grid(axis='y', alpha=0.3)

    # Ajouter les valeurs sur les barres
    for i, (year, count) in enumerate(zip(years, counts)):
        ax1.text(i, count, str(count), ha='center', va='bottom')

# Graphique 2 : Par mois (derniers 24 mois)
if dates_by_month:
    months = sorted(dates_by_month.keys())[-24:]  # 24 derniers mois
    counts = [dates_by_month[month] for month in months]

    ax2.plot(range(len(months)), counts, marker='o', linewidth=2,
             markersize=6, color='coral')
    ax2.fill_between(range(len(months)), counts, alpha=0.3, color='coral')

    ax2.set_xlabel('Mois')
    ax2.set_ylabel('Nombre de documents')
    ax2.set_title('Évolution mensuelle (24 derniers mois)', fontsize=14, fontweight='bold')
    ax2.set_xticks(range(len(months)))
    ax2.set_xticklabels(months, rotation=45, ha='right')
    ax2.grid(axis='y', alpha=0.3)

plt.tight_layout()

# Sauvegarder
output_file = 'timeline_evolution.png'
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"\n✓ Graphique sauvegardé : {output_file}")

# Afficher
plt.show()
