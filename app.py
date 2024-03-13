"""
Descripcion servicio
Last modification: 09-02-2023 - Giovanni Junco
"""
from api import app, socketio

if __name__ == '__main__':
    #start to all the IP of the VM port 5002
    app.run(debug=True, host="0.0.0.0",port=5002)
    socketio.run(app)
