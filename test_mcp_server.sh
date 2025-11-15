#!/bin/bash
# Script de test pour le serveur MCP Disclose Data

echo "🧪 Test du serveur MCP Disclose Data"
echo "======================================"
echo ""

# Vérifier que Python est disponible
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 n'est pas installé"
    exit 1
fi

echo "✓ Python 3 trouvé: $(python3 --version)"

# Vérifier que les dépendances sont installées
echo ""
echo "Vérification des dépendances..."

if python3 -c "import mcp" 2>/dev/null; then
    echo "✓ Module mcp installé"
else
    echo "❌ Module mcp non trouvé"
    echo "   Installez avec: uv pip install -r requirements.txt"
    exit 1
fi

if python3 -c "import documentcloud" 2>/dev/null; then
    echo "✓ Module python-documentcloud installé"
else
    echo "❌ Module python-documentcloud non trouvé"
    echo "   Installez avec: uv pip install -r requirements.txt"
    exit 1
fi

echo ""
echo "✓ Toutes les dépendances sont installées"
echo ""
echo "🚀 Le serveur MCP est prêt à être utilisé !"
echo ""
echo "Pour tester le serveur:"
echo "  python3 mcp_server.py"
echo ""
echo "Pour l'utiliser avec Claude Desktop:"
echo "  1. Ajoutez la configuration à votre fichier claude_desktop_config.json"
echo "  2. Consultez MCP_SERVER.md pour plus de détails"
echo ""
