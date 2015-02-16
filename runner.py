__author__ = 'abought'

from app import app, socketio
import views

if __name__ == "__main__":
    #app.run()
    socketio.run(app)