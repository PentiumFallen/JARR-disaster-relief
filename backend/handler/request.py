from flask import jsonify

class RequestHandler:
    def build_request_dict(self, row):
        result = {
            'request_id': row[0],
            'rcategory': row[1],
            'rname': row[2],
            'rdescription': row[3],
            'raddress': row[4],
            'rmaxpr': row[5],
            'rfulfilled': row[6]
        }
        return result

    def build_request_attributes(self, request_id, rcategory, rname, rdescription, raddress, rmaxprice, rfulfilled):
        result = {
            'request_id': request_id,
            'rcategory': rcategory,
            'rname': rname,
            'rdescription': rdescription,
            'raddress': raddress,
            'rmaxprice': rmaxprice,
            'rfulfilled': rfulfilled
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

    def search_request(self, args):
        category = args.get("category")
        name = args.get("name")
        # Add more! #
        # dao = RequestsDAO()
        request_list = []
        # if (len(args) == 2) and category and name:
        #     request_list = dao.getRequestByCategoryAndName(category, name)
        # elif (len(args) == 1) and category:
        #     request_list = dao.getRequestByCategory(category)
        # elif (len(args) == 1) and name:
        #     request_list = dao.getRequestByName(name)
        # else:
        #     return jsonify(Error = "Malformed query string"), 400
        result_list = []
        result_list.append('Search request works!')
        # for row in request_list:
        #     result = self.build_part_dict(row)
        #     result_list.append(result)
        return jsonify(Requests=result_list)

    def match_requests_to_request(self, args):
        category = args.get("category")
        max_price = args.get("max_price")
        name = args.get("name")
        request_list = []
        # if (len(args) == 1) and name:
        #     request_list = dao.getRequestBycategory(category)
        # elif (len(args) == 2) and category and max_price:
        #     request_list = dao.getRequestByCategoryAndMaxPrice(category, max_price)
        # elif (len(args) == 3) and category and max_price and name:
        #     request_list = dao.getRequestByCategoryNameAndMaxPrice(category, name, max_price)
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
            rname = form['rname']
            rdescription = form['rdescription']
            raddress = form['raddress']
            rmaxprice = form['rmaxprice']
            rfulfilled = form['rfulfilled']
            if rcategory and rname and rdescription and raddress and rmaxprice and rfulfilled:
                # dao = RequestDAO()
                # pid = dao.insert(rcategory, rname, rdescription, raddress, rmaxprice, rfulfilled)
                # result = build_request_attributes(self, request_id, rcategory, rname, rdescription, raddress, rmaxprice, rfulfilled)
                result = 'Insert works!'
                return jsonify(Request=result), 201
            else:
                return jsonify(Error="Unexpected attributes in post request"), 400

    def insert_request_json(self, json):
        rcategory = json['rcategory']
        rname = json['rname']
        rdescription = json['rdescription']
        raddress = json['raddress']
        rmaxprice = json['rmaxprice']
        rfulfilled = json['rfulfilled']
        if rcategory and rname and raddress and rdescription and rmaxprice and rfulfilled:
            # dao = RequestsDAO()
            # pid = dao.insert(pname, pcolor, pmaterial, pprice, rfulfilled)
            # result = self.build_part_attributes(pid, pname, pcolor, pmaterial, pprice, rfulfilled)
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
        #         rname = form['rname']
        #         rdescription = form['rdescription']
        #         raddress = form['raddress']
        #         rmaxprice = form['rmaxprice']
        #         rfulfilled = form['rfulfilled']
        #         if rcategory and rname and raddress and rdescription and rmaxprice:
        #             dao.update(request_id, rcategory, rname, rdescription, raddress, rmaxprice, rfulfilled)
        #             result = self.build_part_attributes(request_id, rcategory, rname, rdescription, raddress, rmaxprice, rfulfilled)
        #             return jsonify(Request=result), 200
        #         else:
        #             return jsonify(Error="Unexpected attributes in update request"), 400
        return jsonify(Request="Update works!")

