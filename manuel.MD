# Manuel d'Installation du Projet **AirNode**

## 1) Brève Description du Projet
Le projet **AirNode** est un réseau de capteurs de qualité de l'air capable de mesurer la **température**, l'**humidité** et le **taux de CO2** dans un environnement donné. Les capteurs (**nœuds**) utilisent des modules **XBee** pour communiquer les données vers une **unité centrale**. Cette unité centrale stocke les données dans une **base SQLite** et fournit une **interface web** permettant la visualisation en temps réel des mesures.

---
## 2) Matériel Utilisé et Coût

### Matériel pour un Nœud Capteur de Qualité d'Air (~118,6 €)
| **Composant**                                  | **Prix**    |
|-----------------------------------------------|------------:|
| Carte **Arduino UNO**                         | ~20 €     |
| Module **UartSbee V5.0**                      | ~5 €      |
| Module **XBee Pro S5** avec antenne           | ~33,60 €  |
| Module **SCD30** (capteur CO2/temp/humidité)  | ~50 €     |
| Module **Logic Level Converter** 3.3V - 5V    | ~5 €      |
| Breadboard                                    | ~5 €      |
| Câbles                                       | ~5 €      |

### Matériel pour l'Unité Centrale (~103,6 €)
| **Composant**                                  | **Prix**    |
|-----------------------------------------------|------------:|
| Carte **Raspberry Pi 3**                      | ~55 €     |
| Carte **SD 16 Go**                            | ~10 €     |
| Lecteur de **Carte SD**                       | ~8 €      |
| Module **UartSbee V5.0**                      | ~5 €      |
| Module **XBee Pro S5** avec antenne           | ~33,60 €  |
| Breadboard                                    | ~5 €      |
| Câbles                                       | ~5 €      |

---
## 3) Prérequis
Avant de commencer, assurez-vous d'avoir installé les outils suivants :

1. **XCTU** : Logiciel pour configurer les modules **XBee**. [Télécharger XCTU](https://www.digi.com/products/embedded-systems/digi-xbee/digi-xbee-tools/xctu).
2. **PlatformIO** : Plateforme de développement pour Arduino. Vous pouvez :
   - L'installer via l'**onglet Extensions** dans **Visual Studio Code**.
   - La télécharger directement depuis le [site officiel](https://platformio.org/).
3. **Raspbian** : Système d'exploitation pour la Raspberry Pi.
4. **Python 3** et **pip3** : Nécessaire pour exécuter les scripts sur la Raspberry Pi.
5. **Carte SD** : Pour installer Raspbian sur la Raspberry Pi.
6. **Lecteur de carte SD** : Pour configurer l'OS sur la carte SD.

---
## 4) Configuration des Modules XBee

### 4.1) Installation de XCTU
1. Téléchargez et installez **XCTU** depuis le site officiel.
2. Connectez votre module **XBee** à votre ordinateur via un adaptateur USB.

### 4.2) Configuration des Modules XBee
1. Lancez **XCTU**.
2. Ajoutez le port série du module **XBee**.
3. Configurez les paramètres suivants :
   - **PAN ID** : Choisissez un identifiant unique (ex. `1234`).
   - **Baudrate** : `9600`.
   - **CH** (Channel) : Configurez-le sur un canal libre (ex. `C`).
   - **Encryption** : Activez le chiffrement avec **AES 128-bit**.
   - **Key** : Spécifiez une clé commune pour sécuriser la communication (ex. `0x1234567890ABCDEF`).
   - **Mode de Fonctionnement** :
     - Configurez un module XBee en **émetteur** (TX) et les autres en **récepteurs** (RX).
      - Si possible, activez le **mode DigiMesh** pour permettre aux modules XBee d'agir à la fois comme émetteurs et récepteurs, ce qui permet de relayer automatiquement les données entre nœuds, d'établir un maillage résilient et d'augmenter la portée du réseau.

   **Remarque** : Tous les modules XBee ne prennent pas en charge tous les protocoles de communication listés. La combinaison du matériel XBee et du firmware radio détermine le protocole qu'un module XBee peut exécuter. Pour plus d'informations sur les modules RF XBee disponibles et les protocoles qu'ils supportent, consultez la [XBee RF Family Comparison Matrix](https://www.digi.com/resources/documentation/digidocs/pdfs/90001506.pdf).

   - ![image](wiki/img/xctu/protocol.png)

4. Appliquez les modifications et vérifiez la communication entre deux modules **XBee** avec XCTU.

---
## 5) Installation et Configuration

### 5.1) Installation du Nœud (Capteur de Qualité d'Air)

#### 1. **Connexion des Composants**
Connectez les composants suivants :
- Le **module XBee Shield** à l'Arduino UNO pour la communication sans fil.
- Le **SparkFun Logic Level Converter** pour gérer les signaux entre 3.3V et 5V.
- Les autres capteurs et modules nécessaires, en suivant les spécifications de leurs documentations respectives.

Assurez-vous de bien relier les broches **GND** et d'alimenter correctement les composants en **3.3V** ou **5V**, selon leurs besoins.

#### 2. **Configuration du Code Arduino**
Clonez le projet **AirNode** et accédez au dossier correspondant :

1. **Cloner le projet AirNode** :
   ```sh
   git clone <URL_du_repo_AirNode>
   cd AirNode/nodes/AirSensor
   ```

2. **Ouvrir le projet PlatformIO** :
   Dans le dossier `AirNode/nodes/AirSensor`, un projet PlatformIO est déjà configuré. Ouvrez-le dans **Visual Studio Code** :
   ```sh
   code .
   ```

3. **Modifier l'ID du module** :
   Ouvrez le fichier `main.cpp` et modifiez la variable `moduleID` pour chaque capteur :
   ```cpp
   String moduleID = "AirNode-1"; // ID du module
   ```

4. **Téléverser le code sur l'Arduino UNO** :
   Utilisez PlatformIO pour téléverser le code sur l'Arduino UNO en cliquant sur l'icône de flèche dans la barre d'outils de PlatformIO.

---
### 5.2) Installation de l'Unité Centrale (Raspberry Pi)

#### 1. **Préparation de la Raspberry Pi**
- **Formatez** la carte SD avec un logiciel comme **Balena Etcher** ou **Raspberry Pi Imager**.
- Téléchargez l'image **Raspbian** (Lite ou Desktop) depuis le site officiel.
- Écrivez l'image Raspbian sur la carte SD via le lecteur de carte.
- Insérez la carte SD dans la Raspberry Pi.
- Connectez la Raspberry Pi à Internet via un câble Ethernet ou Wi-Fi.

#### 2. **Installation des Dépendances**
   ```sh
   sudo apt-get update
   sudo apt-get install sqlite3 python3 python3-pip
   sudo pip3 install flask pyserial
   ```

#### 3. **Création de l'Environnement Virtuel Python**
Pour isoler les dépendances, créez un environnement virtuel Python :
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```
   **Note** : Chaque fois que vous exécutez un script, assurez-vous d'activer l'environnement virtuel avec `source venv/bin/activate`.

#### 4. **Création de la Base de Données SQLite**
Avant d'exécuter le script, créez la base de données SQLite avec la commande suivante :
   ```sh
   sqlite3 /home/pi/sqlite/xbee_data.db
   ```
   **Note** : Assurez-vous que le chemin `DB_PATH` est correctement spécifié dans le fichier `xbee_receiver.py` :
   ```python
   DB_PATH = "/home/pi/sqlite/xbee_data.db"
   ```

#### 5. **Configurer le Port Série GPIO**
Dans le fichier **xbee_receiver.py**, assurez-vous que le port série utilisé est correctement défini selon la connexion des broches GPIO sur la Raspberry Pi :
   ```python
   PORT = "/dev/ttyS0"  # À ajuster si nécessaire
   ```
   Vous pouvez vérifier les ports disponibles avec :
   ```sh
   ls /dev/tty*
   ```

#### 6. **Lancer le Script XBee Receiver en Arrière-Plan**
Pour exécuter le script **xbee_receiver.py** avec les droits administrateur et en arrière-plan :
   ```sh
   sudo python3 xbee_module/xbee_receiver.py &
   ```

#### 7. **Lancer le Serveur Web**
- Accédez au dossier du script :
   ```sh
   cd python_web/
   ```
- Lancez le script Flask :
   ```sh
   python3 app.py
   ```

---
## 6) Vérification et Dépannage
1. **Tester la Communication des XBee** : Utilisez XCTU pour vérifier les transmissions.
2. **Tester le Serveur Web** : Accédez à `http://<IP>:5000`.
3. **Logs d'Erreur** : Consultez les sorties pour le script XBee Receiver et Flask.

---
## 7) Conclusion
Vous disposez maintenant d'un **réseau AirNode** fonctionnel, capable de surveiller en temps réel la qualité de l'air et de fournir des visualisations via une interface web hébergée sur la Raspberry Pi.
