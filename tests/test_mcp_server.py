"""
Tests unitaires pour le serveur MCP Disclose Data
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Ajouter le répertoire parent au path pour importer mcp_server
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from mcp_server import build_query, format_document


class TestBuildQuery(unittest.TestCase):
    """Tests pour la fonction build_query"""

    def test_query_basique(self):
        """Test de génération d'une requête basique sans filtres"""
        query = build_query()
        self.assertIn("+project:219834", query)
        self.assertIn('+status:"success"', query)

    def test_query_avec_keyword(self):
        """Test avec un mot-clé"""
        query = build_query(keyword="éolien")
        self.assertIn("éolien", query)
        self.assertIn("+project:219834", query)

    def test_query_avec_authority(self):
        """Test avec une autorité"""
        query = build_query(authority="Préfecture de région Bretagne")
        self.assertIn('+data_authority:"Préfecture de région Bretagne"', query)

    def test_query_avec_department(self):
        """Test avec un département"""
        query = build_query(department="75")
        self.assertIn('+data_departments:"75"', query)

    def test_query_avec_category(self):
        """Test avec une catégorie"""
        query = build_query(category="Avis")
        self.assertIn('+data_category:"Avis"', query)

    def test_query_avec_dates(self):
        """Test avec des dates"""
        query = build_query(from_date="2024-01-01", to_date="2024-12-31")
        self.assertIn('+publish_at:', query)
        self.assertIn('"2024-01-01T00:00:00Z"', query)
        self.assertIn('"2024-12-31T23:59:59Z"', query)

    def test_query_avec_from_date_seulement(self):
        """Test avec seulement from_date"""
        query = build_query(from_date="2024-01-01")
        self.assertIn('"2024-01-01T00:00:00Z"', query)
        self.assertIn('TO *]', query)

    def test_query_avec_to_date_seulement(self):
        """Test avec seulement to_date"""
        query = build_query(to_date="2024-12-31")
        self.assertIn('[* TO', query)
        self.assertIn('"2024-12-31T23:59:59Z"', query)

    def test_query_combinee(self):
        """Test avec plusieurs filtres combinés"""
        query = build_query(
            keyword="lithium",
            authority="Préfecture de région Bretagne",
            department="35",
            category="Avis",
            from_date="2024-01-01",
            to_date="2024-12-31"
        )
        self.assertIn("lithium", query)
        self.assertIn('+data_authority:"Préfecture de région Bretagne"', query)
        self.assertIn('+data_departments:"35"', query)
        self.assertIn('+data_category:"Avis"', query)
        self.assertIn('"2024-01-01T00:00:00Z"', query)


class TestFormatDocument(unittest.TestCase):
    """Tests pour la fonction format_document"""

    def setUp(self):
        """Créer un mock de document pour les tests"""
        self.mock_doc = Mock()
        self.mock_doc.title = "Test Document"
        self.mock_doc.canonical_url = "https://example.com/doc/123"
        self.mock_doc.pages = 10
        self.mock_doc.description = "Description du dossier"

    def test_format_basique(self):
        """Test du formatage d'un document basique"""
        result = format_document(self.mock_doc)
        self.assertIn("Test Document", result)
        self.assertIn("https://example.com/doc/123", result)
        self.assertIn("10", result)

    def test_format_avec_metadata(self):
        """Test du formatage avec métadonnées"""
        self.mock_doc.data = {
            'authority': 'Préfecture de région Bretagne',
            'category': 'Avis',
            'publication_date': '2024-01-15',
            'departments': ['35', '56'],
            'source_page_url': 'https://source.com/page'
        }

        result = format_document(self.mock_doc)
        self.assertIn("Préfecture de région Bretagne", result)
        self.assertIn("Avis", result)
        self.assertIn("2024-01-15", result)
        self.assertIn("35, 56", result)
        self.assertIn("https://source.com/page", result)

    def test_format_sans_metadata(self):
        """Test du formatage sans métadonnées"""
        self.mock_doc.data = None
        result = format_document(self.mock_doc)
        self.assertIn("Test Document", result)
        self.assertNotIn("Métadonnées", result)

    def test_format_avec_description(self):
        """Test du formatage avec description"""
        result = format_document(self.mock_doc)
        self.assertIn("Dossier", result)
        self.assertIn("Description du dossier", result)

    def test_format_metadata_partielles(self):
        """Test avec seulement certaines métadonnées"""
        self.mock_doc.data = {
            'authority': 'Préfecture de région Bretagne'
        }

        result = format_document(self.mock_doc)
        self.assertIn("Préfecture de région Bretagne", result)
        # Ne devrait pas planter si d'autres champs manquent


class TestMCPServerIntegration(unittest.TestCase):
    """Tests d'intégration pour le serveur MCP"""

    @patch('mcp_server.dc_client')
    async def test_search_documents_tool(self, mock_client):
        """Test de l'outil search_documents"""
        # Mock des résultats
        mock_results = Mock()
        mock_results.count = 1
        mock_doc = Mock()
        mock_doc.id = "123456"
        mock_doc.title = "Document de test"
        mock_doc.canonical_url = "https://example.com/doc/123"
        mock_doc.pages = 5
        mock_doc.data = {'authority': 'Test Authority'}
        mock_results.__iter__ = Mock(return_value=iter([mock_doc]))
        mock_results.__getitem__ = Mock(return_value=[mock_doc])

        mock_client.documents.search.return_value = mock_results

        # Import de la fonction à tester
        from mcp_server import search_documents_tool

        # Test
        result = await search_documents_tool({'keyword': 'test', 'limit': 10})

        # Vérifications
        self.assertEqual(len(result), 1)
        self.assertIn("Document de test", result[0].text)

    @patch('mcp_server.dc_client')
    async def test_get_document_tool(self, mock_client):
        """Test de l'outil get_document"""
        # Mock du document
        mock_doc = Mock()
        mock_doc.title = "Document spécifique"
        mock_doc.canonical_url = "https://example.com/doc/456"
        mock_doc.pages = 8
        mock_doc.data = {
            'authority': 'Préfecture de région Bretagne',
            'category': 'Avis'
        }
        mock_doc.description = "Description du document"

        mock_client.documents.get.return_value = mock_doc

        # Import de la fonction à tester
        from mcp_server import get_document_tool

        # Test
        result = await get_document_tool({'document_id': '456'})

        # Vérifications
        self.assertEqual(len(result), 1)
        self.assertIn("Document spécifique", result[0].text)
        self.assertIn("Préfecture de région Bretagne", result[0].text)


class TestConstants(unittest.TestCase):
    """Tests des constantes"""

    def test_project_id(self):
        """Vérifier que PROJECT_ID est correct"""
        from mcp_server import PROJECT_ID
        self.assertEqual(PROJECT_ID, 219834)


def run_tests():
    """Fonction pour exécuter les tests"""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()


if __name__ == '__main__':
    unittest.main()
