#!/usr/bin/env python3
"""
Script pour surveiller les nouveaux documents ajoutés à Disclose Data

Usage:
    python monitor_new_documents.py [OPTIONS]

Examples:
    python monitor_new_documents.py --days 7
    python monitor_new_documents.py --days 30 --department 75
    python monitor_new_documents.py --days 1 --keyword éolien
"""

import argparse
from documentcloud import DocumentCloud
from datetime import datetime, timedelta


def monitor_new_documents(days=7, keyword=None, department=None, authority=None):
    """
    Surveiller les documents ajoutés récemment
    """
    client = DocumentCloud()
    PROJECT_ID = 219834

    # Calculer la date limite
    limit_date = datetime.now() - timedelta(days=days)
    date_str = limit_date.strftime("%Y-%m-%dT%H:%M:%SZ")

    # Construire la requête
    query_parts = [
        f'+project:{PROJECT_ID}',
        '+status:"success"',
        f'+created_at:["{date_str}" TO NOW]'
    ]

    if keyword:
        query_parts.append(keyword)
    if department:
        query_parts.append(f'+data_departments:"{department}"')
    if authority:
        query_parts.append(f'+data_authority:"{authority}"')

    query = ' '.join(query_parts)

    print("="*80)
    print(f"SURVEILLANCE DES NOUVEAUX DOCUMENTS ({days} derniers jours)")
    print("="*80)
    print(f"\nPériode : depuis {limit_date.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Requête : {query}\n")
    print("Recherche en cours...\n")

    # Effectuer la recherche
    results = client.documents.search(query)

    print(f"{'='*80}")
    print(f"NOUVEAUX DOCUMENTS TROUVÉS : {results.count}")
    print(f"{'='*80}\n")

    if results.count == 0:
        print("Aucun nouveau document trouvé pour cette période.")
        return

    # Grouper par date
    documents_by_date = {}

    for doc in results:
        if hasattr(doc, 'data') and doc.data:
            pub_date = doc.data.get('publication_date', 'Date inconnue')
        else:
            pub_date = 'Date inconnue'

        if pub_date not in documents_by_date:
            documents_by_date[pub_date] = []

        documents_by_date[pub_date].append(doc)

    # Afficher les documents par date (du plus récent au plus ancien)
    for pub_date in sorted(documents_by_date.keys(), reverse=True):
        docs = documents_by_date[pub_date]

        print(f"\n{'─'*80}")
        print(f"📅 {pub_date} ({len(docs)} document{'s' if len(docs) > 1 else ''})")
        print(f"{'─'*80}\n")

        for i, doc in enumerate(docs, 1):
            print(f"{i}. {doc.title}")

            if hasattr(doc, 'data') and doc.data:
                authority = doc.data.get('authority', 'N/A')
                category = doc.data.get('category', 'N/A')
                departments = doc.data.get('departments', [])

                print(f"   Autorité : {authority}")
                print(f"   Catégorie : {category}")
                if departments:
                    print(f"   Départements : {', '.join(departments)}")

            print(f"   URL : {doc.canonical_url}")
            print()

    # Statistiques
    print(f"\n{'='*80}")
    print("STATISTIQUES")
    print(f"{'='*80}\n")

    authorities = {}
    categories = {}

    for doc in results:
        if hasattr(doc, 'data') and doc.data:
            authority = doc.data.get('authority', 'N/A')
            category = doc.data.get('category', 'N/A')

            authorities[authority] = authorities.get(authority, 0) + 1
            categories[category] = categories.get(category, 0) + 1

    print("Par autorité :")
    for authority, count in sorted(authorities.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"  - {authority}: {count}")

    print("\nPar catégorie :")
    for category, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
        print(f"  - {category}: {count}")


def main():
    parser = argparse.ArgumentParser(
        description="Surveiller les nouveaux documents Disclose Data",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation :
  %(prog)s --days 7
  %(prog)s --days 30 --department 75
  %(prog)s --days 1 --keyword lithium
  %(prog)s --days 14 --authority "Préfecture de région Bretagne"
        """
    )

    parser.add_argument(
        '--days',
        type=int,
        default=7,
        help='Nombre de jours à surveiller (défaut: 7)'
    )

    parser.add_argument(
        '-k', '--keyword',
        help='Filtrer par mot-clé'
    )

    parser.add_argument(
        '-d', '--department',
        help='Filtrer par département'
    )

    parser.add_argument(
        '-a', '--authority',
        help='Filtrer par autorité'
    )

    args = parser.parse_args()

    monitor_new_documents(
        days=args.days,
        keyword=args.keyword,
        department=args.department,
        authority=args.authority
    )


if __name__ == '__main__':
    main()
