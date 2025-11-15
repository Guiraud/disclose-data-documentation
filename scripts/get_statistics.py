#!/usr/bin/env python3
"""
Script pour obtenir des statistiques sur la collection Disclose Data

Usage:
    python get_statistics.py [OPTIONS]

Examples:
    python get_statistics.py
    python get_statistics.py --department 75
    python get_statistics.py --year 2024
"""

import argparse
from documentcloud import DocumentCloud
from collections import Counter
from datetime import datetime


def get_all_statistics(department=None, year=None):
    """
    Obtenir des statistiques complètes sur la collection
    """
    client = DocumentCloud()
    PROJECT_ID = 219834

    # Construire la requête de base
    query_parts = [f'+project:{PROJECT_ID}', '+status:"success"']

    if department:
        query_parts.append(f'+data_departments:"{department}"')

    if year:
        query_parts.append(f'+publish_at:["{year}-01-01T00:00:00Z" TO "{year}-12-31T23:59:59Z"]')

    query = ' '.join(query_parts)

    print("="*80)
    print("STATISTIQUES DISCLOSE DATA")
    print("="*80)
    print(f"\nRequête : {query}\n")
    print("Récupération des données...\n")

    # Récupérer tous les documents (limité à 10000)
    results = client.documents.search(query)

    print(f"{'='*80}")
    print(f"NOMBRE TOTAL DE DOCUMENTS : {results.count}")
    print(f"{'='*80}\n")

    # Collecter les statistiques
    authorities = []
    categories = []
    departments = []
    years = []
    months = []
    total_pages = 0

    print("Analyse des documents...")

    # Limiter à 1000 documents pour l'analyse détaillée
    sample_size = min(1000, results.count)

    for i, doc in enumerate(results[:sample_size]):
        if i % 100 == 0 and i > 0:
            print(f"  {i} documents analysés...")

        total_pages += doc.pages if doc.pages else 0

        if hasattr(doc, 'data') and doc.data:
            # Autorités
            authority = doc.data.get('authority')
            if authority:
                authorities.append(authority)

            # Catégories
            category = doc.data.get('category')
            if category:
                categories.append(category)

            # Départements
            doc_departments = doc.data.get('departments', [])
            departments.extend(doc_departments)

            # Dates
            pub_date = doc.data.get('publication_date')
            if pub_date:
                try:
                    # Format attendu : YYYY-MM-DD
                    date_parts = pub_date.split('-')
                    if len(date_parts) >= 2:
                        years.append(date_parts[0])
                        months.append(f"{date_parts[0]}-{date_parts[1]}")
                except:
                    pass

    print(f"\n{'='*80}")
    print("STATISTIQUES GÉNÉRALES")
    print(f"{'='*80}\n")

    print(f"Documents analysés : {sample_size}")
    print(f"Pages totales : {total_pages:,}")
    print(f"Moyenne de pages par document : {total_pages/sample_size:.1f}" if sample_size > 0 else "N/A")

    # Top autorités
    print(f"\n{'='*80}")
    print("TOP 10 AUTORITÉS ENVIRONNEMENTALES")
    print(f"{'='*80}\n")

    if authorities:
        authority_counts = Counter(authorities)
        for i, (authority, count) in enumerate(authority_counts.most_common(10), 1):
            percentage = (count / sample_size) * 100
            print(f"{i:2d}. {authority}")
            print(f"    {count} documents ({percentage:.1f}%)\n")
    else:
        print("Aucune donnée disponible\n")

    # Catégories
    print(f"{'='*80}")
    print("RÉPARTITION PAR CATÉGORIE")
    print(f"{'='*80}\n")

    if categories:
        category_counts = Counter(categories)
        for category, count in category_counts.most_common():
            percentage = (count / sample_size) * 100
            bar = '█' * int(percentage / 2)
            print(f"{category:15s} : {bar} {count} ({percentage:.1f}%)")
    else:
        print("Aucune donnée disponible")

    # Top départements
    print(f"\n{'='*80}")
    print("TOP 15 DÉPARTEMENTS")
    print(f"{'='*80}\n")

    if departments:
        dept_counts = Counter(departments)
        for i, (dept, count) in enumerate(dept_counts.most_common(15), 1):
            print(f"{i:2d}. Département {dept:3s} : {count:4d} documents")
    else:
        print("Aucune donnée disponible")

    # Évolution temporelle
    print(f"\n{'='*80}")
    print("RÉPARTITION PAR ANNÉE")
    print(f"{'='*80}\n")

    if years:
        year_counts = Counter(years)
        for year in sorted(year_counts.keys()):
            count = year_counts[year]
            bar = '█' * (count // 10)
            print(f"{year} : {bar} {count}")
    else:
        print("Aucune donnée disponible")

    # Documents récents
    print(f"\n{'='*80}")
    print("DOCUMENTS LES PLUS RÉCENTS")
    print(f"{'='*80}\n")

    recent_docs = list(results[:5])
    for i, doc in enumerate(recent_docs, 1):
        pub_date = "N/A"
        if hasattr(doc, 'data') and doc.data:
            pub_date = doc.data.get('publication_date', 'N/A')

        print(f"{i}. {doc.title}")
        print(f"   Date : {pub_date}")
        print(f"   URL : {doc.canonical_url}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Obtenir des statistiques sur la collection Disclose Data",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '-d', '--department',
        help='Limiter les statistiques à un département spécifique'
    )

    parser.add_argument(
        '-y', '--year',
        help='Limiter les statistiques à une année spécifique (ex: 2024)'
    )

    args = parser.parse_args()

    get_all_statistics(
        department=args.department,
        year=args.year
    )


if __name__ == '__main__':
    main()
