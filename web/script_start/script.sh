#!/bin/bash

# Se déplacer dans le répertoire du script
cd "$(dirname "$0")"

# Activer l'environnement virtuel
source venv/bin/activate

# Exécuter les scripts Python avec sudo en arrière-plan
sudo python3 xbee_module/xbee_receiver.py &
sudo python3 web/python_web/app.py &
