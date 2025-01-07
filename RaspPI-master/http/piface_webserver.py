#! /usr/bin/env python3

# Notwendige Bibliothek installieren:
#     sudo apt install python3-flask
# oder
#     pip3 install flask

from flask import Flask, render_template, request, redirect
import pifacedigitalio as p

p.init()
# initialisiere Flask-Server
app = Flask(__name__)

in1=[0]*4
# definiere Route für Hauptseite
@app.route('/')
def index():
    i=0
    for i in range(4):
        in1[i]=p.digital_read(i)
        if in1[i]==1:
            in1[i]='Ein'
        elif in1[i]==0:
            in1[i]='Aus' 
      
    return render_template('index.html',in1=in1)

@app.route('/websocket')
def websocket():      
    return render_template('piface_websocket.html')


listzustand=[0]*8

@app.route('/formular', methods=['POST'])
def formular():
    # gebe Antwort an aufrufenden Client zurück
    ausgang = request.form.get('Ausgang')
    zustand = request.form.get('Zustand')
    if ausgang:
        ausgang = int(ausgang)
    if zustand:
        zustand = int(zustand)
    listzustand[ausgang]=zustand
    p.digital_write(ausgang,zustand)
    return redirect('/')


if __name__ == '__main__':
    # starte Flask-Server im Debug-Modus
    app.debug = True
    app.run(threaded=False, host='0.0.0.0', port=5000)
