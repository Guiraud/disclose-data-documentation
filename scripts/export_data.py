#!/usr/bin/env python3
"""
Script d'export de données Disclose Data vers CSV

Usage:
    python export_data.py [OPTIONS] -o output.csv

Examples:
    python export_data.py --keyword éolien -o eolien.csv
    python export_data.py --department 75 -o paris.csv
    python export_data.py --from-date 2024-01-01 --to-date 2024-12-31 -o 2024.csv
"""

import argparse
import csv
from documentcloud import DocumentCloud
from datetime import datetime


def export_documents(
    output_file,
    keyword=None,
    authority=None,
    department=None,
    category=None,
    from_date=None,
    to_date=None,
    max_results=1000
):
    """
    Exporter des documents vers un fichier CSV
    """
    client = DocumentCloud()
    PROJECT_ID = 219834

    # Construire la requête
    query_parts = [f'+project:{PROJECT_ID}', '+status:"success"']

    if keyword:
        query_parts.append(keyword)
    if authority:
        query_parts.append(f'+data_authority:"{authority}"')
    if department:
        query_parts.append(f'+data_departments:"{department}"')
    if category:
        query_parts.append(f'+data_category:"{category}"')

    if from_date or to_date:
        date_from = f'"{from_date}T00:00:00Z"' if from_date else "*"
        date_to = f'"{to_date}T23:59:59Z"' if to_date else "*"
        query_parts.append(f'+publish_at:[{date_from} TO {date_to}]')

    query = ' '.join(query_parts)

    print(f"Requête : {query}\n")
    print("Récupération des documents...\n")

    # Effectuer la recherche
    results = client.documents.search(query)

    print(f"Nombre de documents trouvés : {results.count}")

    if results.count > max_results:
        print(f"Limitation à {max_results} documents pour l'export.")

    # Définir les champs CSV
    fields = [
        'id',
        'title',
        'pages',
        'url',
        'dossier',
        'authority',
        'category',
        'departments',
        'publication_date',
        'source_page_url',
        'source_file_url',
    ]

    # Créer le fichier CSV
    print(f"\nExport vers {output_file}...")

    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()

        count = 0
        for doc in results[:max_results]:
            row = {
                'id': doc.id,
                'title': doc.title,
                'pages': doc.pages,
                'url': doc.canonical_url,
                'dossier': getattr(doc, 'description', ''),
            }

            # Ajouter les métadonnées personnalisées
            if hasattr(doc, 'data') and doc.data:
                row['authority'] = doc.data.get('authority', '')
                row['category'] = doc.data.get('category', '')
                departments = doc.data.get('departments', [])
                row['departments'] = ', '.join(departments) if departments else ''
                row['publication_date'] = doc.data.get('publication_date', '')
                row['source_page_url'] = doc.data.get('source_page_url', '')
                row['source_file_url'] = doc.data.get('source_file_url', '')
            else:
                row['authority'] = ''
                row['category'] = ''
                row['departments'] = ''
                row['publication_date'] = ''
                row['source_page_url'] = ''
                row['source_file_url'] = ''

            writer.writerow(row)
            count += 1

            # Afficher la progression
            if count % 100 == 0:
                print(f"  {count} documents exportés...")

    print(f"\n✓ Export terminé : {count} documents exportés dans {output_file}")

    # Afficher quelques statistiques
    print(f"\nStatistiques :")
    print(f"  Fichier : {output_file}")
    print(f"  Documents : {count}")

    return count


def main():
    parser = argparse.ArgumentParser(
        description="Exporter des documents Disclose Data vers CSV",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation :
  %(prog)s --keyword éolien -o eolien.csv
  %(prog)s --department 75 -o paris.csv
  %(prog)s --authority "Préfecture de région Bretagne" -o bretagne.csv
  %(prog)s --from-date 2024-01-01 --to-date 2024-12-31 -o 2024.csv
        """
    )

    parser.add_argument(
        '-o', '--output',
        required=True,
        help='Fichier CSV de sortie'
    )

    parser.add_argument(
        '-k', '--keyword',
        help='Mot-clé à rechercher'
    )

    parser.add_argument(
        '-a', '--authority',
        help='Filtrer par autorité'
    )

    parser.add_argument(
        '-d', '--department',
        help='Filtrer par département'
    )

    parser.add_argument(
        '-c', '--category',
        choices=['Avis', 'Cadrage', 'Cas par Cas'],
        help='Filtrer par catégorie'
    )

    parser.add_argument(
        '--from-date',
        help='Date de début (YYYY-MM-DD)'
    )

    parser.add_argument(
        '--to-date',
        help='Date de fin (YYYY-MM-DD)'
    )

    parser.add_argument(
        '--max-results',
        type=int,
        default=1000,
        help='Nombre maximum de documents à exporter (défaut: 1000)'
    )

    args = parser.parse_args()

    # Effectuer l'export
    export_documents(
        output_file=args.output,
        keyword=args.keyword,
        authority=args.authority,
        department=args.department,
        category=args.category,
        from_date=args.from_date,
        to_date=args.to_date,
        max_results=args.max_results
    )


if __name__ == '__main__':
    main()
