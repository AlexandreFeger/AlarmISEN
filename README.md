# AlarmISEN
AlarmISEN pour projet IOT
Alarme connectée via BLE – Projet IoT ISEN

Ce projet a été réalisé dans le cadre d’un projet IoT à l’ISEN par  Alexandre Feger ,  Matthieu Astezan  et  Shainez Chaouch .

Il s'agit d'une alarme connectée fonctionnant avec un  capteur PIR , un  buzzer , et une communication  Bluetooth Low Energy (BLE) , pilotée depuis une application mobile développée avec  MIT App Inventor .

----> Contenu du projet

- `main.py` : script principal embarqué sur une carte  Nucleo WB55RG 
- `ble_advertising.py` : module helper pour générer les paquets de publicité BLE
- Application mobile (App Inventor) : interface de connexion BLE, bouton pour activer/désactiver l'alarme

----> Fonctionnement

----> Côté carte (MicroPython)

- Un  capteur PIR  détecte les mouvements (sur la broche D3)
- Un  buzzer  s'active ou se désactive via la broche D2
- La carte émet un signal BLE avec le nom  WB55_MATTHIEU 
- Elle écoute les messages BLE envoyés par l’application mobile :
  - `"1"` → active le buzzer
  - `"0"` → désactive le buzzer


----> Application mobile (MIT App Inventor)

L'application permet :
- De scanner et se connecter à l'appareil WB55_MATTHIEU
- D’activer/désactiver le buzzer à l’aide d’un bouton
- D’afficher l’état actuel (ON / OFF) dans un label


----> Explication du code

----> `main.py`

Ce fichier contient le cœur du système :

-  Initialisation BLE  : configure le Bluetooth LE et active la publicité.
-  Déclaration du service UART BLE  : avec 2 caractéristiques :
  - `TX_CHAR_UUID` pour envoyer des données à l'application
  - `RX_CHAR_UUID` pour recevoir des commandes
-  Connexion au capteur PIR  et au buzzer
-  Fonction `on_rx_write`  :
  - Reçoit les messages `"1"` ou `"0"` envoyés par le téléphone
  - Allume ou éteint le buzzer en conséquence
-  Boucle principale  : passive (`while True`) car l’interaction est pilotée par interruption BLE

----> `ble_advertising.py`

Ce fichier contient des  fonctions utilitaires  pour construire les  paquets de publicité BLE  :

- Permet de configurer dynamiquement :
  - Le nom de l'appareil
  - Les UUIDs diffusés
- Utilise le format BLE standard pour créer les paquets attendus par les smartphones

----> Communication BLE

-  Service UUID  : `6E400001-B5A3-F393-E0A9-E50E24DCCA9E`
-  TX Characteristic (carte → app)  : `6E400003-B5A3-F393-E0A9-E50E24DCCA9E`
-  RX Characteristic (app → carte)  : `6E400002-B5A3-F393-E0A9-E50E24DCCA9E`
- Utilisation de `gatts_notify` pour transmettre des messages côté carte
- Gestion des `Write` BLE pour réception de commandes depuis l'application

----> Dépendances

- MicroPython (port STM32 WB55)
- Modules : `bluetooth`, `machine`, `time`, `struct`
- Application Android créée avec  MIT App Inventor 


----> Équipe projet

-  Alexandre Feger 
-  Matthieu Astezan 
-  Shainez Chaouch 

---->  Prochaines améliorations possibles

- Ajout de notifications push si intrusion détectée
- Historique des détections
- Intégration d’un capteur sonore ou température
- Amélioration de l'interface mobile

----> Scénario de démo :

1. Lancer l'application mobile.
2. Scanner et se connecter à `WB55_MATTHIEU`.
3. Appuyer sur le bouton “Buzzer” :
   - Envoie `"1"` si le buzzer est éteint → il s’allume.
   - Envoie `"0"` si le buzzer est allumé → il s’éteint.
4. L'état actuel (`ON` ou `OFF`) est affiché dans le label de l’application.
5. L'utilisateur peut répéter l’opération autant de fois que nécessaire.

Ce système permet un  contrôle simple, sécurisé et distant  d’un système d’alarme par BLE.

---->  Licence

Projet réalisé dans un cadre académique – librement réutilisable à des fins pédagogiques.
