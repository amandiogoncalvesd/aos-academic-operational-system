#!/usr/bin/env bash
# Commit + push para o GitHub. Uso: GH_TOKEN=... ./scripts/deploy.sh "mensagem do commit"
set -euo pipefail
cd "$(dirname "$0")/.."
MSG="${1:-chore: update}"
: "${GH_TOKEN:?Defina GH_TOKEN}"
rm -f services/core/*.db
git add -A
git diff --cached --quiet && { echo "Nada para enviar."; exit 0; }
git commit -q -m "$MSG"
git push -q "https://amandiogoncalvesd:${GH_TOKEN}@github.com/amandiogoncalvesd/aos-academic-operational-system.git" HEAD:main
echo "✓ $(git rev-parse --short HEAD) → github.com/amandiogoncalvesd/aos-academic-operational-system"
