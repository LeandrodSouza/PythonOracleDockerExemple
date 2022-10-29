from flask import Flask
app = Flask(__name__)
import api.ProjectAPI as Ora


@app.route('/')
def home():
    return "Hey there!"

@app.route('/api')
def conect():
    return Ora.connection()

if __name__ == '__main__':
    from api import *
    app.run(host="0.0.0.0",port=5000,debug=True,use_reloader=True)
