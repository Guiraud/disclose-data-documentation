# Tests unitaires

Ce dossier contient les tests unitaires pour le projet Disclose Data Documentation.

## Installation des dépendances de test

```bash
# Avec uv
uv pip install pytest pytest-asyncio pytest-cov

# Avec pip
pip install pytest pytest-asyncio pytest-cov
```

## Exécution des tests

### Tous les tests

```bash
# Avec pytest (recommandé)
pytest tests/

# Avec unittest
python -m unittest discover tests/
```

### Tests spécifiques

```bash
# Un fichier spécifique
pytest tests/test_mcp_server.py

# Une classe spécifique
pytest tests/test_mcp_server.py::TestBuildQuery

# Un test spécifique
pytest tests/test_mcp_server.py::TestBuildQuery::test_query_basique
```

### Avec couverture de code

```bash
# Générer un rapport de couverture
pytest --cov=mcp_server --cov-report=html tests/

# Voir le rapport
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

### Mode verbose

```bash
# Plus de détails sur les tests
pytest -v tests/

# Encore plus de détails
pytest -vv tests/
```

## Structure des tests

```
tests/
├── __init__.py           # Package tests
├── conftest.py           # Configuration pytest
├── test_mcp_server.py    # Tests du serveur MCP
└── README.md             # Ce fichier
```

## Écrire de nouveaux tests

### Convention de nommage

- Fichiers : `test_*.py`
- Classes : `Test*`
- Fonctions : `test_*`

### Exemple de test simple

```python
def test_ma_fonction():
    """Test de ma_fonction"""
    resultat = ma_fonction(42)
    assert resultat == 84
```

### Exemple de test avec mock

```python
from unittest.mock import Mock, patch

@patch('module.client')
def test_avec_mock(mock_client):
    """Test avec un mock"""
    mock_client.get.return_value = "valeur mockée"
    resultat = fonction_qui_utilise_client()
    assert resultat == "valeur attendue"
```

### Exemple de test asynchrone

```python
import pytest

@pytest.mark.asyncio
async def test_fonction_async():
    """Test d'une fonction asynchrone"""
    resultat = await ma_fonction_async()
    assert resultat is not None
```

## Tests de régression

Avant chaque commit, exécutez :

```bash
pytest tests/
```

Avant chaque pull request, vérifiez la couverture :

```bash
pytest --cov=. --cov-report=term-missing tests/
```

## CI/CD

Les tests sont automatiquement exécutés via GitHub Actions sur chaque :
- Push sur main
- Pull request
- Tag de release

## Ressources

- [Documentation pytest](https://docs.pytest.org/)
- [pytest-asyncio](https://pytest-asyncio.readthedocs.io/)
- [unittest.mock](https://docs.python.org/3/library/unittest.mock.html)
