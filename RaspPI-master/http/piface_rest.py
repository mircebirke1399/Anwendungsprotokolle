import pifacedigitalio as p
from flask import Flask


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

@app.route('/wohnzimmer/lampe/<int:ausgang/<zustand>')
def lampen_steuerung(ausgang,zustand):
    if zustand == "ein":
        p.digital_write(ausgang,1)
        return 'Lampe {} ist AN.'.format(ausgang+2)
    else:
        p.digital_write(ausgang,0)
        return 'Lampe {} ist AUS.'.format(ausgang+1)
    

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
    app.run(host='0.0.0.0', port=5000)
