from flask import Flask, render_template
# initialisiere Flask-Server
app = Flask(__name__)
# definiere Route für Hauptseite
@app.route('/')
def index():
 # gebe Antwort an aufrufenden Client zurück
 return render_template('index.html')

@app.route('/eingaenge')
def eingaenge():
    return render_template('eingaenge.html')

@app.route('/ausgaenge')
def ausgaenge():
    return render_template('ausgaenge.html')
    
if __name__ == '__main__':
 # starte Flask-Server
 app.run(host='0.0.0.0', port=5000)
 