from flask import jsonify
from backend.dao.battery import BatteryDAO


class BatteryHandler:

    def build_battery_dict(self, row):
        result = {}
        result['battery_id'] = row[0]
        result['person_id'] = row[1]
        result['brand'] = row[2]
        result['battery_type'] = row[3]
        result['description'] = row[4]
        result['quantity'] = row[5]
        result['unit_price'] = row[6]
        result['date_posted'] = row[7]
        result['curr_quantity'] = row[8]
        result['is_supply'] = row[9]
        result['address_id'] = row[10]
        return result

    def build_battery_attributes(self, battery_id, person_id, brand, battery_type, description, quantity, unit_price, date_posted,
                               curr_quantity, is_supply, address_id):
        result = {
            'battery_id': battery_id,
            'person_id': person_id,
            'brand': brand,
            'battery_type': battery_type,
            'description': description,
            'quantity': quantity,
            'unit_price': unit_price,
            'date_posted': date_posted,
            'curr_quantity': curr_quantity,
            'is_supply': is_supply,
            'address_id': address_id,
        }
        return result

    def get_all_battery_posts(self):
        dao = BatteryDAO()
        result_list = dao.getAllBattery()
        for row in result_list:
            result = self.build_battery_dict(row)
            result_list.append(result)
        return jsonify(Battery_Posts=result_list)

    def get_all_battery_supplies(self):
        dao = BatteryDAO()
        result_list = dao.getAllBatterySupplies()
        for row in result_list:
            result = self.build_battery_dict(row)
            result_list.append(result)
        return jsonify(Battery_Supplies=result_list)

    def get_all_battery_requests(self):
        dao = BatteryDAO()
        result_list = dao.getAllBatteryRequests()
        for row in result_list:
            result = self.build_battery_dict(row)
            result_list.append(result)
        return jsonify(Battery_Requests=result_list)

    def get_all_available_battery_supplies(self):
        dao = BatteryDAO()
        result_list = dao.getAllAvailableBatterySupplies()
        for row in result_list:
            result = self.build_battery_dict(row)
            result_list.append(result)
        return jsonify(Battery_Supplies=result_list)

    def get_all_unfulfilled_battery_requests(self):
        dao = BatteryDAO()
        result_list = dao.getAllUnfulfilledBatteryRequests()
        for row in result_list:
            result = self.build_battery_dict(row)
            result_list.append(result)
        return jsonify(Battery_Requests=result_list)

    def get_battery_post_by_id(self, battery_id):
        dao = BatteryDAO()
        row = dao.getBatteryById(battery_id)
        if not row:
            return jsonify(Error="Post Not Found"), 404
        else:
            result = self.build_battery_dict(row)
        return jsonify(Battery_Post=result)

    def get_battery_posts_by_person_id(self, person_id):
        dao = BatteryDAO()
        result_list = dao.getBatteryByPersonId(person_id)
        for row in result_list:
            result = self.build_battery_dict(row)
            result_list.append(result)
        return jsonify(Battery_Posts=result_list)

    def get_battery_supplies_by_person_id(self, person_id):
        dao = BatteryDAO()
        result_list = dao.getBatterySuppliesByPersonId(person_id)
        for row in result_list:
            result = self.build_battery_dict(row)
            result_list.append(result)
        return jsonify(Battery_Posts=result_list)

    def get_battery_requests_by_person_id(self, person_id):
        dao = BatteryDAO()
        result_list = dao.getBatteryRequestsByPersonId(person_id)
        for row in result_list:
            result = self.build_battery_dict(row)
            result_list.append(result)
        return jsonify(Battery_Posts=result_list)

    def search_battery_posts(self, args):
        brand = args['brand']
        battery_type = args['battery_type']
        dao = BatteryDAO()

        if len(args) == 2 and brand and battery_type:
            battery_list = dao.getBatteryByBrandAndType(brand, battery_type)
        elif len(args) == 1 and brand:
            battery_list = dao.getBatteryByBrand(brand)
        elif len(args) == 1 and battery_type:
            battery_list = dao.getBatteryByType(battery_type)
        else:
            return jsonify(Error="Malformed query string"), 400
        result_list = []
        for row in battery_list:
            result = self.build_battery_dict(row)
            result_list.append(result)
        return jsonify(Battery_Posts=result_list)

    def search_battery_supplies(self, args):
        brand = args['brand']
        max_price = args['unit_price']
        battery_type = args['battery_type']
        dao = BatteryDAO()

        if len(args) == 3 and brand and max_price and battery_type:
            battery_list = dao.getBatterySuppliesByBrandAndTypeAndMaxPrice(brand, battery_type, max_price)
        elif len(args) == 2 and brand and battery_type:
            battery_list = dao.getBatterySuppliesByBrandAndType(brand, battery_type)
        elif len(args) == 1 and brand:
            battery_list = dao.getBatterySuppliesByBrand(brand)
        elif len(args) == 1 and max_price:
            battery_list = dao.getBatterySuppliesByMaxPrice(max_price)
        elif len(args) == 1 and battery_type:
            battery_list = dao.getBatterySuppliesByType(battery_type)
        else:
            return jsonify(Error="Malformed query string"), 400
        result_list = []
        for row in battery_list:
            result = self.build_battery_dict(row)
            result_list.append(result)
        return jsonify(Battery_Posts=result_list)

    def search_battery_requests(self, args):
        brand = args['brand']
        battery_type = args['battery_type']
        dao = BatteryDAO()

        if len(args) == 2 and brand and battery_type:
            battery_list = dao.getBatteryRequestsByBrandAndType(brand, battery_type)
        elif len(args) == 1 and brand:
            battery_list = dao.getBatteryRequestsByBrand(brand)
        elif len(args) == 1 and battery_type:
            battery_list = dao.getBatteryRequestsByType(battery_type)
        else:
            return jsonify(Error="Malformed query string"), 400
        result_list = []
        for row in battery_list:
            result = self.build_battery_dict(row)
            result_list.append(result)
        return jsonify(Battery_Posts=result_list)

    def insert_battery_supply(self, form):
        if len(form) != 8:
            return jsonify(Error="Malformed post request"), 400
        else:
            dao = BatteryDAO()
            person_id = form['person_id']
            brand = form['brand']
            battery_type = form['battery_type']
            description = form['description']
            quantity = form['quantity']
            unit_price = form['unit_price']
            date_posted = form['date_posted']
            curr_quantity = quantity
            is_supply = True
            address_id = form['address_id']

            if person_id and brand and battery_type and description and unit_price and quantity and date_posted and \
                    address_id:
                battery_id = dao.insert(person_id, brand, description, quantity, unit_price, date_posted, curr_quantity,
                                      is_supply, address_id)
                result = self.build_battery_attributes(battery_id, person_id, brand, battery_type, description, quantity, unit_price,
                                                     date_posted, curr_quantity, is_supply, address_id)
                return jsonify(Supply=result), 201
            else:
                return jsonify(Error="Unexpected attributes in post request"), 400

    def insert_battery_supply_json(self, json):
        dao = BatteryDAO()
        person_id = json['person_id']
        brand = json['brand']
        battery_type = json['battery_type']
        description = json['description']
        quantity = json['quantity']
        unit_price = json['unit_price']
        date_posted = json['date_posted']
        curr_quantity = quantity
        is_supply = True
        address_id = json['address_id']

        if person_id and brand and battery_type and description and unit_price and quantity and date_posted and \
                address_id:
            battery_id = dao.insert(person_id, brand, description, quantity, unit_price, date_posted, curr_quantity,
                                  is_supply, address_id)
            result = self.build_battery_attributes(battery_id, person_id, brand, description, quantity, unit_price,
                                                 date_posted, curr_quantity, is_supply, address_id)
            return jsonify(Supply=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request"), 400

    def insert_battery_request(self, form):
        if len(form) != 8:
            return jsonify(Error="Malformed post request"), 400
        else:
            dao = BatteryDAO()
            person_id = form['person_id']
            brand = form['brand']
            battery_type = form['battery_type']
            description = form['description']
            quantity = form['quantity']
            unit_price = form['unit_price']
            date_posted = form['date_posted']
            curr_quantity = quantity
            is_supply = False
            address_id = form['address_id']

            if person_id and brand and battery_type and description and unit_price and quantity and date_posted and \
                    address_id:
                battery_id = dao.insert(person_id, brand, description, quantity, unit_price, date_posted, curr_quantity,
                                      is_supply, address_id)
                result = self.build_battery_attributes(battery_id, person_id, brand, description, quantity, unit_price,
                                                     date_posted, curr_quantity, is_supply, address_id)
                return jsonify(Supply=result), 201
            else:
                return jsonify(Error="Unexpected attributes in post request"), 400

    def insert_battery_request_json(self, json):
        dao = BatteryDAO()
        person_id = json['person_id']
        brand = json['brand']
        battery_type = json['battery_type']
        description = json['description']
        quantity = json['quantity']
        unit_price = json['unit_price']
        date_posted = json['date_posted']
        curr_quantity = quantity
        is_supply = False
        address_id = json['address_id']

        if person_id and brand and battery_type and description and unit_price and quantity and date_posted and \
                address_id:
            battery_id = dao.insert(person_id, brand, description, quantity, unit_price, date_posted, curr_quantity,
                                  is_supply, address_id)
            result = self.build_battery_attributes(battery_id, person_id, brand, description, quantity, unit_price,
                                                 date_posted, curr_quantity, is_supply, address_id)
            return jsonify(Supply=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request"), 400

    def delete_battery_post(self, battery_id):
        dao = BatteryDAO()
        if not dao.getBatteryById(battery_id):
            return jsonify(Error="Post not found."), 404
        else:
            dao.delete(battery_id)
        return jsonify(DeleteStatus="OK"), 200

    def update_supply(self, battery_id, form):
        dao = BatteryDAO()
        if not dao.getBatteryById(battery_id):
            return jsonify(Error="Post not found."), 404
        else:
            if len(form) != 9:
                return jsonify(Error="Malformed update request"), 400
            else:
                brand = form['brand']
                battery_type = form['battery_type']
                description = form['description']
                unit_price = form['unit_price']
                curr_quantity = form['quantity']
                address_id = form['address_id']

                if int(curr_quantity) < 0:
                    return jsonify(Error="Cannot put negative value"), 400
                if brand and battery_type and description and unit_price and curr_quantity and address_id:
                    dao.update(battery_id, brand, battery_type, description, unit_price, curr_quantity, address_id)
                    row = dao.getbatteryById(battery_id)
                    result = self.build_battery_dict(row)
                    return jsonify(Part=result), 200
                else:
                    return jsonify(Error="Unexpected attributes in update request"), 400
