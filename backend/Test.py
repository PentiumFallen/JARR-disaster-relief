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