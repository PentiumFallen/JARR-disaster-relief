from flask import Flask, jsonify, request
from backend.handler.supply import SupplyHandler
from backend.handler.person import PersonHandler
from backend.handler.request import RequestHandler
from backend.handler.authentication import AuthenticationHandler
from flask_cors import CORS

# Activate
app = Flask(__name__)
# Apply CORS to this app
CORS(app)


@app.route('/')
def greeting():
    return 'Hello, this is the JARR DB App!'


@app.route('/JARR-disaster-relief/person/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def getPersonById(id):
    if request.method == 'GET':
        id_type = request.args.get('id_type', type=str)
        if id_type == 'person':
            return PersonHandler().get_person_by_id(id)
        elif id_type == 'supply':
            return PersonHandler().get_person_by_supply_id(id)
        else:
            return PersonHandler().get_person_by_request_id(id)
    elif request.method == 'PUT':
        return PersonHandler().update_person(id, request.form)
    elif request.method == 'DELETE':
        return PersonHandler().delete_person(id)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route('/JARR-disaster-relief/person/location/<int:person_id>', methods=['POST'])
def updatePersonLocation(person_id):
    if request.method == 'POST':
        return PersonHandler().update_person_location(request.json['new_location'], person_id)


@app.route('/JARR-disaster-relief/person', methods=['GET', 'POST'])
def getAllPersons():
    if request.method == 'POST':
        return PersonHandler().insert_person_json(request.json)
    else:
        if not request.args:
            return PersonHandler().get_all_persons()


@app.route('/JARR-disaster-relief/supplies', methods=['GET', 'POST'])
def getAllSupplies():
    if request.method == 'POST':
        return SupplyHandler().insert_supply_json(request.json)
    else:
        if not request.args:
            return SupplyHandler().get_all_supplies()
        else:
            return SupplyHandler().search_supply(request.args)


@app.route('/JARR-disaster-relief/person/<int:person_id>/supplies')
def getAllSuppliesOfPerson(person_id):
    return SupplyHandler().get_supplies_by_person_id(person_id)


@app.route('/JARR-disaster-relief/supplies/match')
def matchSuppliesToRequest():
    return SupplyHandler().match_supplies_to_request(request.args)


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


@app.route('/JARR-disaster-relief/authentication/login', methods=['GET'])
def getAccountLogin():
    if request.method == 'GET':
        return AuthenticationHandler().accountLogin(request.args)
    else:
        return jsonify(Error="Method not allowed"), 405


@app.route('/JARR-disaster-relief/authentication/password', methods=['GET'])
def getChangeAccountPassword():
    if request.method == 'GET':
        return AuthenticationHandler().accountChangePassword(request.args)
    else:
        return jsonify(Error="Method not allowed"), 405


@app.route('/JARR-disaster-relief/requests', methods=['GET', 'POST'])
def getAllRequests():
    if request.method == 'POST':
        return RequestHandler().insert_request_json(request.json)
    else:
        if not request.args:
            return RequestHandler.get_all_requests()
        else:
            return RequestHandler.search_request(request.args)


@app.route('/JARR-disaster-relief/requests/match')
def matchRequesttoSupplies():
    return RequestHandler.match_requests_to_supplies(request.args)


@app.route('/JARR-disaster-relief/requests/<int:supply_id>', methods=['GET', 'PUT', 'DELETE'])
def getRrequestById(request_id):
    if request.method == 'GET':
        return RequestHandler().get_request_by_id(request_id)
    elif request.method == 'PUT':
        return RequestHandler.update_request(request_id, request.form)
    elif request.method == 'DELETE':
        return RequestHandler.delete_request(request_id)
    else:
        return jsonify(Error="Method not allowed."), 405


if __name__ == '__main__':
    app.run()
