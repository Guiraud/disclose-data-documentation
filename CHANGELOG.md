# Changelog

Toutes les modifications notables de ce projet seront documentées dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Semantic Versioning](https://semver.org/lang/fr/).

## [1.0.0] - 2024-12-05

### Ajouté
- ✅ Tests unitaires pour `mcp_server.py`
- ✅ Module `utils.py` avec retry logic et validation
- ✅ Retry automatique pour les appels API (3 tentatives avec backoff exponentiel)
- ✅ Validation robuste des paramètres (dates, départements, catégories)
- ✅ Configuration moderne avec `pyproject.toml` (PEP 621)
- ✅ Script d'installation automatique `setup_mcp.sh`
- ✅ Fichier `.python-version` pour pyenv
- ✅ Licence MIT
- ✅ `.gitignore` complet
- ✅ Badges dans le README (Python, License, Code Style, MCP, Status)
- ✅ Section "Démarrage ultra-rapide" dans le README
- ✅ Fichier `mcp_config.example.json` avec exemples détaillés
- ✅ Documentation des tests (`tests/README.md`)
- ✅ Ce fichier CHANGELOG.md
- ✅ Fichier CONTRIBUTING.md

### Amélioré
- 🔧 Configuration MCP avec chemin absolu dans `mcp_config.json`
- 🔧 Gestion d'erreurs robuste dans toutes les fonctions MCP
- 🔧 Logging amélioré avec format structuré
- 🔧 Documentation enrichie avec emojis et meilleure navigation
- 🔧 Structure du README plus claire

### Technique
- Type hints améliorés dans `mcp_server.py`
- Docstrings complètes pour toutes les fonctions
- Support optionnel des dépendances dev et docs
- Configuration pytest, black, ruff, mypy dans pyproject.toml

## [0.9.0] - 2024-11-XX

### Ajouté
- Serveur MCP (Model Context Protocol)
- 5 outils MCP : search, get_document, statistics, list_authorities, get_document_text
- Documentation MCP (`MCP_SERVER.md`)
- Configuration pour Claude Desktop

## [0.8.0] - 2024-XX-XX

### Ajouté
- Support pyenv dans la documentation
- Tutoriel pour débutants
- Scripts de visualisation (5 scripts)
- Scripts utilitaires CLI (4 scripts)
- Exemples de code (6 exemples)

## [0.7.0] - 2024-XX-XX

### Ajouté
- Documentation API complète
- FAQ détaillée
- Guide d'installation avec uv et pip
- Métadonnées personnalisées des documents

---

## Types de changements

- `Ajouté` pour les nouvelles fonctionnalités
- `Modifié` pour les changements dans les fonctionnalités existantes
- `Déprécié` pour les fonctionnalités qui seront bientôt supprimées
- `Supprimé` pour les fonctionnalités supprimées
- `Corrigé` pour les corrections de bugs
- `Sécurité` pour les vulnérabilités corrigées
