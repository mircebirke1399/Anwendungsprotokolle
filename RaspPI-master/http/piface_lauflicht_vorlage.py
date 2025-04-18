#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# piface_lauflicht_vorlage.py
#---------------------------------------------------
# Steuert ein Lauflicht auf dem PiFace
# über eine Web-Oberfläche
#---------------------------------------------------
# Autor: Walter Rothlin
# Datum: 14.2.2021
#---------------------------------------------------
# Anleitung:
# - Skript auf dem Raspberry Pi speichern
# - Skript ausführen
# - In Web-Browser die Seite http://<IP-Adresse-des-Raspberry>:5000/ aufrufen
# - Geschwindigkeit des Lauflichts einstellen
#---------------------------------------------------

# Notwendige Bibliothek installieren:
#     sudo apt install python3-flask
# oder
#     pip3 install flask

import time
import threading
import pifacedigitalio as p

from flask import Flask
from flask import request

p.init()
# TODO: Bibliothek zur Ansteuerung des PiFace importieren und PiFace initialisieren

# initialisiere Flask server
app = Flask(__name__)

# globale Variable zur Speicherung der aktuellen Lauflicht-Geschwindigkeit
aktuelle_geschwindigkeit = 100

# HTML-Formular
formular = """
           <html>
           <body>
           <h1>Lauflicht mit dem PiFace</h1>
           <form action="/lauflicht" method="POST">
             <p><input type="number" name="geschwindigkeit" min="10" max="1000" value="{geschwindigkeit}" /> Geschwindigkeit [ms] </p>
             <p><input type="submit" value="Absenden" /></p>
           </form>
           </body>
           </html>
           """

@app.route('/lauflicht', methods=['GET', 'POST'])
def lauflicht_html():
    global aktuelle_geschwindigkeit
    if request.method == 'POST':
        aktuelle_geschwindigkeit = int(request.form['geschwindigkeit'])
        print('Geschwindigkeit geändert zu: {}'.format(aktuelle_geschwindigkeit))
        return formular.format(geschwindigkeit=aktuelle_geschwindigkeit)
    else:
        return formular.format(geschwindigkeit=aktuelle_geschwindigkeit)

def lauflicht_steuerung():
    global aktuelle_geschwindigkeit
    aktuelle_Ausgabe = 0
    aktuelle_Richtung = 0
    
    while True:
        # TODO: Schreibe aktuellen Wert auf Ausgang
        if aktuelle_Richtung==0:
            if aktuelle_Ausgabe==0:
                p.digital_write(aktuelle_Ausgabe,1)
                aktuelle_Ausgabe+=1
            elif aktuelle_Ausgabe > 0 and aktuelle_Ausgabe <7:
                p.digital_write(aktuelle_Ausgabe-1,0)
                p.digital_write(aktuelle_Ausgabe,1)
                aktuelle_Ausgabe+=1
            elif aktuelle_Ausgabe ==7:
                p.digital_write(aktuelle_Ausgabe,1)
                p.digital_write(aktuelle_Ausgabe-1,0)
                aktuelle_Ausgabe-=1
                aktuelle_Richtung=1
        elif aktuelle_Richtung==1:
            if aktuelle_Ausgabe==7:
                p.digital_write(aktuelle_Ausgabe,1)
                aktuelle_Ausgabe_=1
            elif aktuelle_Ausgabe > 0 and aktuelle_Ausgabe <7:
                p.digital_write(aktuelle_Ausgabe+1,0)
                p.digital_write(aktuelle_Ausgabe,1)
                aktuelle_Ausgabe-=1
            elif aktuelle_Ausgabe==0:
                p.digital_write(aktuelle_Ausgabe+1,0)
                p.digital_write(aktuelle_Ausgabe,1)
                aktuelle_Ausgabe+=1
                aktuelle_Richtung=0
        print('laufe mit Geschwindigkeit {}'.format(aktuelle_geschwindigkeit))
        time.sleep(aktuelle_geschwindigkeit / 1000.)

if __name__ == '__main__':
    # starte Hintergrund-Thread für das Lauflicht
    thread = threading.Thread(target=lauflicht_steuerung, args=())
    thread.daemon = True
    thread.start()
    # starte Web-Server zur Steuerung des Lauflichts
    app.run(host= '0.0.0.0', port=5000, debug=True, use_reloader=False)
