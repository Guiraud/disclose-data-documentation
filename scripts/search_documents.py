#!/usr/bin/env python3
"""
Script de recherche interactive de documents Disclose Data

Usage:
    python search_documents.py [OPTIONS]

Examples:
    python search_documents.py --keyword lithium
    python search_documents.py --authority "Préfecture de région Bretagne"
    python search_documents.py --department 75
    python search_documents.py --from-date 2024-01-01 --to-date 2024-12-31
"""

import argparse
from documentcloud import DocumentCloud
from datetime import datetime


def search_documents(
    keyword=None,
    authority=None,
    department=None,
    category=None,
    from_date=None,
    to_date=None,
    limit=50
):
    """
    Rechercher des documents avec différents filtres
    """
    client = DocumentCloud()
    PROJECT_ID = 219834

    # Construire la requête de base
    query_parts = [f'+project:{PROJECT_ID}', '+status:"success"']

    # Ajouter les filtres
    if keyword:
        query_parts.append(keyword)

    if authority:
        query_parts.append(f'+data_authority:"{authority}"')

    if department:
        query_parts.append(f'+data_departments:"{department}"')

    if category:
        query_parts.append(f'+data_category:"{category}"')

    if from_date or to_date:
        date_from = from_date or "*"
        date_to = to_date or "*"

        if date_from != "*":
            date_from = f'"{date_from}T00:00:00Z"'
        if date_to != "*":
            date_to = f'"{date_to}T23:59:59Z"'

        query_parts.append(f'+publish_at:[{date_from} TO {date_to}]')

    # Assembler la requête
    query = ' '.join(query_parts)

    print(f"Requête : {query}\n")
    print("Recherche en cours...\n")

    # Effectuer la recherche
    results = client.documents.search(query)

    print(f"{'='*80}")
    print(f"Nombre total de documents trouvés : {results.count}")
    print(f"{'='*80}\n")

    # Afficher les résultats
    for i, doc in enumerate(results[:limit], 1):
        print(f"{i}. {doc.title}")
        print(f"   URL : {doc.canonical_url}")

        if hasattr(doc, 'data') and doc.data:
            authority = doc.data.get('authority', 'N/A')
            category = doc.data.get('category', 'N/A')
            pub_date = doc.data.get('publication_date', 'N/A')
            departments = doc.data.get('departments', [])

            print(f"   Autorité : {authority}")
            print(f"   Catégorie : {category}")
            print(f"   Date : {pub_date}")
            if departments:
                print(f"   Départements : {', '.join(departments)}")

        print()

    if results.count > limit:
        print(f"Note : Seuls les {limit} premiers résultats sont affichés.")
        print(f"Utilisez --limit pour en afficher plus.")

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Rechercher des documents dans la collection Disclose Data",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation :
  %(prog)s --keyword éolien
  %(prog)s --authority "Préfecture de région Bretagne"
  %(prog)s --department 75
  %(prog)s --category Avis
  %(prog)s --from-date 2024-01-01 --to-date 2024-12-31
  %(prog)s --keyword lithium --department 973
        """
    )

    parser.add_argument(
        '-k', '--keyword',
        help='Mot-clé à rechercher dans les documents'
    )

    parser.add_argument(
        '-a', '--authority',
        help='Filtrer par autorité environnementale'
    )

    parser.add_argument(
        '-d', '--department',
        help='Filtrer par code département (ex: 75, 35, 973)'
    )

    parser.add_argument(
        '-c', '--category',
        choices=['Avis', 'Cadrage', 'Cas par Cas'],
        help='Filtrer par catégorie de procédure'
    )

    parser.add_argument(
        '--from-date',
        help='Date de début (format: YYYY-MM-DD)'
    )

    parser.add_argument(
        '--to-date',
        help='Date de fin (format: YYYY-MM-DD)'
    )

    parser.add_argument(
        '-l', '--limit',
        type=int,
        default=50,
        help='Nombre maximum de résultats à afficher (défaut: 50)'
    )

    args = parser.parse_args()

    # Vérifier qu'au moins un filtre est fourni
    if not any([args.keyword, args.authority, args.department, args.category, args.from_date, args.to_date]):
        parser.print_help()
        print("\nErreur : Veuillez spécifier au moins un critère de recherche.")
        return

    # Effectuer la recherche
    search_documents(
        keyword=args.keyword,
        authority=args.authority,
        department=args.department,
        category=args.category,
        from_date=args.from_date,
        to_date=args.to_date,
        limit=args.limit
    )


if __name__ == '__main__':
    main()
