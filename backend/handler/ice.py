from flask import jsonify
from backend.dao.ice import IceDAO


class IceHandler:

    def build_ice_dict(self, row):
        result = {}
        result['ice_id'] = row[0]
        result['person_id'] = row[1]
        result['brand'] = row[2]
        result['weight'] = row[3]
        result['description'] = row[4]
        result['quantity'] = row[5]
        result['unit_price'] = row[6]
        result['date_posted'] = row[7]
        result['curr_quantity'] = row[8]
        result['is_supply'] = row[9]
        result['address_id'] = row[10]
        return result

    def build_ice_attributes(self, ice_id, person_id, brand, weight, description, quantity, unit_price, date_posted,
                             curr_quantity, is_supply, address_id):
        result = {
            'ice_id': ice_id,
            'person_id': person_id,
            'brand': brand,
            'weight': weight,
            'description': description,
            'quantity': quantity,
            'unit_price': unit_price,
            'date_posted': date_posted,
            'curr_quantity': curr_quantity,
            'is_supply': is_supply,
            'address_id': address_id,
        }
        return result

    def get_all_ice_posts(self):
        dao = IceDAO()
        result_list = dao.getAllIce()
        for row in result_list:
            result = self.build_ice_dict(row)
            result_list.append(result)
        return jsonify(Dry_Food_Posts=result_list)

    def get_all_ice_supplies(self):
        dao = IceDAO()
        result_list = dao.getAllIceSupplies()
        for row in result_list:
            result = self.build_ice_dict(row)
            result_list.append(result)
        return jsonify(Dry_Food_Supplies=result_list)

    def get_all_ice_requests(self):
        dao = IceDAO()
        result_list = dao.getAllIceRequests()
        for row in result_list:
            result = self.build_ice_dict(row)
            result_list.append(result)
        return jsonify(Dry_Food_Requests=result_list)

    def get_all_available_ice_supplies(self):
        dao = IceDAO()
        result_list = dao.getAllAvailableIceSupplies()
        for row in result_list:
            result = self.build_ice_dict(row)
            result_list.append(result)
        return jsonify(Dry_Food_Supplies=result_list)

    def get_all_unfulfilled_ice_requests(self):
        dao = IceDAO()
        result_list = dao.getAllUnfulfilledIceRequests()
        for row in result_list:
            result = self.build_ice_dict(row)
            result_list.append(result)
        return jsonify(Dry_Food_Requests=result_list)

    def get_ice_post_by_id(self, ice_id):
        dao = IceDAO()
        row = dao.getIceById(ice_id)
        if not row:
            return jsonify(Error="Post Not Found"), 404
        else:
            result = self.build_ice_dict(row)
        return jsonify(Dry_Food_Post=result)

    def get_ice_posts_by_person_id(self, person_id):
        dao = IceDAO()
        result_list = dao.getIceByPersonId(person_id)
        for row in result_list:
            result = self.build_ice_dict(row)
            result_list.append(result)
        return jsonify(Dry_Food_Posts=result_list)

    def get_ice_supplies_by_person_id(self, person_id):
        dao = IceDAO()
        result_list = dao.getIceSuppliesByPersonId(person_id)
        for row in result_list:
            result = self.build_ice_dict(row)
            result_list.append(result)
        return jsonify(Dry_Food_Posts=result_list)

    def get_ice_requests_by_person_id(self, person_id):
        dao = IceDAO()
        result_list = dao.getIceRequestsByPersonId(person_id)
        for row in result_list:
            result = self.build_ice_dict(row)
            result_list.append(result)
        return jsonify(Dry_Food_Posts=result_list)

    def search_ice_posts(self, args):
        brand = args['brand']
        weight = args['weight']
        dao = IceDAO()

        if len(args) == 2 and brand and weight:
            ice_list = dao.getIceByBrandAndFoodType(brand, weight)
        elif len(args) == 1 and brand:
            ice_list = dao.getIceByBrand(brand)
        elif len(args) == 1 and weight:
            ice_list = dao.getIceByFoodType(weight)
        else:
            return jsonify(Error="Malformed query string"), 400
        result_list = []
        for row in ice_list:
            result = self.build_ice_dict(row)
            result_list.append(result)
        return jsonify(Dry_Food_Posts=result_list)

    def search_ice_supplies(self, args):
        brand = args['brand']
        max_price = args['unit_price']
        weight = args['weight']
        dao = IceDAO()

        if len(args) == 3 and brand and max_price and weight:
            ice_list = dao.getIceSuppliesByBrandAndFoodTypeAndMaxPrice(brand, weight, max_price)
        elif len(args) == 2 and brand and weight:
            ice_list = dao.getIceSuppliesByBrandAndFoodType(brand, weight)
        elif len(args) == 1 and brand:
            ice_list = dao.getIceSuppliesByBrand(brand)
        elif len(args) == 1 and max_price:
            ice_list = dao.getIceSuppliesByMaxPrice(max_price)
        elif len(args) == 1 and weight:
            ice_list = dao.getIceSuppliesByFoodType(weight)
        else:
            return jsonify(Error="Malformed query string"), 400
        result_list = []
        for row in ice_list:
            result = self.build_ice_dict(row)
            result_list.append(result)
        return jsonify(Dry_Food_Posts=result_list)

    def search_ice_requests(self, args):
        brand = args['brand']
        weight = args['weight']
        dao = IceDAO()

        if len(args) == 2 and brand and weight:
            ice_list = dao.getIceRequestsByBrandAndFoodType(brand, weight)
        elif len(args) == 1 and brand:
            ice_list = dao.getIceRequestsByBrand(brand)
        elif len(args) == 1 and weight:
            ice_list = dao.getIceRequestsByFoodType(weight)
        else:
            return jsonify(Error="Malformed query string"), 400
        result_list = []
        for row in ice_list:
            result = self.build_ice_dict(row)
            result_list.append(result)
        return jsonify(Dry_Food_Posts=result_list)

    def insert_ice_supply(self, form):
        if len(form) != 8:
            return jsonify(Error="Malformed post request"), 400
        else:
            dao = IceDAO()
            person_id = form['person_id']
            brand = form['brand']
            weight = form['weight']
            description = form['description']
            quantity = form['quantity']
            unit_price = form['unit_price']
            date_posted = form['date_posted']
            curr_quantity = quantity
            is_supply = True
            address_id = form['address_id']

            if person_id and brand and description and unit_price and quantity and date_posted and weight and \
                    address_id:
                ice_id = dao.insert(person_id, brand, weight, description, quantity, unit_price, date_posted,
                                    curr_quantity, is_supply, address_id)
                result = self.build_ice_attributes(ice_id, person_id, brand, weight, description, quantity, unit_price,
                                                   date_posted, curr_quantity, is_supply, address_id)
                return jsonify(Dry_Food=result), 201
            else:
                return jsonify(Error="Unexpected attributes in post request"), 400

    def insert_ice_supply_json(self, json):
        dao = IceDAO()
        person_id = json['person_id']
        brand = json['brand']
        weight = json['weight']
        description = json['description']
        quantity = json['quantity']
        unit_price = json['unit_price']
        date_posted = json['date_posted']
        curr_quantity = quantity
        is_supply = True
        address_id = json['address_id']

        if person_id and brand and description and unit_price and quantity and date_posted and weight and \
                address_id:
            ice_id = dao.insert(person_id, brand, weight, description, quantity, unit_price, date_posted,
                                curr_quantity, is_supply, address_id)
            result = self.build_ice_attributes(ice_id, person_id, brand, weight, description, quantity, unit_price,
                                               date_posted, curr_quantity, is_supply, address_id)
            return jsonify(Dry_Food=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request"), 400

    def insert_ice_request(self, form):
        if len(form) != 8:
            return jsonify(Error="Malformed post request"), 400
        else:
            dao = IceDAO()
            person_id = form['person_id']
            brand = form['brand']
            weight = form['weight']
            description = form['description']
            quantity = form['quantity']
            unit_price = form['unit_price']
            date_posted = form['date_posted']
            curr_quantity = quantity
            is_supply = False
            address_id = form['address_id']

            if person_id and brand and description and unit_price and quantity and date_posted and weight and \
                    address_id:
                ice_id = dao.insert(person_id, brand, weight, description, quantity, unit_price, date_posted,
                                    curr_quantity, is_supply, address_id)
                result = self.build_ice_attributes(ice_id, person_id, brand, weight, description, quantity, unit_price,
                                                   date_posted, curr_quantity, is_supply, address_id)
                return jsonify(Dry_Food=result), 201
            else:
                return jsonify(Error="Unexpected attributes in post request"), 400

    def insert_ice_request_json(self, json):
        dao = IceDAO()
        person_id = json['person_id']
        brand = json['brand']
        weight = json['weight']
        description = json['description']
        quantity = json['quantity']
        unit_price = json['unit_price']
        date_posted = json['date_posted']
        curr_quantity = quantity
        is_supply = False
        address_id = json['address_id']

        if person_id and brand and description and unit_price and quantity and date_posted and weight and \
                address_id:
            ice_id = dao.insert(person_id, brand, weight, description, quantity, unit_price, date_posted,
                                curr_quantity, is_supply, address_id)
            result = self.build_ice_attributes(ice_id, person_id, brand, weight, description, quantity, unit_price,
                                               date_posted, curr_quantity, is_supply, address_id)
            return jsonify(Dry_Food=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request"), 400

    def delete_ice_post(self, ice_id):
        dao = IceDAO()
        if not dao.getIceById(ice_id):
            return jsonify(Error="Post not found."), 404
        else:
            dao.delete(ice_id)
        return jsonify(DeleteStatus="OK"), 200

    def update_ice_post(self, ice_id, form):
        dao = IceDAO()
        if not dao.getIceById(ice_id):
            return jsonify(Error="Post not found."), 404
        else:
            if len(form) != 9:
                return jsonify(Error="Malformed update request"), 400
            else:
                brand = form['brand']
                weight = form['weight']
                description = form['description']
                unit_price = form['unit_price']
                curr_quantity = form['quantity']
                address_id = form['address_id']

                if int(curr_quantity) < 0:
                    return jsonify(Error="Cannot put negative value"), 400
                if brand and description and unit_price and curr_quantity and weight and address_id:
                    dao.update(ice_id, brand, weight, description, unit_price, curr_quantity, address_id)
                    row = dao.getIceById(ice_id)
                    result = self.build_ice_dict(row)
                    return jsonify(Part=result), 200
                else:
                    return jsonify(Error="Unexpected attributes in update request"), 400
