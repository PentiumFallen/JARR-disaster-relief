from flask import Flask, jsonify, request

from backend.handler.fulfilledRequest import FulfilledRequestHandler
from backend.handler.purchasedSupply import PurchasedSupplyHandler
from backend.handler.supply import SupplyHandler
from backend.handler.person import PersonHandler
from backend.handler.request import RequestHandler
from backend.handler.resource import ResourceHandler
from backend.handler.account import AccountHandler
from backend.handler.address import AddressHandler
from backend.handler.authentication import Auth
from flask_cors import CORS

# Activate
app = Flask(__name__)
# Apply CORS to this app
CORS(app)


@app.route('/')
def greeting():
    return 'Hello, this is the JARR DB App!'


@app.route('/JARR-disaster-relief/signup', methods=['POST'])
def signup():
    return Auth().signup(request.form)


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


@app.route('/JARR-disaster-relief/person/location/<int:person_id>', methods=['PUT'])
def updatePersonDefaultAddress(person_id):
    if request.method == 'PUT':
        return AddressHandler().update_person_default_address(person_id, request.form)


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
        # Mutually exclusive
        if request.json is not None and request.form is None:
            return SupplyHandler().insert_supply_json(request.json)
        elif request.form is not None and request.json is None:
            return SupplyHandler().insert_supply(request.form)
        else:
            return jsonify(Error="Malformed post request."), 400
    elif request.method == 'GET':
        if not request.args:
            return SupplyHandler().get_all_supplies()
        else:
            return SupplyHandler().search_supplies(request.args)
    else:
        return jsonify(Error="Method not allowed."), 405


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


# __PurchasedSupply__

@app.route('/JARR-disaster-relief/purchase', methods=['GET', 'POST'])
def getPurchases():
    if request.method == 'POST':
        if request.json:
            return PurchasedSupplyHandler().insert_purchasedSupply_json(request.json)
        elif request.form:
            return PurchasedSupplyHandler().insert_purchasedSupply(request.form)
        else:
            return jsonify(Error="Data not found"), 405
    elif request.method == 'GET':
        return PurchasedSupplyHandler().getAllPurchasedSupplies()

@app.route('/JARR-disaster-relief/purchase/stats/<int:stat>', methods=['GET'])
def getPurchaseStats(stat):
    if stat == 0:
        return PurchasedSupplyHandler().getTotalPurchases()
    elif stat == 1:
        return PurchasedSupplyHandler().getTotalPurchasesPerCategory()
    elif stat == 2:
        return PurchasedSupplyHandler().getTotalSuppliesPurchasedPerCategory()
    elif stat == 3:
        return PurchasedSupplyHandler().getPurchaseStatisticsPerCategory()
    else:
        return jsonify(Error="Incorrect statistic request"), 405

@app.route('/JARR-disaster-relief/purchase/<int:id>', methods=['GET'])
def getPurchaseById(target_id):
    idType = request.args.get('id_type', type=str)
    if idType == 'purchase':
        return PurchasedSupplyHandler().getPurchasedSupplyById(target_id)
    elif idType == 'buyer':
        return PurchasedSupplyHandler().getPurchasedSuppliesByBuyerId(target_id)
    elif idType == 'supplier':
        return PurchasedSupplyHandler().getPurchasedSuppliesBySupplierId(target_id)
    elif idType == 'supply':
        return PurchasedSupplyHandler().getPurchasedSuppliesBySupplyId(target_id)
    else:
        return jsonify(Error="Incorrect ID type"), 405


# __Request__

@app.route('/JARR-disaster-relief/requests', methods=['GET', 'POST'])
def getAllRequests():
    if request.method == 'POST':
        if request.json is not None and request.form is None:
            return RequestHandler().insert_request_json(request.json)
        elif request.form is not None and request.json is None:
            return RequestHandler().insert_request(request.form)
        else:
            return jsonify(Error="Malformed post request")
    elif request.method == 'GET':
        if not request.args:
            return RequestHandler().get_all_requests()
        else:
            return RequestHandler().search_requests(request.args)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route('/JARR-disaster-relief/requests/<int:request_id>', methods=['GET', 'PUT', 'DELETE'])
def getRequestById(request_id):
    if request.method == 'GET':
        return RequestHandler().get_request_by_id(request_id)
    elif request.method == 'PUT':
        return RequestHandler().update_request(request_id, request.form)
    elif request.method == 'DELETE':
        return RequestHandler().delete_request(request_id)
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


# __FulfilledRequest__

@app.route('/JARR-disaster-relief/fulfill', methods=['GET', 'POST'])
def getFulfills():
    if request.method == 'POST':
        if request.json:
            return FulfilledRequestHandler().insert_fulfilledRequest_json(request.json)
        elif request.form:
            return FulfilledRequestHandler().insert_fulfilledRequest(request.form)
        else:
            return jsonify(Error="Data not found"), 405
    elif request.method == 'GET':
        return FulfilledRequestHandler().getAllFulfilledRequests()


@app.route('/JARR-disaster-relief/fulfill/stats/<int:stat>', methods=['GET'])
def getFulfillStats(stat):
    if stat == 0:
        return FulfilledRequestHandler().getTotalFulfillments()
    elif stat == 1:
        return FulfilledRequestHandler().getTotalFulfillmentsPerCategory()
    elif stat == 2:
        return FulfilledRequestHandler().getTotalRequestsFulfulliedPerCategory()
    elif stat == 3:
        return FulfilledRequestHandler().getFulfillmentStatisticsPerCategory()
    else:
        return jsonify(Error="Incorrect statistic request"), 405


@app.route('/JARR-disaster-relief/fulfill/<int:id>', methods=['GET'])
def getFulfillById(target_id):
    idType = request.args.get('id_type', type=str)
    if idType == 'fulfill':
        return FulfilledRequestHandler().getFulfilledRequestById(target_id)
    elif idType == 'buyer':
        return FulfilledRequestHandler().getFulfilledRequestsByBuyerId(target_id)
    elif idType == 'supplier':
        return FulfilledRequestHandler().getFulfilledRequestsBySellerId(target_id)
    elif idType == 'request':
        return FulfilledRequestHandler().getFulfilledRequestsByRequestId(target_id)
    else:
        return jsonify(Error="Incorrect ID type"), 405


# Resources
# TODO this needs to be fixed
@app.route('/JARR-disaster-relief/resources/<int:resource_id>')
def getAllResources():
    return ResourceHandler().get_all_resources()


@app.route('/JARR-disaster-relief/resources/')
def getAllAvailableResource():
    return ResourceHandler().get_available_resource()


@app.route('/JARR-disaster-relief/resource/<int:person_id>')
def getResourceByPersonId(person_id):
    return ResourceHandler().get_resources_by_person_id(person_id)


@app.route('/JARR-disaster-relief/resource/count')
def getTotalResourceCount():
    return ResourceHandler().get_total_resource()


# Account
@app.route('/JARR-disaster-relief/accounts')
def getAccountData(account_id):
    return AccountHandler().get_account_data(account_id)


@app.route('/JARR-disaster-relief/person/<int:person_id>/accounts')
def getAccountByPersonId(person_id):
    return AccountHandler().get_account_by_person_id(person_id)


@app.route('/JARR-disaster-relief/account/<int:account_id>')
def getAccountType(account_id):
    return AccountHandler().get_account_type(account_id)


@app.route('/JARR-disaster-relief/account/is_admin')
def getAdminAccount():
    return AccountHandler().get_admin_accounts()


if __name__ == '__main__':
    app.run()
