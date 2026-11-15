#!/bin/bash
# Signiert die Kurzbefehle auf dem Mac, damit sie importiert werden können.
# Aufruf im Terminal:  cd ~/"Wissen Rettungsdienst/kurzbefehl" && bash signieren.sh
set -e
cd "$(dirname "$0")"
for n in "Wissen" "Wissen vorlesen"; do
  rm -f "$n.shortcut"
  shortcuts sign --mode anyone --input "$n.unsigned.shortcut" --output "$n.shortcut"
  echo "✅ $n.shortcut signiert"
done
echo "Jetzt im Finder doppelt auf „Wissen.shortcut“ und „Wissen vorlesen.shortcut“ klicken."
