from flask import jsonify
from backend.dao.water import WaterDAO


class WaterHandler:

    def build_water_dict(self, row):
        result = {}
        result['water_id'] = row[0]
        result['person_id'] = row[1]
        result['brand'] = row[2]
        result['description'] = row[3]
        result['quantity'] = row[4]
        result['unit_price'] = row[5]
        result['date_posted'] = row[6]
        result['curr_quantity'] = row[7]
        result['is_supply'] = row[8]
        result['type_id'] = row[9]
        result['address_id'] = row[10]
        return result

    def build_water_attributes(self, water_id, person_id, brand, description, quantity, unit_price, date_posted,
                               curr_quantity, is_supply, type_id, address_id):
        result = {
            'water_id': water_id,
            'person_id': person_id,
            'brand': brand,
            'description': description,
            'quantity': quantity,
            'unit_price': unit_price,
            'date_posted': date_posted,
            'curr_quantity': curr_quantity,
            'is_supply': is_supply,
            'type_id': type_id,
            'address_id': address_id,
        }
        return result

    def get_all_water_posts(self):
        dao = WaterDAO()
        result_list = dao.getAllWater()
        for row in result_list:
            result = self.build_water_dict(row)
            result_list.append(result)
        return jsonify(Water_Posts=result_list)

    def get_all_water_supplies(self):
        dao = WaterDAO()
        result_list = dao.getAllWaterSupplies()
        for row in result_list:
            result = self.build_water_dict(row)
            result_list.append(result)
        return jsonify(Water_Supplies=result_list)

    def get_all_water_requests(self):
        dao = WaterDAO()
        result_list = dao.getAllWaterRequests()
        for row in result_list:
            result = self.build_water_dict(row)
            result_list.append(result)
        return jsonify(Water_Requests=result_list)

    def get_all_available_water_supplies(self):
        dao = WaterDAO()
        result_list = dao.getAllAvailableWaterSupplies()
        for row in result_list:
            result = self.build_water_dict(row)
            result_list.append(result)
        return jsonify(Water_Supplies=result_list)

    def get_all_unfulfilled_water_requests(self):
        dao = WaterDAO()
        result_list = dao.getAllUnfulfilledWaterRequests()
        for row in result_list:
            result = self.build_water_dict(row)
            result_list.append(result)
        return jsonify(Water_Requests=result_list)

    def get_water_post_by_id(self, water_id):
        dao = WaterDAO()
        row = dao.getWaterById(water_id)
        if not row:
            return jsonify(Error="Post Not Found"), 404
        else:
            result = self.build_water_dict(row)
        return jsonify(Water_Post=result)

    def get_water_posts_by_person_id(self, person_id):
        dao = WaterDAO()
        result_list = dao.getWaterByPersonId(person_id)
        for row in result_list:
            result = self.build_water_dict(row)
            result_list.append(result)
        return jsonify(Water_Posts=result_list)

    def get_water_supplies_by_person_id(self, person_id):
        dao = WaterDAO()
        result_list = dao.getWaterSuppliesByPersonId(person_id)
        for row in result_list:
            result = self.build_water_dict(row)
            result_list.append(result)
        return jsonify(Water_Posts=result_list)

    def get_water_requests_by_person_id(self, person_id):
        dao = WaterDAO()
        result_list = dao.getWaterRequestsByPersonId(person_id)
        for row in result_list:
            result = self.build_water_dict(row)
            result_list.append(result)
        return jsonify(Water_Posts=result_list)

    def search_water_posts(self, args):
        brand = args['brand']
        water_type = args['water_type']
        dao = WaterDAO()

        if len(args) == 2 and brand and water_type:
            water_list = dao.getWaterByBrandAndType(brand, water_type)
        elif len(args) == 1 and brand:
            water_list = dao.getWaterByBrand(brand)
        elif len(args) == 1 and water_type:
            water_list = dao.getWaterByType(water_type)
        else:
            return jsonify(Error="Malformed query string"), 400
        result_list = []
        for row in water_list:
            result = self.build_water_dict(row)
            result_list.append(result)
        return jsonify(Water_Posts=result_list)

    def search_water_supplies(self, args):
        brand = args['brand']
        max_price = args['unit_price']
        water_type = args['water_type']
        dao = WaterDAO()

        if len(args) == 3 and brand and max_price and water_type:
            water_list = dao.getWaterSuppliesByBrandAndTypeAndMaxPrice(brand, water_type, max_price)
        elif len(args) == 2 and brand and water_type:
            water_list = dao.getWaterSuppliesByBrandAndType(brand, water_type)
        elif len(args) == 1 and brand:
            water_list = dao.getWaterSuppliesByBrand(brand)
        elif len(args) == 1 and max_price:
            water_list = dao.getWaterSuppliesByMaxPrice(max_price)
        elif len(args) == 1 and water_type:
            water_list = dao.getWaterSuppliesByType(water_type)
        else:
            return jsonify(Error="Malformed query string"), 400
        result_list = []
        for row in water_list:
            result = self.build_water_dict(row)
            result_list.append(result)
        return jsonify(Water_Posts=result_list)

    def search_water_requests(self, args):
        brand = args['brand']
        water_type = args['water_type']
        dao = WaterDAO()

        if len(args) == 2 and brand and water_type:
            water_list = dao.getWaterRequestsByBrandAndType(brand, water_type)
        elif len(args) == 1 and brand:
            water_list = dao.getWaterRequestsByBrand(brand)
        elif len(args) == 1 and water_type:
            water_list = dao.getWaterRequestsByType(water_type)
        else:
            return jsonify(Error="Malformed query string"), 400
        result_list = []
        for row in water_list:
            result = self.build_water_dict(row)
            result_list.append(result)
        return jsonify(Water_Posts=result_list)

    def insert_water_supply(self, form):
        if len(form) != 8:
            return jsonify(Error="Malformed post request"), 400
        else:
            dao = WaterDAO()
            person_id = form['person_id']
            brand = form['brand']
            description = form['description']
            quantity = form['quantity']
            unit_price = form['unit_price']
            date_posted = form['date_posted']
            curr_quantity = quantity
            is_supply = True
            type_id = dao.getWaterTypeId(form['water_type'])
            address_id = form['address_id']

            if person_id and brand and description and unit_price and quantity and date_posted and type_id and \
                    address_id:
                water_id = dao.insert(person_id, brand, description, quantity, unit_price, date_posted, curr_quantity,
                                      is_supply, type_id, address_id)
                result = self.build_water_attributes(water_id, person_id, brand, description, quantity, unit_price,
                                                     date_posted, curr_quantity, is_supply, type_id, address_id)
                return jsonify(Supply=result), 201
            else:
                return jsonify(Error="Unexpected attributes in post request"), 400

    def insert_water_supply_json(self, json):
        dao = WaterDAO()
        person_id = json['person_id']
        brand = json['brand']
        description = json['description']
        quantity = json['quantity']
        unit_price = json['unit_price']
        date_posted = json['date_posted']
        curr_quantity = quantity
        is_supply = True
        type_id = dao.getWaterTypeId(json['water_type'])
        address_id = json['address_id']

        if person_id and brand and description and unit_price and quantity and date_posted and type_id and \
                address_id:
            water_id = dao.insert(person_id, brand, description, quantity, unit_price, date_posted, curr_quantity,
                                  is_supply, type_id, address_id)
            result = self.build_water_attributes(water_id, person_id, brand, description, quantity, unit_price,
                                                 date_posted, curr_quantity, is_supply, type_id, address_id)
            return jsonify(Supply=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request"), 400

    def insert_water_request(self, form):
        if len(form) != 8:
            return jsonify(Error="Malformed post request"), 400
        else:
            dao = WaterDAO()
            person_id = form['person_id']
            brand = form['brand']
            description = form['description']
            quantity = form['quantity']
            unit_price = form['unit_price']
            date_posted = form['date_posted']
            curr_quantity = quantity
            is_supply = False
            type_id = dao.getWaterTypeId(form['water_type'])
            address_id = form['address_id']

            if person_id and brand and description and unit_price and quantity and date_posted and type_id and \
                    address_id:
                water_id = dao.insert(person_id, brand, description, quantity, unit_price, date_posted, curr_quantity,
                                      is_supply, type_id, address_id)
                result = self.build_water_attributes(water_id, person_id, brand, description, quantity, unit_price,
                                                     date_posted, curr_quantity, is_supply, type_id, address_id)
                return jsonify(Supply=result), 201
            else:
                return jsonify(Error="Unexpected attributes in post request"), 400

    def insert_water_request_json(self, json):
        dao = WaterDAO()
        person_id = json['person_id']
        brand = json['brand']
        description = json['description']
        quantity = json['quantity']
        unit_price = json['unit_price']
        date_posted = json['date_posted']
        curr_quantity = quantity
        is_supply = False
        type_id = dao.getWaterTypeId(json['water_type'])
        address_id = json['address_id']

        if person_id and brand and description and unit_price and quantity and date_posted and type_id and \
                address_id:
            water_id = dao.insert(person_id, brand, description, quantity, unit_price, date_posted, curr_quantity,
                                  is_supply, type_id, address_id)
            result = self.build_water_attributes(water_id, person_id, brand, description, quantity, unit_price,
                                                 date_posted, curr_quantity, is_supply, type_id, address_id)
            return jsonify(Supply=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request"), 400

    def delete_water_post(self, water_id):
        dao = WaterDAO()
        if not dao.getWaterById(water_id):
            return jsonify(Error="Post not found."), 404
        else:
            dao.delete(water_id)
        return jsonify(DeleteStatus="OK"), 200

    def update_supply(self, water_id, form):
        dao = WaterDAO()
        if not dao.getWaterById(water_id):
            return jsonify(Error="Post not found."), 404
        else:
            if len(form) != 9:
                return jsonify(Error="Malformed update request"), 400
            else:
                brand = form['brand']
                description = form['description']
                unit_price = form['unit_price']
                curr_quantity = form['quantity']
                type_id = dao.getWaterTypeId(form['water_type'])
                address_id = form['address_id']

                if int(curr_quantity) < 0:
                    return jsonify(Error="Cannot put negative value"), 400
                if brand and description and unit_price and curr_quantity and type_id and address_id:
                    dao.update(water_id, brand, description, unit_price, curr_quantity, type_id, address_id)
                    row = dao.getWaterById(water_id)
                    result = self.build_water_dict(row)
                    return jsonify(Part=result), 200
                else:
                    return jsonify(Error="Unexpected attributes in update request"), 400
