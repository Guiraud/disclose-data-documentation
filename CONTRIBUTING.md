# Guide de contribution

Merci de votre intérêt pour contribuer au projet Disclose Data Documentation ! 🎉

## Table des matières

- [Code de conduite](#code-de-conduite)
- [Comment contribuer](#comment-contribuer)
- [Configuration de l'environnement de développement](#configuration-de-lenvironnement-de-développement)
- [Standards de code](#standards-de-code)
- [Tests](#tests)
- [Documentation](#documentation)
- [Processus de pull request](#processus-de-pull-request)

---

## Code de conduite

En participant à ce projet, vous acceptez de respecter notre code de conduite :

- Soyez respectueux et professionnel
- Acceptez les critiques constructives
- Concentrez-vous sur ce qui est bon pour la communauté
- Faites preuve d'empathie envers les autres membres

## Comment contribuer

Il existe de nombreuses façons de contribuer :

### 🐛 Signaler des bugs

Utilisez le système d'issues GitHub pour signaler des bugs :

1. Vérifiez qu'une issue similaire n'existe pas déjà
2. Créez une nouvelle issue avec le label "bug"
3. Décrivez le problème en détail :
   - Ce que vous avez fait
   - Ce que vous attendiez
   - Ce qui s'est passé
   - Comment reproduire le bug

### 💡 Proposer des améliorations

Vous avez une idée pour améliorer le projet ?

1. Créez une issue avec le label "enhancement"
2. Décrivez votre proposition en détail
3. Expliquez pourquoi c'est utile
4. Attendez les retours avant de commencer le développement

### 📝 Améliorer la documentation

La documentation peut toujours être améliorée :

- Corriger des fautes d'orthographe
- Clarifier des explications
- Ajouter des exemples
- Traduire en anglais

### 🔧 Contribuer du code

Voir la section [Processus de pull request](#processus-de-pull-request)

---

## Configuration de l'environnement de développement

### Prérequis

- Python 3.10 ou supérieur
- Git
- uv (recommandé) ou pip

### Installation

```bash
# Cloner le dépôt
git clone https://github.com/Guiraud/disclose-data-documentation.git
cd disclose-data-documentation

# Créer un environnement virtuel
uv venv
source .venv/bin/activate  # Linux/macOS
# ou
.venv\Scripts\activate  # Windows

# Installer les dépendances (incluant dev)
uv pip install -e ".[dev]"

# Ou avec pip
pip install -e ".[dev]"
```

### Vérifier l'installation

```bash
# Exécuter les tests
pytest tests/

# Vérifier le style de code
ruff check .
black --check .

# Vérifier les types
mypy mcp_server.py utils.py
```

---

## Standards de code

### Style de code

Nous utilisons les standards suivants :

- **Formatage** : [Black](https://black.readthedocs.io/) avec une longueur de ligne de 100
- **Linting** : [Ruff](https://docs.astral.sh/ruff/)
- **Type hints** : [mypy](https://mypy.readthedocs.io/)

### Avant de commit

```bash
# Formater le code
black .

# Vérifier le linting
ruff check . --fix

# Vérifier les types
mypy mcp_server.py utils.py

# Exécuter les tests
pytest tests/
```

### Conventions de nommage

- **Variables et fonctions** : `snake_case`
- **Classes** : `PascalCase`
- **Constantes** : `UPPER_SNAKE_CASE`
- **Fichiers** : `snake_case.py`

### Docstrings

Utilisez le format Google :

```python
def ma_fonction(param1: str, param2: int) -> bool:
    """
    Brève description de la fonction.

    Description plus détaillée si nécessaire.

    Args:
        param1: Description du paramètre 1
        param2: Description du paramètre 2

    Returns:
        Description de la valeur de retour

    Raises:
        ValueError: Description de l'exception

    Example:
        >>> ma_fonction("test", 42)
        True
    """
    pass
```

---

## Tests

### Exécuter les tests

```bash
# Tous les tests
pytest tests/

# Avec couverture
pytest --cov=. --cov-report=html tests/

# Tests spécifiques
pytest tests/test_mcp_server.py::TestBuildQuery
```

### Écrire des tests

- Créez un fichier `test_*.py` dans le dossier `tests/`
- Nommez les fonctions de test `test_*`
- Utilisez des assertions claires
- Mockez les appels externes (API, etc.)

Exemple :

```python
def test_ma_fonction():
    """Test de ma_fonction avec des paramètres valides."""
    resultat = ma_fonction("input")
    assert resultat == "expected output"
```

### Couverture de code

Visez une couverture de **au moins 80%** pour le nouveau code.

---

## Documentation

### Mettre à jour la documentation

Si votre contribution modifie le comportement :

1. Mettez à jour le README.md
2. Mettez à jour les docstrings
3. Ajoutez des exemples si nécessaire
4. Mettez à jour le CHANGELOG.md

### Documentation des API

Ajoutez des docstrings complètes pour :

- Toutes les fonctions publiques
- Toutes les classes
- Tous les modules

---

## Processus de pull request

### Avant de créer une PR

1. ✅ Créez une issue pour discuter de votre changement (pour les gros changements)
2. ✅ Créez une branche depuis `main` : `git checkout -b feature/ma-fonctionnalite`
3. ✅ Faites vos modifications
4. ✅ Ajoutez des tests
5. ✅ Vérifiez que tous les tests passent
6. ✅ Vérifiez le style de code
7. ✅ Mettez à jour la documentation
8. ✅ Mettez à jour CHANGELOG.md

### Créer la PR

1. Poussez votre branche : `git push origin feature/ma-fonctionnalite`
2. Créez une pull request sur GitHub
3. Décrivez vos changements en détail
4. Liez l'issue correspondante (si applicable)
5. Attendez la revue de code

### Template de PR

```markdown
## Description

Brève description des changements

## Type de changement

- [ ] Bug fix
- [ ] Nouvelle fonctionnalité
- [ ] Breaking change
- [ ] Documentation

## Checklist

- [ ] Tests ajoutés/mis à jour
- [ ] Documentation mise à jour
- [ ] CHANGELOG.md mis à jour
- [ ] Tous les tests passent
- [ ] Code formaté avec Black
- [ ] Linting passé (Ruff)
- [ ] Type checking passé (mypy)

## Tests

Description des tests ajoutés

## Screenshots (si applicable)

Ajoutez des captures d'écran si pertinent
```

### Revue de code

- Répondez aux commentaires de manière constructive
- Effectuez les modifications demandées
- Poussez les modifications (elles seront automatiquement ajoutées à la PR)

### Merge

Une fois approuvée, votre PR sera mergée par un mainteneur.

---

## Questions ?

Si vous avez des questions :

- 📧 Email : data@disclose.ngo
- 🐛 Issue GitHub : [Créer une issue](https://github.com/Guiraud/disclose-data-documentation/issues)

Merci pour votre contribution ! 🙏
