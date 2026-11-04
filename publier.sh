#!/usr/bin/env bash
# Publie le site sur rivesenreves.com (GitHub Pages, branche gh-pages).
# Usage : ./publier.sh "message de mise à jour"
set -euo pipefail
cd "$(dirname "$0")"
MSG="${1:-Mise à jour du site}"
SITE="$(mktemp -d)"; GHP="$(mktemp -d)"
trap 'git worktree remove --force "$GHP" 2>/dev/null || true; rm -rf "$SITE"' EXIT
python3 build.py
RER_SORTIE="$SITE/out" python3 build.py >/dev/null
git checkout -q -- docs/photos-a-fournir.md 2>/dev/null || true
rm -f "$SITE/out/.htaccess"
echo "rivesenreves.com" > "$SITE/out/CNAME"
touch "$SITE/out/.nojekyll"
git fetch -q origin gh-pages
rmdir "$GHP"; git worktree add -q "$GHP" origin/gh-pages
cd "$GHP"
find . -mindepth 1 -maxdepth 1 ! -name .git -exec rm -rf {} +
cp -a "$SITE/out/." .
git add -A
if git diff --cached --quiet; then echo "Rien de nouveau à publier."; exit 0; fi
git commit -q -m "$MSG"
git push -q origin HEAD:gh-pages
echo "Publié sur https://rivesenreves.com"
