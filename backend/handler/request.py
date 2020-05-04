from flask import jsonify
from backend.dao.request import RequestDAO
#from backend.dao.resource import ResourceDAO


class RequestHandler:

    # Joined to resource
    def build_request_dict(self, row):
        result = {
            'request_id': row[0],
            'category': row[1],
            'subcategory': row[2],
            'person_id': row[3],
            'name': row[4],
            'quantity': row[5],
            'rdescription': row[6],
            'needed': row[7],
            'max_unit_price': row[8],
            'date_offered': row[9],
            'address_id': row[10]
        }
        return result

    def build_request_attributes(self, request_id, resource_id, category_id, person_id, name, quantity, description,
                                 needed, max_unit_price, address_id):
        result = {
            'request_id': request_id,
            'resource_id': resource_id,
            'category_id': category_id,
            'person_id': person_id,
            'name': name,
            'quantity': quantity,
            'rdescription': description,
            'needed': needed,
            'max_unit_price': max_unit_price,
            'address_id': address_id
        }
        return result

    def build_request_count(self, row):
        result = {
            'category': row[0],
            'amount': row[1]
        }
        return result

    def get_all_requests(self):
        dao = RequestDAO()
        request_list = dao.getAllRequests()
        result_list = []
        for row in request_list:
            result = self.build_request_dict(row)
            result_list.append(result)
        return jsonify(Requests=result_list)

    def get_all_needed_requests(self):
        dao = RequestDAO()
        request_list = dao.getAllNeededRequests()
        result_list = []
        for row in request_list:
            result = self.build_request_dict(row)
            result_list.append(result)
        return jsonify(Needed_Requests=result_list)

    def get_total_requests(self):
        dao = RequestDAO()
        amount = dao.getTotalRequests()
        return jsonify(Total_Requests=amount)

    def get_total_needed_requests(self):
        dao = RequestDAO()
        amount = dao.getTotalNeededRequests()
        return jsonify(Total_Needed_Requests=amount)

    def get_total_requests_per_category(self):
        dao = RequestDAO()
        count_list = dao.getTotalRequestsPerCategory()
        result_list = []
        for row in count_list:
            result = self.build_request_count(row)
            result_list.append(result)
        return jsonify(Request_Count=result_list)

    def get_total_needed_requests_per_category(self):
        dao = RequestDAO()
        count_list = dao.getTotalNeededRequestsPerCategory()
        result_list = []
        for row in count_list:
            result = self.build_request_count(row)
            result_list.append(result)
        return jsonify(Needed_Request_Count=result_list)

    def get_request_by_id(self, request_id):
        dao = RequestDAO()
        row = dao.getRequestById(request_id)
        if not row:
            return jsonify(Error="Post Not Found"), 404
        else:
            result = self.build_request_dict(row)
        return jsonify(Request_Post=result)

    def get_requests_by_person_id(self, person_id):
        dao = RequestDAO()
        request_list = dao.getRequestsByPersonId(person_id)
        result_list = []
        for row in request_list:
            result = self.build_request_dict(row)
            result_list.append(result)
        return jsonify(Request_Posts=result_list)

    def get_needed_requests_by_person_id(self, person_id):
        dao = RequestDAO()
        request_list = dao.getNeededRequestsByPersonId(person_id)
        result_list = []
        for row in request_list:
            result = self.build_request_dict(row)
            result_list.append(result)
        return jsonify(Request_Posts=result_list)

    def search_requests(self, args):
        max_price = args['max_unit_price']
        category = args['category']
        dao = RequestDAO()

        if len(args) == 2 and max_price and category:
            request_list = dao.getRequestsByMaxPriceAndCategory(max_price, category)
        elif len(args) == 1 and max_price:
            request_list = dao.getRequestsByMaxPrice(max_price)
        elif len(args) == 1 and category:
            request_list = dao.getRequestsByCategory(category)
        else:
            return jsonify(Error="Malformed query string"), 400
        result_list = []
        for row in request_list:
            result = self.build_request_dict(row)
            result_list.append(result)
        return jsonify(Request_Posts=result_list)

    def search_needed_requests(self, args):
        max_price = args['max_unit_price']
        category = args['category']
        dao = RequestDAO()

        if len(args) == 2 and max_price and category:
            request_list = dao.getNeededRequestsByMaxPriceAndCategory(max_price, category)
        elif len(args) == 1 and max_price:
            request_list = dao.getNeededRequestsByMaxPrice(max_price)
        elif len(args) == 1 and category:
            request_list = dao.getNeededRequestsByCategory(category)
        else:
            return jsonify(Error="Malformed query string"), 400
        result_list = []
        for row in request_list:
            result = self.build_request_dict(row)
            result_list.append(result)
        return jsonify(Request_Posts=result_list)

    def insert_request(self, form):
        if len(form) != 7:
            return jsonify(Error="Malformed post request"), 400
        else:
            dao = RequestDAO()
            category_id = form['category_id']
            person_id = form['person_id']
            name = form['name']
            quantity = form['quantity']
            description = form['description']
            unit_price = form['max_unit_price']
            address_id = form['address_id']

            if person_id and category_id and name and description and unit_price and quantity \
                    and address_id:
                needed = quantity
                #resource_id = ResourceDAO().insert(category_id, person_id, name, quantity)
                resource_id = 0
                request_id = dao.insert(resource_id, person_id, description, needed, unit_price,
                                        address_id)
                result = self.build_request_attributes(request_id, resource_id, category_id, person_id, name, quantity,
                                                       description, needed, unit_price, address_id)
                return jsonify(Request=result), 201
            else:
                return jsonify(Error="Unexpected attributes in post request"), 400

    def insert_request_json(self, json):
        dao = RequestDAO()
        category_id = json['category_id']
        person_id = json['person_id']
        name = json['name']
        quantity = json['quantity']
        description = json['description']
        needed = quantity
        unit_price = json['max_unit_price']
        address_id = json['address_id']

        if person_id and category_id and name and needed and description and unit_price and quantity \
                and address_id:
            # resource_id = ResourceDAO().insert(category_id=category_id, person_id=person_id, name=name, quantity=quantity)
            resource_id = 0
            request_id = dao.insert(resource_id, person_id, description, needed, unit_price, address_id)
            result = self.build_request_attributes(request_id, resource_id, category_id, person_id, name, quantity,
                                                   description, needed, unit_price, address_id)
            return jsonify(Request=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request"), 400

    def delete_request(self, request_id):
        dao = RequestDAO()
        if not dao.getRequestById(request_id):
            return jsonify(Error="Post not found."), 404
        else:
            dao.delete(request_id)
        return jsonify(DeleteStatus="OK"), 200

    def update_request(self, request_id, form):
        dao = RequestDAO()
        if not dao.getRequestById(request_id):
            return jsonify(Error="Post not found."), 404
        else:
            if len(form) != 4:
                return jsonify(Error="Malformed update request"), 400
            else:
                description = form['description']
                unit_price = form['max_unit_price']
                needed = form['needed']
                address_id = form['address_id']

                if int(needed) < 0:
                    return jsonify(Error="Cannot put negative value in needed"), 400
                if description and unit_price and needed and address_id:
                    dao.update(request_id, description, needed, unit_price, address_id)
                    row = dao.getRequestById(request_id)
                    result = self.build_request_dict(row)
                    return jsonify(Part=result), 200
                else:
                    return jsonify(Error="Unexpected attributes in update request"), 400
