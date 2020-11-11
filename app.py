from flask import Flask
from wsgiref.simple_server import make_server

app = Flask(__name__)

@app.route('/api/v1/hello-world-11')
def hello_world():
    return 'Hello World №11!'

with make_server('', 8000, app) as server:
    print('http://127.0.0.1:8000/api/v1/hello-world-11')
    server.serve_forever()
