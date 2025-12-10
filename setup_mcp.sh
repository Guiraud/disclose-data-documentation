#!/bin/bash
# Script d'installation du serveur MCP Disclose Data pour Claude Desktop

set -e

echo "🚀 Configuration du serveur MCP Disclose Data"
echo "=============================================="
echo ""

# Déterminer le chemin absolu du projet
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MCP_SERVER_PATH="$PROJECT_DIR/mcp_server.py"

echo "📁 Chemin du projet détecté : $PROJECT_DIR"
echo ""

# Vérifier que mcp_server.py existe
if [ ! -f "$MCP_SERVER_PATH" ]; then
    echo "❌ Erreur : mcp_server.py introuvable"
    exit 1
fi

# Rendre le serveur exécutable
chmod +x "$MCP_SERVER_PATH"
echo "✓ mcp_server.py rendu exécutable"

# Déterminer le chemin de configuration selon l'OS
if [[ "$OSTYPE" == "darwin"* ]]; then
    CONFIG_DIR="$HOME/Library/Application Support/Claude"
    OS_NAME="macOS"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    CONFIG_DIR="$HOME/.config/Claude"
    OS_NAME="Linux"
else
    echo "❌ Système d'exploitation non supporté : $OSTYPE"
    echo "Veuillez configurer manuellement avec les instructions dans MCP_SERVER.md"
    exit 1
fi

CONFIG_FILE="$CONFIG_DIR/claude_desktop_config.json"

echo ""
echo "🔍 Système détecté : $OS_NAME"
echo "📝 Fichier de configuration : $CONFIG_FILE"
echo ""

# Vérifier quelle version de Python utiliser
PYTHON_CMD=""
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "❌ Python introuvable. Veuillez installer Python 3.10+"
    exit 1
fi

PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
echo "✓ Python détecté : $PYTHON_CMD (version $PYTHON_VERSION)"

# Vérifier que les dépendances sont installées
echo ""
echo "🔍 Vérification des dépendances..."

if ! $PYTHON_CMD -c "import mcp" 2>/dev/null; then
    echo "⚠️  Module 'mcp' non trouvé"
    echo ""
    read -p "Voulez-vous installer les dépendances maintenant ? (o/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[OoYy]$ ]]; then
        if command -v uv &> /dev/null; then
            echo "📦 Installation avec uv..."
            uv pip install -r "$PROJECT_DIR/requirements.txt"
        else
            echo "📦 Installation avec pip..."
            $PYTHON_CMD -m pip install -r "$PROJECT_DIR/requirements.txt"
        fi
    else
        echo "⚠️  Installez les dépendances manuellement avant de continuer"
        exit 1
    fi
fi

echo "✓ Dépendances vérifiées"

# Créer le répertoire de configuration si nécessaire
if [ ! -d "$CONFIG_DIR" ]; then
    echo ""
    echo "⚠️  Le répertoire de configuration Claude n'existe pas : $CONFIG_DIR"
    echo "Assurez-vous que Claude Desktop est installé."
    read -p "Voulez-vous créer le répertoire ? (o/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[OoYy]$ ]]; then
        mkdir -p "$CONFIG_DIR"
        echo "✓ Répertoire créé"
    else
        exit 1
    fi
fi

# Générer la configuration
NEW_CONFIG=$(cat <<EOF
{
  "mcpServers": {
    "disclose-data": {
      "command": "$PYTHON_CMD",
      "args": ["$MCP_SERVER_PATH"],
      "env": {}
    }
  }
}
EOF
)

echo ""
echo "📝 Configuration générée :"
echo "$NEW_CONFIG"
echo ""

# Sauvegarder ou fusionner avec la configuration existante
if [ -f "$CONFIG_FILE" ]; then
    echo "⚠️  Un fichier de configuration existe déjà"
    echo ""
    echo "Options :"
    echo "  1) Sauvegarder l'ancien et créer un nouveau"
    echo "  2) Afficher les instructions pour fusion manuelle"
    echo "  3) Annuler"
    echo ""
    read -p "Votre choix (1-3) : " -n 1 -r
    echo

    case $REPLY in
        1)
            BACKUP_FILE="$CONFIG_FILE.backup.$(date +%Y%m%d_%H%M%S)"
            cp "$CONFIG_FILE" "$BACKUP_FILE"
            echo "✓ Sauvegarde créée : $BACKUP_FILE"
            echo "$NEW_CONFIG" > "$CONFIG_FILE"
            echo "✓ Nouvelle configuration écrite"
            ;;
        2)
            echo ""
            echo "Ajoutez cette section dans $CONFIG_FILE :"
            echo ""
            echo "$NEW_CONFIG" | grep -A 6 '"disclose-data"'
            echo ""
            exit 0
            ;;
        *)
            echo "Installation annulée"
            exit 0
            ;;
    esac
else
    echo "$NEW_CONFIG" > "$CONFIG_FILE"
    echo "✓ Configuration créée"
fi

echo ""
echo "✅ Installation terminée !"
echo ""
echo "📖 Prochaines étapes :"
echo "  1. Redémarrez Claude Desktop"
echo "  2. Vérifiez que le serveur MCP 'disclose-data' est disponible"
echo "  3. Essayez : 'Trouve-moi des documents sur l'éolien'"
echo ""
echo "📚 Documentation complète : $PROJECT_DIR/MCP_SERVER.md"
