from flask import jsonify
from backend.dao.canned_food import CannedFoodDAO


class CannedFoodHandler:

    def build_cf_dict(self, row):
        result = {}
        result['cf_id'] = row[0]
        result['person_id'] = row[1]
        result['brand'] = row[2]
        result['food_type'] = row[3]
        result['description'] = row[4]
        result['quantity'] = row[5]
        result['unit_price'] = row[6]
        result['date_posted'] = row[7]
        result['curr_quantity'] = row[8]
        result['is_supply'] = row[9]
        result['address_id'] = row[10]
        return result

    def build_cf_attributes(self, cf_id, person_id, brand, food_type, description, quantity, unit_price, date_posted,
                            curr_quantity, is_supply, address_id):
        result = {
            'cf_id': cf_id,
            'person_id': person_id,
            'brand': brand,
            'food_type': food_type,
            'description': description,
            'quantity': quantity,
            'unit_price': unit_price,
            'date_posted': date_posted,
            'curr_quantity': curr_quantity,
            'is_supply': is_supply,
            'address_id': address_id,
        }
        return result

    def get_all_cf_posts(self):
        dao = CannedFoodDAO()
        result_list = dao.getAllCannedFood()
        for row in result_list:
            result = self.build_cf_dict(row)
            result_list.append(result)
        return jsonify(Canned_Food_Posts=result_list)

    def get_all_cf_supplies(self):
        dao = CannedFoodDAO()
        result_list = dao.getAllCannedFoodSupplies()
        for row in result_list:
            result = self.build_cf_dict(row)
            result_list.append(result)
        return jsonify(Canned_Food_Supplies=result_list)

    def get_all_cf_requests(self):
        dao = CannedFoodDAO()
        result_list = dao.getAllCannedFoodRequests()
        for row in result_list:
            result = self.build_cf_dict(row)
            result_list.append(result)
        return jsonify(Canned_Food_Requests=result_list)

    def get_all_available_cf_supplies(self):
        dao = CannedFoodDAO()
        result_list = dao.getAllAvailableCannedFoodSupplies()
        for row in result_list:
            result = self.build_cf_dict(row)
            result_list.append(result)
        return jsonify(Canned_Food_Supplies=result_list)

    def get_all_unfulfilled_cf_requests(self):
        dao = CannedFoodDAO()
        result_list = dao.getAllUnfulfilledCannedFoodRequests()
        for row in result_list:
            result = self.build_cf_dict(row)
            result_list.append(result)
        return jsonify(Canned_Food_Requests=result_list)

    def get_cf_post_by_id(self, cf_id):
        dao = CannedFoodDAO()
        row = dao.getCannedFoodById(cf_id)
        if not row:
            return jsonify(Error="Post Not Found"), 404
        else:
            result = self.build_cf_dict(row)
        return jsonify(Canned_Food_Post=result)

    def get_cf_posts_by_person_id(self, person_id):
        dao = CannedFoodDAO()
        result_list = dao.getCannedFoodByPersonId(person_id)
        for row in result_list:
            result = self.build_cf_dict(row)
            result_list.append(result)
        return jsonify(Canned_Food_Posts=result_list)

    def get_cf_supplies_by_person_id(self, person_id):
        dao = CannedFoodDAO()
        result_list = dao.getCannedFoodSuppliesByPersonId(person_id)
        for row in result_list:
            result = self.build_cf_dict(row)
            result_list.append(result)
        return jsonify(Canned_Food_Posts=result_list)

    def get_cf_requests_by_person_id(self, person_id):
        dao = CannedFoodDAO()
        result_list = dao.getCannedFoodRequestsByPersonId(person_id)
        for row in result_list:
            result = self.build_cf_dict(row)
            result_list.append(result)
        return jsonify(Canned_Food_Posts=result_list)

    def search_cf_posts(self, args):
        brand = args['brand']
        food_type = args['food_type']
        dao = CannedFoodDAO()

        if len(args) == 2 and brand and food_type:
            cf_list = dao.getCannedFoodByBrandAndFoodType(brand, food_type)
        elif len(args) == 1 and brand:
            cf_list = dao.getCannedFoodByBrand(brand)
        elif len(args) == 1 and food_type:
            cf_list = dao.getCannedFoodByFoodType(food_type)
        else:
            return jsonify(Error="Malformed query string"), 400
        result_list = []
        for row in cf_list:
            result = self.build_cf_dict(row)
            result_list.append(result)
        return jsonify(Canned_Food_Posts=result_list)

    def search_cf_supplies(self, args):
        brand = args['brand']
        max_price = args['unit_price']
        food_type = args['food_type']
        dao = CannedFoodDAO()

        if len(args) == 3 and brand and max_price and food_type:
            cf_list = dao.getCannedFoodSuppliesByBrandAndFoodTypeAndMaxPrice(brand, food_type, max_price)
        elif len(args) == 2 and brand and food_type:
            cf_list = dao.getCannedFoodSuppliesByBrandAndFoodType(brand, food_type)
        elif len(args) == 1 and brand:
            cf_list = dao.getCannedFoodSuppliesByBrand(brand)
        elif len(args) == 1 and max_price:
            cf_list = dao.getCannedFoodSuppliesByMaxPrice(max_price)
        elif len(args) == 1 and food_type:
            cf_list = dao.getCannedFoodSuppliesByFoodType(food_type)
        else:
            return jsonify(Error="Malformed query string"), 400
        result_list = []
        for row in cf_list:
            result = self.build_cf_dict(row)
            result_list.append(result)
        return jsonify(Canned_Food_Posts=result_list)

    def search_cf_requests(self, args):
        brand = args['brand']
        food_type = args['food_type']
        dao = CannedFoodDAO()

        if len(args) == 2 and brand and food_type:
            cf_list = dao.getCannedFoodRequestsByBrandAndFoodType(brand, food_type)
        elif len(args) == 1 and brand:
            cf_list = dao.getCannedFoodRequestsByBrand(brand)
        elif len(args) == 1 and food_type:
            cf_list = dao.getCannedFoodRequestsByFoodType(food_type)
        else:
            return jsonify(Error="Malformed query string"), 400
        result_list = []
        for row in cf_list:
            result = self.build_cf_dict(row)
            result_list.append(result)
        return jsonify(Canned_Food_Posts=result_list)

    def insert_cf_supply(self, form):
        if len(form) != 8:
            return jsonify(Error="Malformed post request"), 400
        else:
            dao = CannedFoodDAO()
            person_id = form['person_id']
            brand = form['brand']
            food_type = form['food_type']
            description = form['description']
            quantity = form['quantity']
            unit_price = form['unit_price']
            date_posted = form['date_posted']
            curr_quantity = quantity
            is_supply = True
            address_id = form['address_id']

            if person_id and brand and description and unit_price and quantity and date_posted and food_type and \
                    address_id:
                cf_id = dao.insert(person_id, brand, food_type, description, quantity, unit_price, date_posted,
                                   curr_quantity, is_supply, address_id)
                result = self.build_cf_attributes(cf_id, person_id, brand, food_type, description, quantity, unit_price,
                                                  date_posted, curr_quantity, is_supply, address_id)
                return jsonify(Canned_Food=result), 201
            else:
                return jsonify(Error="Unexpected attributes in post request"), 400

    def insert_cf_supply_json(self, json):
        dao = CannedFoodDAO()
        person_id = json['person_id']
        brand = json['brand']
        food_type = json['food_type']
        description = json['description']
        quantity = json['quantity']
        unit_price = json['unit_price']
        date_posted = json['date_posted']
        curr_quantity = quantity
        is_supply = True
        address_id = json['address_id']

        if person_id and brand and description and unit_price and quantity and date_posted and food_type and \
                address_id:
            cf_id = dao.insert(person_id, brand, food_type, description, quantity, unit_price, date_posted,
                               curr_quantity, is_supply, address_id)
            result = self.build_cf_attributes(cf_id, person_id, brand, food_type, description, quantity, unit_price,
                                              date_posted, curr_quantity, is_supply, address_id)
            return jsonify(Canned_Food=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request"), 400

    def insert_cf_request(self, form):
        if len(form) != 8:
            return jsonify(Error="Malformed post request"), 400
        else:
            dao = CannedFoodDAO()
            person_id = form['person_id']
            brand = form['brand']
            food_type = form['food_type']
            description = form['description']
            quantity = form['quantity']
            unit_price = form['unit_price']
            date_posted = form['date_posted']
            curr_quantity = quantity
            is_supply = False
            address_id = form['address_id']

            if person_id and brand and description and unit_price and quantity and date_posted and food_type and \
                    address_id:
                cf_id = dao.insert(person_id, brand, food_type, description, quantity, unit_price, date_posted,
                                   curr_quantity, is_supply, address_id)
                result = self.build_cf_attributes(cf_id, person_id, brand, food_type, description, quantity, unit_price,
                                                  date_posted, curr_quantity, is_supply, address_id)
                return jsonify(Canned_Food=result), 201
            else:
                return jsonify(Error="Unexpected attributes in post request"), 400

    def insert_cf_request_json(self, json):
        dao = CannedFoodDAO()
        person_id = json['person_id']
        brand = json['brand']
        food_type = json['food_type']
        description = json['description']
        quantity = json['quantity']
        unit_price = json['unit_price']
        date_posted = json['date_posted']
        curr_quantity = quantity
        is_supply = False
        address_id = json['address_id']

        if person_id and brand and description and unit_price and quantity and date_posted and food_type and \
                address_id:
            cf_id = dao.insert(person_id, brand, food_type, description, quantity, unit_price, date_posted,
                               curr_quantity, is_supply, address_id)
            result = self.build_cf_attributes(cf_id, person_id, brand, food_type, description, quantity, unit_price,
                                              date_posted, curr_quantity, is_supply, address_id)
            return jsonify(Canned_Food=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request"), 400

    def delete_cf_post(self, cf_id):
        dao = CannedFoodDAO()
        if not dao.getCannedFoodById(cf_id):
            return jsonify(Error="Post not found."), 404
        else:
            dao.delete(cf_id)
        return jsonify(DeleteStatus="OK"), 200

    def update_cf_post(self, cf_id, form):
        dao = CannedFoodDAO()
        if not dao.getCannedFoodById(cf_id):
            return jsonify(Error="Post not found."), 404
        else:
            if len(form) != 9:
                return jsonify(Error="Malformed update request"), 400
            else:
                brand = form['brand']
                food_type = form['food_type']
                description = form['description']
                unit_price = form['unit_price']
                curr_quantity = form['quantity']
                address_id = form['address_id']

                if int(curr_quantity) < 0:
                    return jsonify(Error="Cannot put negative value"), 400
                if brand and description and unit_price and curr_quantity and food_type and address_id:
                    dao.update(cf_id, brand, food_type, description, unit_price, curr_quantity, address_id)
                    row = dao.getCannedFoodById(cf_id)
                    result = self.build_cf_dict(row)
                    return jsonify(Part=result), 200
                else:
                    return jsonify(Error="Unexpected attributes in update request"), 400
