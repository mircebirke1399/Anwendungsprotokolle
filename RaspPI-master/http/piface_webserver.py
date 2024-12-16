#! /usr/bin/env python3

# Notwendige Bibliothek installieren:
#     sudo apt install python3-flask
# oder
#     pip3 install flask

from flask import Flask, render_template, request
import pifacedigitalio as p

p.init()
# initialisiere Flask-Server
app = Flask(__name__)


# definiere Route für Hauptseite
@app.route('/')
def index():
    in1=p.digital_read(0)
    in2=p.digital_read(1)
    in3=p.digital_read(2)
    in4=p.digital_read(3)   
    return render_template('index.html',in1=in1,in2=in2,in3=in3,in4=in4)

@app.route('/formular', methods=['POST'])
def formular():
    # gebe Antwort an aufrufenden Client zurück
    ausgang = request.form.get('Ausgang')
    zustand = request.form.get('Zustand')
    if ausgang:
        ausgang = int(ausgang)
    if zustand:
        zustand = int(zustand)
        
    if request.form.get('Zustand') == '1': 
        p.digital_write(ausgang,zustand)
    elif request.form.get('zustand') == '0':
        p.digital_write(ausgang,zustand)
    


if __name__ == '__main__':
    # starte Flask-Server im Debug-Modus
    app.debug = True
    app.run(threaded=False, host='0.0.0.0', port=5000)
