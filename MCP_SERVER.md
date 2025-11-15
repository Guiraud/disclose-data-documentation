# Serveur MCP Disclose Data

Ce projet inclut un serveur MCP (Model Context Protocol) qui permet à Claude et d'autres clients MCP de rechercher et récupérer des documents des autorités environnementales françaises.

## Qu'est-ce qu'un serveur MCP ?

Le Model Context Protocol (MCP) est un protocole standardisé qui permet aux modèles d'IA d'interagir avec des sources de données externes de manière structurée. Ce serveur expose les fonctionnalités de l'API Disclose Data via MCP.

## Installation

### Prérequis

- Python 3.10 ou supérieur
- Les dépendances du projet

### Installation des dépendances

**Avec uv (recommandé) :**
```bash
uv pip install -r requirements.txt
```

> **Note pour utilisateurs de pyenv :**
> ```bash
> uv pip install --python python3 -r requirements.txt
> ```

**Ou avec pip :**
```bash
pip install -r requirements.txt
```

### Rendre le serveur exécutable

```bash
chmod +x mcp_server.py
```

## Configuration

### Pour Claude Desktop

Ajoutez cette configuration à votre fichier de configuration Claude Desktop :

**Sur macOS :**
`~/Library/Application Support/Claude/claude_desktop_config.json`

**Sur Windows :**
`%APPDATA%\Claude\claude_desktop_config.json`

**Sur Linux :**
`~/.config/Claude/claude_desktop_config.json`

**Configuration :**
```json
{
  "mcpServers": {
    "disclose-data": {
      "command": "python",
      "args": ["/chemin/absolu/vers/mcp_server.py"],
      "env": {}
    }
  }
}
```

OU avec uv :
```json
{
  "mcpServers": {
    "disclose-data": {
      "command": "uv",
      "args": ["run", "--python", "python3", "/chemin/absolu/vers/mcp_server.py"],
      "env": {}
    }
  }
}
```

Remplacez `/chemin/absolu/vers/` par le chemin complet vers le répertoire du projet.

### Pour d'autres clients MCP

Consultez la documentation de votre client MCP pour savoir comment configurer un serveur externe.

## Outils disponibles

Le serveur MCP expose 5 outils principaux :

### 1. `search_documents`

Rechercher des documents avec des filtres optionnels.

**Paramètres :**
- `keyword` (optionnel) : Mot-clé à rechercher (ex: "éolien", "lithium")
- `authority` (optionnel) : Autorité environnementale
- `department` (optionnel) : Code département (ex: "75", "35")
- `category` (optionnel) : Catégorie ("Avis", "Cadrage", "Cas par Cas")
- `from_date` (optionnel) : Date de début (format: YYYY-MM-DD)
- `to_date` (optionnel) : Date de fin (format: YYYY-MM-DD)
- `limit` (optionnel) : Nombre max de résultats (défaut: 10)

**Exemple d'utilisation dans Claude :**
> "Recherche tous les documents sur l'éolien en Bretagne"

### 2. `get_document`

Récupérer les détails d'un document spécifique.

**Paramètres :**
- `document_id` (requis) : ID du document DocumentCloud

**Exemple :**
> "Récupère les détails du document avec l'ID 123456"

### 3. `get_statistics`

Obtenir des statistiques sur la collection.

**Paramètres :**
- `department` (optionnel) : Limiter à un département
- `year` (optionnel) : Limiter à une année (format: YYYY)

**Exemple :**
> "Donne-moi les statistiques pour l'année 2024"

### 4. `list_authorities`

Lister les autorités environnementales disponibles.

**Paramètres :**
- `limit` (optionnel) : Nombre d'autorités à retourner (défaut: 20)

**Exemple :**
> "Liste les 10 autorités environnementales avec le plus de documents"

### 5. `get_document_text`

Récupérer le texte complet d'un document (OCR).

**Paramètres :**
- `document_id` (requis) : ID du document
- `page` (optionnel) : Numéro de page spécifique

**Exemple :**
> "Récupère le texte de la page 5 du document 123456"

## Tests

### Test en ligne de commande

Vous pouvez tester le serveur directement :

```bash
python mcp_server.py
```

Le serveur démarre et attend des commandes via stdin/stdout (protocole MCP).

### Test avec un client MCP

Le moyen le plus simple de tester est d'utiliser Claude Desktop après configuration.

## Exemples d'utilisation avec Claude

Une fois le serveur configuré dans Claude Desktop, vous pouvez poser des questions naturelles :

**Recherche simple :**
> "Trouve-moi des documents sur les projets éoliens"

**Recherche avec filtres :**
> "Recherche tous les avis environnementaux publiés par la Préfecture de Bretagne en 2024"

**Analyse géographique :**
> "Combien de documents concernent Paris (département 75) ?"

**Récupération de texte :**
> "Récupère et analyse le texte du document 123456"

**Statistiques :**
> "Donne-moi des statistiques sur les documents de 2023"

## Dépannage

### Erreur : "Module 'mcp' not found"

Assurez-vous que toutes les dépendances sont installées :
```bash
uv pip install -r requirements.txt
```

### Erreur : "python: command not found" (avec pyenv)

Utilisez :
```json
{
  "mcpServers": {
    "disclose-data": {
      "command": "python3",
      "args": ["/chemin/absolu/vers/mcp_server.py"]
    }
  }
}
```

Ou configurez pyenv :
```bash
pyenv global 3.12.4
```

### Le serveur ne démarre pas dans Claude Desktop

1. Vérifiez que le chemin vers `mcp_server.py` est **absolu** (commence par `/` sur macOS/Linux ou `C:\` sur Windows)
2. Vérifiez que le fichier est exécutable : `chmod +x mcp_server.py`
3. Testez le serveur en ligne de commande d'abord
4. Consultez les logs de Claude Desktop pour voir les erreurs

### Pas de résultats

L'API DocumentCloud peut être lente. Soyez patient lors des premières requêtes.

## Architecture technique

Le serveur MCP :
- Utilise le SDK MCP Python officiel
- Communique via stdin/stdout (protocole MCP standard)
- Interroge l'API DocumentCloud en temps réel
- Ne stocke pas de données localement
- Gère automatiquement la pagination pour les grandes requêtes

## Sécurité

- Le serveur est en lecture seule (aucune modification de données possible)
- Aucune authentification requise (données publiques)
- Pas de stockage de données personnelles
- Conformité avec les conditions d'utilisation de DocumentCloud

## Performances

- Les recherches simples : ~1-3 secondes
- Les statistiques (500 docs) : ~5-10 secondes
- Récupération de texte : ~2-5 secondes par document

Pour de meilleures performances, utilisez des filtres spécifiques.

## Développement

### Ajouter un nouvel outil

1. Ajoutez la définition de l'outil dans `list_tools()`
2. Implémentez la fonction de traitement dans `call_tool()`
3. Créez une fonction async dédiée (ex: `my_tool_tool()`)
4. Mettez à jour cette documentation

### Logs

Les logs sont disponibles dans la sortie standard. Niveau par défaut : INFO.

Pour activer le mode debug :
```python
logging.basicConfig(level=logging.DEBUG)
```

## Support

Pour des questions ou des problèmes :
- Consultez la [documentation principale](README.md)
- Ouvrez une issue sur GitHub
- Contactez : data@disclose.ngo

## Ressources

- [Documentation MCP](https://modelcontextprotocol.io/)
- [SDK MCP Python](https://github.com/modelcontextprotocol/python-sdk)
- [API DocumentCloud](https://www.documentcloud.org/help/api/)
- [Documentation Disclose Data](README.md)
