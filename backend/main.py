from flask import Flask, jsonify, request
from backend.handler.supply import SupplyHandler
from backend.handler.person import PersonHandler
from backend.handler.request import RequestHandler
from backend.handler.resource import ResourceHandler
from backend.handler.account import AccountHandler
from flask_cors import CORS

# Activate
app = Flask(__name__)
# Apply CORS to this app
CORS(app)

@app.route('/')
def greeting():
    return 'Hello, this is the JARR DB App!'


@app.route('/JARR-disaster-relief/person/<int:person_id>', methods=['GET', 'PUT', 'DELETE'])
def getPersonById(person_id):
    if request.method == 'GET':
        id_type = request.args.get('id_type', type=str)
        if id_type == 'person':
            return PersonHandler().get_person_by_id(person_id)
        elif id_type == 'supply':
            return PersonHandler().get_person_by_supply_id(person_id)
        else:
            return PersonHandler().get_person_by_request_id(person_id)
    elif request.method == 'PUT':
        return PersonHandler().update_person(person_id, request.form)
    elif request.method == 'DELETE':
        return PersonHandler().delete_person(person_id)
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

# __Supply__

@app.route('/JARR-disaster-relief/supplies', methods=['GET', 'POST'])
def getAllSupplies():
    if request.method == 'POST':
        return SupplyHandler().insert_supply_json(request.json)
    elif request.method == 'GET':
        if not request.args:
            return SupplyHandler().get_all_supplies()
        else:
            return SupplyHandler().search_supplies(request.args)
    else:
        return jsonify(Error="Method not allowed."), 405

@app.route('/JARR-disaster-relief/supplies/count')
def getTotalSupplyCount():
    return SupplyHandler().get_total_supplies()

@app.route('/JARR-disaster-relief/supplies/available/count')
def getTotalAvailableSupplyCount():
    return SupplyHandler().get_total_available_supplies()

@app.route('/JARR-disaster-relief/supplies/available')
def getAllAvailableSupplies():
    if not request.args:
        return SupplyHandler().get_all_available_supplies()
    else:
        return SupplyHandler().search_available_supplies(request.args)


@app.route('/JARR-disaster-relief/person/<int:person_id>/supplies')
def getSuppliesByPersonId(person_id):
    return SupplyHandler().get_supplies_by_person_id(person_id)

@app.route('/JARR-disaster-relief/person/<int:person_id>/supplies/available')
def getAvailableSuppliesByPersonId(person_id):
    return SupplyHandler().get_available_supplies_by_person_id(person_id)

# __Request__

@app.route('/JARR-disaster-relief/requests', methods=['GET', 'POST'])
def getAllRequests():
    if request.method == 'POST':
        return RequestHandler().insert_request_json(request.json)
    elif request.method == 'GET':
        if not request.args:
            return RequestHandler().get_all_requests()
        else:
            return RequestHandler().search_requests(request.args)
    else:
        return jsonify(Error="Method not allowed."), 405

@app.route('/JARR-disaster-relief/requests/count')
def getTotalRequestCount():
    return RequestHandler().get_total_requests()

@app.route('/JARR-disaster-relief/requests/needed/count')
def getTotalNeededRequestCount():
    return RequestHandler().get_total_needed_requests()

@app.route('/JARR-disaster-relief/requests/needed')
def getAllNeededRequests():
    if not request.args:
        return RequestHandler().get_all_needed_requests()
    else:
        return RequestHandler().search_needed_requests(request.args)


@app.route('/JARR-disaster-relief/person/<int:person_id>/requests')
def getRequestsByPersonId(person_id):
    return RequestHandler().get_requests_by_person_id(person_id)

@app.route('/JARR-disaster-relief/person/<int:person_id>/requests/needed')
def getNeededRequestsByPersonId(person_id):
    return RequestHandler().get_needed_requests_by_person_id(person_id)

#Resources
@app.route('/JARR-disaster-relief/resources/<int:resource_id>')
def getAllResources():
    return ResourceHandler().get_all_resources()

@app.route('/JARR-disaster-relief/resources/')
def getAllAvailableResource():
    return ResourceHandler().get_available_resource()


@app.route('/JARR-disaster-relief/resource/<int:person_id>')
def getResourceByPersonId(person_id):
    return ResourceHandler.get_resource_by_id(person_id)

@app.route('/JARR-disaster-relief/resource/count')
def getTotalResourceCount():
    return ResourceHandler().get_total_resource()

#Account
@app.route('/JARR-disaster-relief/account')
def getAccountData(account_id):
    return AccountHandler().get_account_data(account_id)

@app.route('/JARR-disaster-relief/person/<int:person_id>/resources')
def getAccountByPersonId(person_id):
    return AccountHandler().get_account_by_person_id(person_id)

@app.route('/JARR-disaster-relief/account/<int:account_id>')
def getAccountType(account_id):
    return AccountHandler().get_account_type(account_id)

@app.route('/JARR-disaster-relief/account/is_admin')
def getAdminAccount(is_admin):
    return AccountHandler().get_admin_account(is_admin)

if __name__ == '__main__':
    app.run()
