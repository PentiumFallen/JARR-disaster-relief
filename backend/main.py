from flask import Flask, jsonify, request
from backend.handler.supply import SupplyHandler
from flask_cors import CORS

# Activate
app = Flask(__name__)
# Apply CORS to this app
CORS(app)

@app.route('/')
def greeting():
    return 'Hello, this is the JARR DB App!'

@app.route('/JARR-disaster-relief/supplies', methods=['GET', 'POST'])
def getAllSupplies():
    if request.method == 'POST':
        return SupplyHandler().insert_supply_json(request.json)
    else:
        if not request.args:
            return SupplyHandler().get_all_supplies()
        else:
            return SupplyHandler().search_supply(request.args)

@app.route('/JARR-disaster-relief/supplies/<int:supply_id>', methods=['GET', 'PUT', 'DELETE'])
def getSupplyById(supply_id):
    if request.method == 'GET':
        return SupplyHandler().get_supply_by_id(supply_id)
    elif request.method == 'PUT':
        return SupplyHandler().update_supply(supply_id, request.form)
    elif request.method == 'DELETE':
        return SupplyHandler().delete_supply(supply_id)
    else:
        return jsonify(Error="Method not allowed."), 405

if __name__ == '__main__':
    app.run()