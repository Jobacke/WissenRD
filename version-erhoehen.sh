#!/bin/bash
# Erhöht die Versionsnummer an allen Stellen und schreibt einen Eintrag ins CHANGELOG.
# Aufruf:   ./version-erhoehen.sh "Kurzbeschreibung der Änderung"            → 1.0.0 → 1.0.1
#           ./version-erhoehen.sh "Neue Funktion XY" minor                   → 1.0.1 → 1.1.0
#           ./version-erhoehen.sh "Großer Umbau" major                       → 1.1.0 → 2.0.0
# Danach:   git add -A && git commit -m "vX.Y.Z" && git push
set -e
cd "$(dirname "$0")"
TEXT="${1:?Bitte eine Beschreibung angeben, z. B. ./version-erhoehen.sh \"Suche verbessert\"}"
ART="${2:-patch}"

ALT=$(sed -n 's/.*APP_VERSION = "\(.*\)".*/\1/p' js/version.js)
BUILD=$(sed -n 's/.*APP_BUILD = \([0-9]*\).*/\1/p' js/version.js)
IFS=. read -r MA MI PA <<< "$ALT"
case "$ART" in
  major) MA=$((MA+1)); MI=0; PA=0 ;;
  minor) MI=$((MI+1)); PA=0 ;;
  *)     PA=$((PA+1)) ;;
esac
NEU="$MA.$MI.$PA"; NBUILD=$((BUILD+1)); HEUTE=$(date +%F)

# macOS- und Linux-kompatibles sed
sedi() { if sed --version >/dev/null 2>&1; then sed -i "$@"; else sed -i '' "$@"; fi; }
sedi "s/APP_VERSION = \".*\"/APP_VERSION = \"$NEU\"/" js/version.js
sedi "s/APP_BUILD = [0-9]*/APP_BUILD = $NBUILD/" js/version.js
sedi "s/APP_DATUM = \".*\"/APP_DATUM = \"$HEUTE\"/" js/version.js
sedi "s/const CACHE = \".*\"/const CACHE = \"wissen-rd-$NEU-b$NBUILD\"/" sw.js

{ head -n 2 CHANGELOG.md; printf "## v%s (Build %s) – %s\n- %s\n\n" "$NEU" "$NBUILD" "$HEUTE" "$TEXT"; tail -n +3 CHANGELOG.md; } > CHANGELOG.tmp
mv CHANGELOG.tmp CHANGELOG.md

echo "✅ Version $ALT → $NEU (Build $NBUILD)"
