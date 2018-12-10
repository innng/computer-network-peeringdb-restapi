#!/usr/bin/env python3

from flask import Flask
import json
from sys import argv

app = Flask(__name__)

# entrada
port = int(argv[1])
netfile = argv[2]
ixfile = argv[3]
netixlanfile = argv[4]

# abre os três arquivos
with open(netfile, 'r') as fout:
    fnet = json.load(fout)

with open(ixfile, 'r') as fout:
    fix = json.load(fout)

with open(netixlanfile, 'r') as fout:
    flan = json.load(fout)


# callback da página inicial
@app.route("/")
def hello():
    return ""


# callback do endpoint tipo 1
@app.route('/api/ix')
def ix():
    return json.dumps({'data': fix['data']})


# callback do endpoint tipo 2
@app.route('/api/ixnets/<ix_id>')
def net(ix_id):
    lista = [x['net_id'] for x in flan['data'] if x['ix_id'] == int(ix_id)]
    return json.dumps({'data': lista})


# callback do endpoint tipo 3
@app.route('/api/netname/<net_id>')
def netixlan(net_id):
    lista = [x['name'] for x in fnet['data'] if x['id'] == int(net_id)]
    return json.dumps(lista[0])


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=port)
