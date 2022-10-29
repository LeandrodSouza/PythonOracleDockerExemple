from flask import Flask
import api.ConectorOracle as Ora
app = Flask(__name__)


@app.route('/')
def home():
    return "App run 🔥"


@app.route('/api')
def con():
    return Ora.connection()


if __name__ == '__main__':
    from api import *

    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=True)
