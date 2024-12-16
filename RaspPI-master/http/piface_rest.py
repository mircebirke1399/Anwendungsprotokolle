import pifacedigitalio as p
from flask import Flask, render_template


# initialisiere PiFace
p.init()

# initialisiere Flask server
app = Flask(__name__)


@app.route('/')
def info():
    return 'PiFace HTTP-Schnittstelle'

@app.route('/<name>')
def hello(name):
    return 'Hallo {}!'.format(name)

@app.route('/wohnzimmer/lampe/<int:ausgang>/<zustand>')
def lampen_steuerung(ausgang,zustand):
    if zustand == "ein":
        p.digital_write(ausgang,1)
        return 'Lampe {} in Wohnzimmer ist AN.'.format(ausgang+1)
    elif zustand == "aus":
        p.digital_write(ausgang,0)
        return 'Lampe {} in Wohnzimmer ist AUS.'.format(ausgang+1)
    else:
        return '{} ist kein richtiger Zustand'.format(zustand)



@app.route('/eingang/<int:eingang>')
def eingang_auslesen(eingang):
    wert = p.digital_read(eingang)
    if wert:
       return 'Eingang ist: EIN.'
    else:
       return 'Eingang ist: AUS.'

if __name__ == '__main__':
    # starte Flask-Server im Debug-Modus
    app.debug = True
    app.run(threaded=False, host='0.0.0.0', port=5000)
