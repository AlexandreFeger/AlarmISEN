import bluetooth
import time
from machine import Pin
from bluetooth import UUID

# === Initialisation BLE ===
ble = bluetooth.BLE()
ble.active(True)

# === Capteur PIR et Buzzer ===
capteur = Pin("D3", Pin.IN)
buzzer = Pin("D2", Pin.OUT)

# === BLE UART Config ===
DEVICE_NAME = "WB55_MATTHIEU"
UART_SERVICE_UUID = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
TX_CHAR_UUID = bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E")
RX_CHAR_UUID = bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E")

UART_SERVICE = (
    UART_SERVICE_UUID,
    (
        (TX_CHAR_UUID, bluetooth.FLAG_READ | bluetooth.FLAG_NOTIFY),
        (RX_CHAR_UUID, bluetooth.FLAG_WRITE),
    ),
)

handles = ble.gatts_register_services([UART_SERVICE])
tx_handle, rx_handle = handles[0]

ADV_DATA = bytes([
    0x02, 0x01, 0x06,
    (len(DEVICE_NAME) + 1), 0x09]) + DEVICE_NAME.encode()

ble.gap_advertise(100, adv_data=ADV_DATA)
print(f"BLE actif : {DEVICE_NAME}")

conn_handle = None
buzzer_loop = False  #Activation/désactivation de la boucle buzzer

def bt_callback(event, data):
    global conn_handle, buzzer_loop
    if event == 1:
        conn_handle = data[0]
        print("Appareil connecte")
    elif event == 2:
        conn_handle = None
        buzzer_loop = False
        print("Appareil deconnecte")
    elif event == 3:
        message = ble.gatts_read(rx_handle).decode().strip()
        print(f"Message recu : {message}")
        if message == '1' :
            buzzer.value(1)
            print("Boucle buzzer activee !")
        elif message == '0':
            #buzzer_loop = False
            buzzer.value(0)
            print("Boucle buzzer arrêtee")

ble.irq(bt_callback)

# === Variable pour mémoriser l'état précédent du capteur
dernier_etat = -1

try:
    while True:
        if conn_handle is not None:
            # Mouvement PIR
            etat_actuel = capteur.value()
            if etat_actuel != dernier_etat:
                if etat_actuel == 1:
                    msg = "Mouvement détecte"
                    buzzer.value(1)
                else:
                    msg = "Pas de mouvement"
                    buzzer.value(0)
                print(f"{msg}")
                ble.gatts_notify(conn_handle, tx_handle, msg.encode())
                dernier_etat = etat_actuel

            #Buzzer infini si demandé
            if buzzer_loop:
                buzzer.value(1)
                time.sleep(1)
                buzzer.value(0)
                time.sleep(1)
            else:
                time.sleep(0.1)  #Petite pause pour la boucle principale

        else:
            buzzer.value(0)
            time.sleep(2)
            print("En attente de connexion BLE...")

except KeyboardInterrupt:
    ble.active(False)
    buzzer.value(0)
    print("Programme arrete")
