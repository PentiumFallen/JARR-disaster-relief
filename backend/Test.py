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


