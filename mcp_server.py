#!/usr/bin/env python3
"""
Serveur MCP pour l'API Disclose Data

Ce serveur expose les fonctionnalités de recherche et de récupération
de documents des autorités environnementales françaises via le Model Context Protocol.
"""

import asyncio
import logging
from typing import Any, Optional, Sequence
from datetime import datetime

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource

from documentcloud import DocumentCloud

# Configuration du logging (doit être avant l'import de utils)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("disclose-data-mcp")

# Import des utilitaires
try:
    from utils import (
        retry_on_error,
        validate_date_format,
        validate_department_code,
        validate_category,
        safe_dict_get,
        APIError,
        ValidationError,
    )
    logger.info("Utilitaires chargés avec succès")
except ImportError:
    # Fallback si utils.py n'est pas disponible
    logger.warning("Module utils non disponible, fonctionnement en mode dégradé")
    def retry_on_error(*args, **kwargs):
        def decorator(func):
            return func
        return decorator
    def validate_date_format(date_str): return True
    def validate_department_code(code): return True
    def validate_category(cat): return True
    def safe_dict_get(data, key, default=None): return data.get(key, default) if data else default
    class APIError(Exception): pass
    class ValidationError(Exception): pass

# Constantes
PROJECT_ID = 219834

# Initialiser le serveur MCP
app = Server("disclose-data-server")

# Client DocumentCloud global
dc_client = DocumentCloud()


# Fonctions wrapper avec retry logic pour appels API
@retry_on_error(max_attempts=3, initial_delay=1.0, backoff_factor=2.0)
def search_with_retry(query: str):
    """Recherche avec retry automatique en cas d'erreur réseau."""
    logger.debug(f"Recherche avec retry: {query}")
    return dc_client.documents.search(query)


@retry_on_error(max_attempts=3, initial_delay=1.0, backoff_factor=2.0)
def get_document_with_retry(doc_id: str):
    """Récupération de document avec retry automatique."""
    logger.debug(f"Récupération document avec retry: {doc_id}")
    return dc_client.documents.get(doc_id)


def build_query(
    keyword: Optional[str] = None,
    authority: Optional[str] = None,
    department: Optional[str] = None,
    category: Optional[str] = None,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
) -> str:
    """
    Construire une requête DocumentCloud avec les filtres fournis.

    Args:
        keyword: Mot-clé à rechercher
        authority: Autorité environnementale
        department: Code département
        category: Catégorie de document
        from_date: Date de début (YYYY-MM-DD)
        to_date: Date de fin (YYYY-MM-DD)

    Returns:
        Requête DocumentCloud formatée

    Raises:
        ValidationError: Si les paramètres sont invalides
    """
    query_parts = [f"+project:{PROJECT_ID}", '+status:"success"']

    if keyword:
        query_parts.append(keyword)

    if authority:
        query_parts.append(f'+data_authority:"{authority}"')

    if department:
        if not validate_department_code(department):
            logger.warning(f"Code département potentiellement invalide: {department}")
        query_parts.append(f'+data_departments:"{department}"')

    if category:
        if not validate_category(category):
            raise ValidationError(f"Catégorie invalide: {category}. Valeurs acceptées: Avis, Cadrage, Cas par Cas")
        query_parts.append(f'+data_category:"{category}"')

    if from_date:
        if not validate_date_format(from_date):
            raise ValidationError(f"Format de date invalide pour from_date: {from_date}. Format attendu: YYYY-MM-DD")

    if to_date:
        if not validate_date_format(to_date):
            raise ValidationError(f"Format de date invalide pour to_date: {to_date}. Format attendu: YYYY-MM-DD")

    if from_date or to_date:
        date_from = f'"{from_date}T00:00:00Z"' if from_date else "*"
        date_to = f'"{to_date}T23:59:59Z"' if to_date else "*"
        query_parts.append(f'+publish_at:[{date_from} TO {date_to}]')

    return ' '.join(query_parts)


def format_document(doc: Any) -> str:
    """Formater un document pour l'affichage."""
    result = [f"# {doc.title}\n"]
    result.append(f"**URL**: {doc.canonical_url}")
    result.append(f"**Pages**: {doc.pages}")

    if hasattr(doc, 'data') and doc.data:
        result.append("\n## Métadonnées")

        if doc.data.get('authority'):
            result.append(f"- **Autorité**: {doc.data['authority']}")

        if doc.data.get('category'):
            result.append(f"- **Catégorie**: {doc.data['category']}")

        if doc.data.get('publication_date'):
            result.append(f"- **Date de publication**: {doc.data['publication_date']}")

        if doc.data.get('departments'):
            deps = ', '.join(doc.data['departments'])
            result.append(f"- **Départements**: {deps}")

        if doc.data.get('source_page_url'):
            result.append(f"- **Source**: {doc.data['source_page_url']}")

    if hasattr(doc, 'description') and doc.description:
        result.append(f"\n## Dossier\n{doc.description}")

    return '\n'.join(result)


@app.list_tools()
async def list_tools() -> list[Tool]:
    """Liste des outils disponibles dans le serveur MCP."""
    return [
        Tool(
            name="search_documents",
            description="Rechercher des documents dans la collection Disclose Data avec des filtres optionnels",
            inputSchema={
                "type": "object",
                "properties": {
                    "keyword": {
                        "type": "string",
                        "description": "Mot-clé à rechercher dans les documents (ex: 'éolien', 'lithium')"
                    },
                    "authority": {
                        "type": "string",
                        "description": "Filtrer par autorité environnementale (ex: 'Préfecture de région Bretagne')"
                    },
                    "department": {
                        "type": "string",
                        "description": "Code département français (ex: '75' pour Paris, '35' pour Ille-et-Vilaine)"
                    },
                    "category": {
                        "type": "string",
                        "enum": ["Avis", "Cadrage", "Cas par Cas"],
                        "description": "Catégorie de procédure"
                    },
                    "from_date": {
                        "type": "string",
                        "description": "Date de début (format: YYYY-MM-DD)"
                    },
                    "to_date": {
                        "type": "string",
                        "description": "Date de fin (format: YYYY-MM-DD)"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Nombre maximum de résultats à retourner (défaut: 10)",
                        "default": 10
                    }
                }
            }
        ),
        Tool(
            name="get_document",
            description="Récupérer les détails d'un document spécifique par son ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "document_id": {
                        "type": "string",
                        "description": "ID du document DocumentCloud"
                    }
                },
                "required": ["document_id"]
            }
        ),
        Tool(
            name="get_statistics",
            description="Obtenir des statistiques sur la collection ou un sous-ensemble filtré",
            inputSchema={
                "type": "object",
                "properties": {
                    "department": {
                        "type": "string",
                        "description": "Limiter les statistiques à un département"
                    },
                    "year": {
                        "type": "string",
                        "description": "Limiter les statistiques à une année (format: YYYY)"
                    }
                }
            }
        ),
        Tool(
            name="list_authorities",
            description="Lister les autorités environnementales disponibles avec le nombre de documents",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Nombre d'autorités à retourner (défaut: 20)",
                        "default": 20
                    }
                }
            }
        ),
        Tool(
            name="get_document_text",
            description="Récupérer le texte complet d'un document (si disponible via OCR)",
            inputSchema={
                "type": "object",
                "properties": {
                    "document_id": {
                        "type": "string",
                        "description": "ID du document DocumentCloud"
                    },
                    "page": {
                        "type": "integer",
                        "description": "Numéro de page spécifique (optionnel, retourne toutes les pages par défaut)"
                    }
                },
                "required": ["document_id"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
    """Gestionnaire d'appels d'outils."""

    try:
        if name == "search_documents":
            return await search_documents_tool(arguments)

        elif name == "get_document":
            return await get_document_tool(arguments)

        elif name == "get_statistics":
            return await get_statistics_tool(arguments)

        elif name == "list_authorities":
            return await list_authorities_tool(arguments)

        elif name == "get_document_text":
            return await get_document_text_tool(arguments)

        else:
            return [TextContent(type="text", text=f"Outil inconnu: {name}")]

    except Exception as e:
        logger.error(f"Erreur lors de l'exécution de {name}: {e}")
        return [TextContent(type="text", text=f"Erreur: {str(e)}")]


async def search_documents_tool(arguments: dict) -> Sequence[TextContent]:
    """Rechercher des documents avec filtres."""
    keyword = arguments.get("keyword")
    authority = arguments.get("authority")
    department = arguments.get("department")
    category = arguments.get("category")
    from_date = arguments.get("from_date")
    to_date = arguments.get("to_date")
    limit = arguments.get("limit", 10)

    query = build_query(keyword, authority, department, category, from_date, to_date)

    logger.info(f"Recherche: {query}")
    results = search_with_retry(query)

    output = [f"# Résultats de recherche\n"]
    output.append(f"**Requête**: `{query}`")
    output.append(f"**Total de documents trouvés**: {results.count}\n")

    if results.count == 0:
        output.append("Aucun document trouvé.")
        return [TextContent(type="text", text='\n'.join(output))]

    output.append(f"## Documents (affichage des {min(limit, results.count)} premiers)\n")

    for i, doc in enumerate(results[:limit], 1):
        output.append(f"### {i}. {doc.title}")
        output.append(f"- **ID**: {doc.id}")
        output.append(f"- **URL**: {doc.canonical_url}")
        output.append(f"- **Pages**: {doc.pages}")

        if hasattr(doc, 'data') and doc.data:
            if doc.data.get('authority'):
                output.append(f"- **Autorité**: {doc.data['authority']}")
            if doc.data.get('category'):
                output.append(f"- **Catégorie**: {doc.data['category']}")
            if doc.data.get('publication_date'):
                output.append(f"- **Date**: {doc.data['publication_date']}")
            if doc.data.get('departments'):
                deps = ', '.join(doc.data['departments'])
                output.append(f"- **Départements**: {deps}")

        output.append("")

    if results.count > limit:
        output.append(f"\n*Note: {results.count - limit} documents supplémentaires non affichés.*")

    return [TextContent(type="text", text='\n'.join(output))]


async def get_document_tool(arguments: dict) -> Sequence[TextContent]:
    """Récupérer un document spécifique."""
    doc_id = arguments["document_id"]

    logger.info(f"Récupération du document: {doc_id}")
    doc = get_document_with_retry(doc_id)

    return [TextContent(type="text", text=format_document(doc))]


async def get_statistics_tool(arguments: dict) -> Sequence[TextContent]:
    """Obtenir des statistiques."""
    department = arguments.get("department")
    year = arguments.get("year")

    query_parts = [f"+project:{PROJECT_ID}", '+status:"success"']

    if department:
        query_parts.append(f'+data_departments:"{department}"')

    if year:
        query_parts.append(f'+publish_at:["{year}-01-01T00:00:00Z" TO "{year}-12-31T23:59:59Z"]')

    query = ' '.join(query_parts)

    logger.info(f"Statistiques: {query}")
    results = search_with_retry(query)

    # Collecter des statistiques
    authorities = {}
    categories = {}
    departments_count = {}
    total_pages = 0

    for doc in results[:500]:  # Limité pour performance
        if doc.pages:
            total_pages += doc.pages

        if hasattr(doc, 'data') and doc.data:
            if doc.data.get('authority'):
                auth = doc.data['authority']
                authorities[auth] = authorities.get(auth, 0) + 1

            if doc.data.get('category'):
                cat = doc.data['category']
                categories[cat] = categories.get(cat, 0) + 1

            for dept in doc.data.get('departments', []):
                departments_count[dept] = departments_count.get(dept, 0) + 1

    output = ["# Statistiques Disclose Data\n"]
    output.append(f"**Total de documents**: {results.count}")
    output.append(f"**Total de pages**: {total_pages:,}")
    if results.count > 0:
        output.append(f"**Moyenne pages/document**: {total_pages/min(500, results.count):.1f}")

    if categories:
        output.append("\n## Répartition par catégorie")
        for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            output.append(f"- **{cat}**: {count}")

    if authorities:
        output.append("\n## Top 10 autorités")
        for auth, count in sorted(authorities.items(), key=lambda x: x[1], reverse=True)[:10]:
            output.append(f"- {auth}: {count}")

    if departments_count:
        output.append("\n## Top 10 départements")
        for dept, count in sorted(departments_count.items(), key=lambda x: x[1], reverse=True)[:10]:
            output.append(f"- Département {dept}: {count}")

    return [TextContent(type="text", text='\n'.join(output))]


async def list_authorities_tool(arguments: dict) -> Sequence[TextContent]:
    """Lister les autorités disponibles."""
    limit = arguments.get("limit", 20)

    query = f"+project:{PROJECT_ID} +status:\"success\""
    results = search_with_retry(query)

    authorities = {}
    for doc in results[:1000]:  # Échantillon
        if hasattr(doc, 'data') and doc.data and doc.data.get('authority'):
            auth = doc.data['authority']
            authorities[auth] = authorities.get(auth, 0) + 1

    output = ["# Autorités environnementales\n"]
    output.append(f"**Total d'autorités uniques**: {len(authorities)}\n")

    for i, (auth, count) in enumerate(sorted(authorities.items(), key=lambda x: x[1], reverse=True)[:limit], 1):
        output.append(f"{i}. **{auth}** ({count} documents)")

    return [TextContent(type="text", text='\n'.join(output))]


async def get_document_text_tool(arguments: dict) -> Sequence[TextContent]:
    """Récupérer le texte d'un document."""
    doc_id = arguments["document_id"]
    page = arguments.get("page")

    logger.info(f"Récupération du texte: {doc_id} (page: {page})")
    doc = get_document_with_retry(doc_id)

    output = [f"# Texte du document: {doc.title}\n"]

    try:
        if page is not None:
            # Récupérer une page spécifique
            text = doc.get_page_text(page)
            output.append(f"## Page {page}\n")
            output.append(text if text else "*Aucun texte disponible pour cette page*")
        else:
            # Récupérer tout le texte
            full_text = doc.full_text
            if full_text:
                output.append(full_text)
            else:
                output.append("*Texte non disponible pour ce document*")
    except Exception as e:
        output.append(f"*Erreur lors de la récupération du texte: {str(e)}*")

    return [TextContent(type="text", text='\n'.join(output))]


async def main():
    """Point d'entrée principal du serveur MCP."""
    async with stdio_server() as (read_stream, write_stream):
        logger.info("Serveur MCP Disclose Data démarré")
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
