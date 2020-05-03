from flask import jsonify

class RequestHandler:
    def build_request_dict(self, row):
        result = {
            'request_id': row[0],
            'rcategory': row[1],
            'rdescription': row[2],
            'raddress': row[3],
            'rprice': row[4],
        }
        return result

    def build_request_attributes(self, request_id, rcategory, rdescription, raddress, rprice,):
        result = {
            'request_id': request_id,
            'rcategory': rcategory,
            'rdescription': rdescription,
            'raddress': raddress,
            'rprice': rprice
        }
        return result

    def get_all_requests(self):
        # dao = RequestDAO()
        # request_list = dao.get_all_requests()
        result_list = ['Get all requests works!']
        # for row in request_list:
        #     result = self.build_request_dict(row)
        #     result_list.append(result)
        return jsonify(Requests=result_list)

    def get_request_by_id(self, request_id):
        # dao = RequestsDAO()
        # row = dao.getRequestById(pid)
        # if not row:
        #     return jsonify(Error = "Request Not Found"), 404
        # else:
        #     request = self.build_request_dict(row)
        request = 'Got request ' + str(request_id) + '!'
        return jsonify(Request=request)

    def get_requests_by_person_id(self, person_id):
        requests = 'Got requests of person number ' + str(person_id)
        return jsonify(Requests=requests)

    def search_request(self, args):
        category = args.get("category")
        # Add more! #
        # dao = RequestsDAO()
        request_list = []
        # if (len(args) == 1) and category:
        #     request_list = dao.getRequestByCategory(category)
        # else:
        #     return jsonify(Error = "Malformed query string"), 400
        result_list = []
        result_list.append('Search request works!')
        # for row in request_list:
        #     result = self.build_part_dict(row)
        #     result_list.append(result)
        return jsonify(Requests=result_list)

    def match_requests_to_supplies(self, args):
        category = args.get("category")
        rprice = args.get("rprice")
        request_list = []
        # if (len(args) == 1) and category:
        #     request_list = dao.getRequestBycategory(category)
        # elif (len(args) == 2) and category and rprice:
        #     request_list = dao.getRequestByCategoryAndMaxPrice(category, rprice)
        # else:
        #     return jsonify(Error = "Malformed querry string"), 400
        result_list = []
        result_list.append('Match requests to request works!')
        # for row in request_list:
        #     result = self.build_part_dict(row)
        #     result_list.append(result)
        return jsonify(Requests=result_list)

    def insert_request(self, form):
        if len(form) != 5:
            return jsonify(Error="Malformed post request"), 400
        else:
            rcategory = form['rcategory']
            rdescription = form['rdescription']
            raddress = form['raddress']
            rprice = form['rprice']
            if rcategory and rdescription and raddress and rprice:
                # dao = RequestDAO()
                # pid = dao.insert(rcategory, rdescription, raddress, rprice)
                # result = build_request_attributes(self, request_id, rcategory, rdescription, raddress, rprice)
                result = 'Insert works!'
                return jsonify(Request=result), 201
            else:
                return jsonify(Error="Unexpected attributes in post request"), 400

    def insert_request_json(self, json):
        rcategory = json['rcategory']
        rdescription = json['rdescription']
        raddress = json['raddress']
        rprice = json['rprice']
        if rcategory and raddress and rdescription and rprice:
            # dao = RequestsDAO()
            # pid = dao.insert(rcategory, rdescription, raddress, rprice)
            # result = build_request_attributes(self, request_id, rcategory, rdescription, raddress, rprice)
            return jsonify(Request="Insert request json works!"), 201
        else:
            return jsonify(Error="Unexpected attributes in post request"), 400

    def delete_request(self, request_id):
        # dao = RequestDAO()
        # if not dao.getRequestById(request_id):
        #     return jsonify(Error = "Request not found."), 404
        # else:
        #     dao.delete(request_id)
        return jsonify(DeleteStatus="OK"), 200

    def update_request(self, request_id, form):
        # dao = RequestDAO()
        # if not dao.getRequestById(request_id):
        #     return jsonify(Error="Request not found."), 404
        # else:
        #     if len(form) != 4:
        #         return jsonify(Error="Malformed update request"), 400
        #     else:
        #         rcategory = form['rcategory']
        #         rdescription = form['rdescription']
        #         raddress = form['raddress']
        #         rprice = form['rprice']
        #         if rcategory and raddress and rdescription and rprice:
        #             dao.update(request_id, rcategory, rdescription, raddress, rprice)
        #             result = self.build_part_attributes(request_id, rcategory, rdescription, raddress, rprice)
        #             return jsonify(Request=result), 200
        #         else:
        #             return jsonify(Error="Unexpected attributes in update request"), 400
        return jsonify(Request="Update works!")

