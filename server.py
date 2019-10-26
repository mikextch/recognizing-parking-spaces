from os import environ
from dotenv import load_dotenv, find_dotenv
from flask import Flask, render_template,Response
from flask_socketio import SocketIO, emit
import pickle
from recognizing import videoDetection

lista_espacis = [0,1,0,0,1,0,1]

load_dotenv(find_dotenv())
app = Flask(__name__)

# Configuracion
app.config['SECRET_KEY'] = environ.get('SECRET_KEY')
app.config['DEBUG'] = True if environ.get('DEBUG') == 'True' else False
app.config['PORT'] = 80
# app.config['HOST'] =

# Socketio
DOMAIN = environ.get('DOMAIN')
DOMAIN_STREAM = "http://"+DOMAIN+"/stream"
socketio = SocketIO(app)
nuevo_usuario = ""

@app.route('/')
def home():
    return render_template(
        'home.html',
        domain=DOMAIN,
        dominio_stream=DOMAIN_STREAM
    )

@app.route('/stream')
def video_stream_reco():
    return Response(videoDetection.recognize(),mimetype='multipart/x-mixed-replace; boundary=frame')


@socketio.on('espacios')
def espacios(message):
    emit('recibido_espacios',{
        'espacios':lista_espacis
    }, broadcast=True)

# Iniciamos
if __name__ == '__main__':
    socketio.run(app,host="192.168.1.82")
