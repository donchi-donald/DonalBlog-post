#ich importieren Sie zuerst das Flask-Objekt aus dem flask-Paket.
from flask import Flask

#damit wird instanz mitgeteilt
app = Flask(__name__)

# Decorator, der eine reguläre Python-Funktion in eine Flask-Anzeigefunktion verwandelt.
@app.route('/')
def hello():
    return 'Hello World!'