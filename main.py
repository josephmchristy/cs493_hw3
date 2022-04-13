from google.cloud import datastore
from flask import Flask, request
import json

from sqlalchemy import null
import constants

app = Flask(__name__)
client = datastore.Client()

@app.route('/')
def index():
    return "Please navigate to /slips to use this API"\

@app.route('/slips', methods=['POST','GET'])
def boats_get_post():
    if request.method == 'POST':
        content = request.get_json()
        new_slip = datastore.entity.Entity(key=client.key(constants.slips))
        new_slip.update({"number": content["number"]})
        new_slip.update({"current_boat": null})
        client.put(new_slip)
        return str(new_slip.key.id)
    elif request.method == 'GET':
        query = client.query(kind=constants.slips)
        results = list(query.fetch())
        for e in results:
            e["id"] = e.key.id
        return json.dumps(results)
    else:
        return 'Method not recognized'

@app.route('/slips/<id>', methods=['PUT','DELETE','GET'])
def slips_put_delete(id):
    if request.method == 'PUT':
        content = request.get_json()
        slip_key = client.key(constants.slips, int(id))
        slip = client.get(key=slip_key)
        slip.update({"number": content["number"]})
        client.put(slip)
        return ('',200)
    elif request.method == 'DELETE':
        key = client.key(constants.slips, int(id))
        client.delete(key)
        return ('',200)
    elif request.method == 'GET':
        slip_key = client.key(constants.slips, int(id))
        slip = client.get(key=slip_key)
        return json.dumps(slip)
    else:
        return 'Method not recognized'

@app.route('/boats', methods=['POST','GET'])
def boats_get_post():
    if request.method == 'POST':
        content = request.get_json()
        new_boat = datastore.entity.Entity(key=client.key(constants.boats))
        new_boat.update({"name": content["name"], "type": content["type"], "length": content["length"]})
        client.put(new_boat)
        return str(new_boat.key.id)
    elif request.method == 'GET':
        query = client.query(kind=constants.boats)
        results = list(query.fetch())
        for e in results:
            e["id"] = e.key.id
        return json.dumps(results)
    else:
        return 'Method not recognized'

@app.route('/boats/<id>', methods=['PUT','DELETE','GET'])
def slipss_put_delete(id):
    if request.method == 'PUT':
        content = request.get_json()
        boat_key = client.key(constants.boats, int(id))
        boat = client.get(key=boat_key)
        boat.update({"name": content["name"], "type": content["type"], "length": content["length"]})
        client.put(boat)
        return ('',200)
    elif request.method == 'DELETE':
        key = client.key(constants.boats, int(id))
        client.delete(key)
        return ('',200)
    elif request.method == 'GET':
        boat_key = client.key(constants.boats, int(id))
        boat = client.get(key=boat_key)
        return json.dumps(boat)
    else:
        return 'Method not recognized'

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)