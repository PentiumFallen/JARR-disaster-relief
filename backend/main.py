from flask import Flask, jsonify, request
from backend.handler.supply import SupplyHandler
from backend.handler.water import WaterHandler
from backend.handler.waterTransaction import WaterTransactionHandler
from backend.handler.medication import MedicationHandler
from backend.handler.fuel import FuelHandler
from backend.handler.baby_food import BabyFoodHandler
from backend.handler.canned_food import CannedFoodHandler
from backend.handler.dry_food import DryFoodHandler
from backend.handler.ice import IceHandler
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


# __Water__

@app.route('/JARR-disaster-relief/water')
def getAllWaterPosts():
    return WaterHandler().get_all_water_posts()


@app.route('/JARR-disaster-relief/water/<int:water_id>', methods=['GET', 'PUT', 'DELETE'])
def getWaterPostById(water_id):
    if request.method == 'GET':
        return WaterHandler().get_water_post_by_id(water_id)
    elif request.method == 'PUT':
        return WaterHandler().update_water_post(water_id, request.form)
    elif request.method == 'DELETE':
        return WaterHandler().delete_water_post(water_id)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route('/JARR-disaster-relief/person/<int:person_id>/water')
def getWaterPostsByPersonId(person_id):
    return WaterHandler().get_water_posts_by_person_id(person_id)


@app.route('/JARR-disaster-relief/water/supplies', methods=['GET', 'POST'])
def getAllWaterSupplies():
    if request.method == 'POST':
        return WaterHandler().insert_water_supply_json(request.json)
    elif request.method == 'GET':
        if not request.args:
            return WaterHandler().get_all_water_supplies()
        else:
            return WaterHandler().search_water_supplies(request.args)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route('/JARR-disaster-relief/person/<int:person_id>/water/supplies')
def getWaterSupplyByPersonId(person_id):
    return WaterHandler().get_water_supplies_by_person_id(person_id)


@app.route('/JARR-disaster-relief/water/requests', methods=['GET', 'POST'])
def getAllWaterRequests():
    if request.method == 'POST':
        return WaterHandler().insert_water_request_json(request.json)
    else:
        if not request.args:
            return WaterHandler().get_all_water_requests()
        else:
            return WaterHandler().search_water_requests(request.args)


@app.route('/JARR-disaster-relief/person/<int:person_id>/water/requests')
def getWaterRequestsByPersonId(person_id):
    return WaterHandler().get_water_supplies_by_person_id(person_id)

# __WaterTransactions__

@app.route('/JARR-disaster-relief/water-transaction')
def getAllWaterTransactions():
    return WaterTransactionHandler().getAllWaterTransaction()


@app.route('/JARR-disaster-relief/water-transaction/<int:water_id>', methods=['GET', 'PUT', 'DELETE'])
def getWaterTransactionById(water_id):
    if request.method == 'GET':
        return WaterTransactionHandler().getWaterTransactionById(water_id)
    elif request.method == 'PUT':
        return WaterTransactionHandler().updateTransaction(water_id, request.form)
    elif request.method == 'DELETE':
        return WaterTransactionHandler().deleteWaterTransaction(water_id)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route('/JARR-disaster-relief/person/<int:person_id>/water-transaction')
def getWaterPostsByPersonId(person_id):
    return WaterTransactionHandler().getWaterTransactionByPersonId(person_id)


# __Medication__

@app.route('/JARR-disaster-relief/medication')
def getAllMedicationPosts():
    return MedicationHandler().get_all_medication_posts()


@app.route('/JARR-disaster-relief/medication/<int:medication_id>', methods=['GET', 'PUT', 'DELETE'])
def getMedicationPostById(medication_id):
    if request.method == 'GET':
        return MedicationHandler().get_medication_post_by_id(medication_id)
    elif request.method == 'PUT':
        return MedicationHandler().update_medication(medication_id, request.form)
    elif request.method == 'DELETE':
        return MedicationHandler().delete_medication_post(medication_id)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route('/JARR-disaster-relief/person/<int:person_id>/medication')
def getMedicationPostsByPersonId(person_id):
    return MedicationHandler().get_medication_posts_by_person_id(person_id)


@app.route('/JARR-disaster-relief/medication/supplies', methods=['GET', 'POST'])
def getAllMedicationSupplies():
    if request.method == 'POST':
        return MedicationHandler().insert_medication_supply_json(request.json)
    elif request.method == 'GET':
        if not request.args:
            return MedicationHandler().get_all_medication_supplies()
        else:
            return MedicationHandler().search_medication_supplies(request.args)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route('/JARR-disaster-relief/person/<int:person_id>/medication/supplies')
def getMedicationSupplyByPersonId(person_id):
    return MedicationHandler().get_medication_supplies_by_person_id(person_id)


@app.route('/JARR-disaster-relief/medication/requests', methods=['GET', 'POST'])
def getAllMedicationRequests():
    if request.method == 'POST':
        return MedicationHandler().insert_medication_request_json(request.json)
    else:
        if not request.args:
            return MedicationHandler().get_all_medication_requests()
        else:
            return MedicationHandler().search_medication_requests(request.args)


@app.route('/JARR-disaster-relief/person/<int:person_id>/medication/requests')
def getMedicationRequestsByPersonId(person_id):
    return MedicationHandler().get_medication_supplies_by_person_id(person_id)


# __BabyFood__

@app.route('/JARR-disaster-relief/baby-food')
def getAllBabyFoodPosts():
    return BabyFoodHandler().get_all_bf_posts()


@app.route('/JARR-disaster-relief/bf/<int:bf_id>', methods=['GET', 'PUT', 'DELETE'])
def getBabyFoodPostById(bf_id):
    if request.method == 'GET':
        return BabyFoodHandler().get_bf_post_by_id(bf_id)
    elif request.method == 'PUT':
        return BabyFoodHandler().update_bf_post(bf_id, request.form)
    elif request.method == 'DELETE':
        return BabyFoodHandler().delete_bf_post(bf_id)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route('/JARR-disaster-relief/person/<int:person_id>/baby-food')
def getBabyFoodPostsByPersonId(person_id):
    return BabyFoodHandler().get_bf_posts_by_person_id(person_id)


@app.route('/JARR-disaster-relief/baby-food/supplies', methods=['GET', 'POST'])
def getAllBabyFoodSupplies():
    if request.method == 'POST':
        return BabyFoodHandler().insert_bf_supply_json(request.json)
    elif request.method == 'GET':
        if not request.args:
            return BabyFoodHandler().get_all_bf_supplies()
        else:
            return BabyFoodHandler().search_bf_supplies(request.args)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route('/JARR-disaster-relief/person/<int:person_id>/baby-food/supplies')
def getBabyFoodSupplyByPersonId(person_id):
    return BabyFoodHandler().get_bf_supplies_by_person_id(person_id)


@app.route('/JARR-disaster-relief/baby-food/requests', methods=['GET', 'POST'])
def getAllBabyFoodRequests():
    if request.method == 'POST':
        return BabyFoodHandler().insert_bf_request_json(request.json)
    else:
        if not request.args:
            return BabyFoodHandler().get_all_bf_requests()
        else:
            return BabyFoodHandler().search_bf_requests(request.args)


@app.route('/JARR-disaster-relief/person/<int:person_id>/baby-food/requests')
def getBabyFoodRequestsByPersonId(person_id):
    return BabyFoodHandler().get_bf_supplies_by_person_id(person_id)


# __CannedFood__

@app.route('/JARR-disaster-relief/canned-food')
def getAllCannedFoodPosts():
    return CannedFoodHandler().get_all_cf_posts()


@app.route('/JARR-disaster-relief/cf/<int:cf_id>', methods=['GET', 'PUT', 'DELETE'])
def getCannedFoodPostById(cf_id):
    if request.method == 'GET':
        return CannedFoodHandler().get_cf_post_by_id(cf_id)
    elif request.method == 'PUT':
        return CannedFoodHandler().update_cf_post(cf_id, request.form)
    elif request.method == 'DELETE':
        return CannedFoodHandler().delete_cf_post(cf_id)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route('/JARR-disaster-relief/person/<int:person_id>/canned-food')
def getCannedFoodPostsByPersonId(person_id):
    return CannedFoodHandler().get_cf_posts_by_person_id(person_id)


@app.route('/JARR-disaster-relief/canned-food/supplies', methods=['GET', 'POST'])
def getAllCannedFoodSupplies():
    if request.method == 'POST':
        return CannedFoodHandler().insert_cf_supply_json(request.json)
    elif request.method == 'GET':
        if not request.args:
            return CannedFoodHandler().get_all_cf_supplies()
        else:
            return CannedFoodHandler().search_cf_supplies(request.args)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route('/JARR-disaster-relief/person/<int:person_id>/canned-food/supplies')
def getCannedFoodSupplyByPersonId(person_id):
    return CannedFoodHandler().get_cf_supplies_by_person_id(person_id)


@app.route('/JARR-disaster-relief/canned-food/requests', methods=['GET', 'POST'])
def getAllCannedFoodRequests():
    if request.method == 'POST':
        return CannedFoodHandler().insert_cf_request_json(request.json)
    else:
        if not request.args:
            return CannedFoodHandler().get_all_cf_requests()
        else:
            return CannedFoodHandler().search_cf_requests(request.args)


@app.route('/JARR-disaster-relief/person/<int:person_id>/canned-food/requests')
def getCannedFoodRequestsByPersonId(person_id):
    return CannedFoodHandler().get_cf_supplies_by_person_id(person_id)


# __DryFood__

@app.route('/JARR-disaster-relief/dry-food')
def getAllDryFoodPosts():
    return DryFoodHandler().get_all_df_posts()


@app.route('/JARR-disaster-relief/df/<int:df_id>', methods=['GET', 'PUT', 'DELETE'])
def getDryFoodPostById(df_id):
    if request.method == 'GET':
        return DryFoodHandler().get_df_post_by_id(df_id)
    elif request.method == 'PUT':
        return DryFoodHandler().update_df_post(df_id, request.form)
    elif request.method == 'DELETE':
        return DryFoodHandler().delete_df_post(df_id)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route('/JARR-disaster-relief/person/<int:person_id>/dry-food')
def getDryFoodPostsByPersonId(person_id):
    return DryFoodHandler().get_df_posts_by_person_id(person_id)


@app.route('/JARR-disaster-relief/dry-food/supplies', methods=['GET', 'POST'])
def getAllDryFoodSupplies():
    if request.method == 'POST':
        return DryFoodHandler().insert_df_supply_json(request.json)
    elif request.method == 'GET':
        if not request.args:
            return DryFoodHandler().get_all_df_supplies()
        else:
            return DryFoodHandler().search_df_supplies(request.args)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route('/JARR-disaster-relief/person/<int:person_id>/dry-food/supplies')
def getDryFoodSupplyByPersonId(person_id):
    return DryFoodHandler().get_df_supplies_by_person_id(person_id)


@app.route('/JARR-disaster-relief/dry-food/requests', methods=['GET', 'POST'])
def getAllDryFoodRequests():
    if request.method == 'POST':
        return DryFoodHandler().insert_df_request_json(request.json)
    else:
        if not request.args:
            return DryFoodHandler().get_all_df_requests()
        else:
            return DryFoodHandler().search_df_requests(request.args)


@app.route('/JARR-disaster-relief/person/<int:person_id>/dry-food/requests')
def getDryFoodRequestsByPersonId(person_id):
    return DryFoodHandler().get_df_supplies_by_person_id(person_id)


# __Ice__

@app.route('/JARR-disaster-relief/ice')
def getAllIcePosts():
    return IceHandler().get_all_ice_posts()


@app.route('/JARR-disaster-relief/ice/<int:ice_id>', methods=['GET', 'PUT', 'DELETE'])
def getIcePostById(ice_id):
    if request.method == 'GET':
        return IceHandler().get_ice_post_by_id(ice_id)
    elif request.method == 'PUT':
        return IceHandler().update_ice_post(ice_id, request.form)
    elif request.method == 'DELETE':
        return IceHandler().delete_ice_post(ice_id)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route('/JARR-disaster-relief/person/<int:person_id>/ice')
def getIcePostsByPersonId(person_id):
    return IceHandler().get_ice_posts_by_person_id(person_id)


@app.route('/JARR-disaster-relief/ice/supplies', methods=['GET', 'POST'])
def getAllIceSupplies():
    if request.method == 'POST':
        return IceHandler().insert_ice_supply_json(request.json)
    elif request.method == 'GET':
        if not request.args:
            return IceHandler().get_all_ice_supplies()
        else:
            return IceHandler().search_ice_supplies(request.args)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route('/JARR-disaster-relief/person/<int:person_id>/ice/supplies')
def getIceSupplyByPersonId(person_id):
    return IceHandler().get_ice_supplies_by_person_id(person_id)


@app.route('/JARR-disaster-relief/ice/requests', methods=['GET', 'POST'])
def getAllIceRequests():
    if request.method == 'POST':
        return IceHandler().insert_ice_request_json(request.json)
    else:
        if not request.args:
            return IceHandler().get_all_ice_requests()
        else:
            return IceHandler().search_ice_requests(request.args)


@app.route('/JARR-disaster-relief/person/<int:person_id>/ice/requests')
def getIceRequestsByPersonId(person_id):
    return IceHandler().get_ice_supplies_by_person_id(person_id)


# __Fuel__

@app.route('/JARR-disaster-relief/fuel')
def getAllFuelPosts():
    return FuelHandler().get_all_fuel_posts()


@app.route('/JARR-disaster-relief/fuel/<int:fuel_id>', methods=['GET', 'PUT', 'DELETE'])
def getFuelPostById(fuel_id):
    if request.method == 'GET':
        return FuelHandler().get_fuel_post_by_id(fuel_id)
    elif request.method == 'PUT':
        return FuelHandler().update_fuel_post(fuel_id, request.form)
    elif request.method == 'DELETE':
        return FuelHandler().delete_fuel_post(fuel_id)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route('/JARR-disaster-relief/person/<int:person_id>/fuel')
def getFuelPostsByPersonId(person_id):
    return FuelHandler().get_fuel_posts_by_person_id(person_id)


@app.route('/JARR-disaster-relief/fuel/supplies', methods=['GET', 'POST'])
def getAllFuelSupplies():
    if request.method == 'POST':
        return FuelHandler().insert_fuel_supply_json(request.json)
    elif request.method == 'GET':
        if not request.args:
            return FuelHandler().get_all_fuel_supplies()
        else:
            return FuelHandler().search_fuel_supplies(request.args)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route('/JARR-disaster-relief/person/<int:person_id>/fuel/supplies')
def getFuelSupplyByPersonId(person_id):
    return FuelHandler().get_fuel_supplies_by_person_id(person_id)


@app.route('/JARR-disaster-relief/fuel/requests', methods=['GET', 'POST'])
def getAllFuelRequests():
    if request.method == 'POST':
        return FuelHandler().insert_fuel_request_json(request.json)
    else:
        if not request.args:
            return FuelHandler().get_all_fuel_requests()
        else:
            return FuelHandler().search_fuel_requests(request.args)


@app.route('/JARR-disaster-relief/person/<int:person_id>/fuel/requests')
def getFuelRequestsByPersonId(person_id):
    return FuelHandler().get_fuel_supplies_by_person_id(person_id)


# @app.route('/JARR-disaster-relief/supplies', methods=['GET', 'POST'])
# def getAllSupplies():
#     if request.method == 'POST':
#         return SupplyHandler().insert_supply_json(request.json)
#     else:
#         if not request.args:
#             return SupplyHandler().get_all_supplies()
#         else:
#             return SupplyHandler().search_supply(request.args)
#
#
# @app.route('/JARR-disaster-relief/person/<int:person_id>/supplies')
# def getAllSuppliesOfPerson(person_id):
#     return SupplyHandler().get_supplies_by_person_id(person_id)
#
#
# @app.route('/JARR-disaster-relief/supplies/match')
# def matchSuppliesToRequest():
#     return SupplyHandler().match_supplies_to_request(request.args)
#
#
# @app.route('/JARR-disaster-relief/supplies/<int:supply_id>', methods=['GET', 'PUT', 'DELETE'])
# def getSupplyById(supply_id):
#     if request.method == 'GET':
#         return SupplyHandler().get_supply_by_id(supply_id)
#     elif request.method == 'PUT':
#         return SupplyHandler().update_supply(supply_id, request.form)
#     elif request.method == 'DELETE':
#         return SupplyHandler().delete_supply(supply_id)
#     else:
#         return jsonify(Error="Method not allowed."), 405


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
def getRequestById(request_id):
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
