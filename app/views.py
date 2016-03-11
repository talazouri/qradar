__author__ = 'IBM'

import os
import json

from app import app
from flask import render_template
from flask import send_file
from flask import request
from flask import json
from flask import jsonify
from flask import url_for


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template("index.html")


@app.route('/<path:template>.html')
def send_template(template):
    template_file = '{0}.html'.format(os.path.join('', template))
    return send_file(template_file)


tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]


@app.route('/rest', methods=['GET'])
def rest():
    return 'rest'


@app.route('/rest/assets', methods=['GET'])
def assets():
    return jsonify({'tasks': tasks})

jsonAssets = '{ "Assets": [{ "id": "1", "ip": "1.2.3.4"},{"id": "2","ip": "2.3.4.5"},{"id": "3","ip": "3.4.5.6"}]}'


def getAsset(id):
    int_id = int(id)
    assets = json.loads(jsonAssets)
    json.dumps(assets, sort_keys=True, indent=4)
    return assets['Assets'][int_id]["ip"]


@app.route('/rest_api', methods=['GET', 'POST'])
def rest_api():
    if request.method == "GET":
        asset_id = request.args.get('id')
        return getAsset(asset_id)
    else:
        print "tmp"  # POST Method
    return render_template("index.html")