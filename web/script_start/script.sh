#!/bin/bash

cd "$(dirname "$0")"

# Activer l'environnement virtuel
source venv/bin/activate

# Exécuter les scripts Python avec leurs chemins relatifs
python3 xbee_module/xbee_receiver.py
python3 web/python_web/app.py
