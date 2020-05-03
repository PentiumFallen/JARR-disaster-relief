from flask import jsonify
from backend.dao.fuel import FuelDAO


class FuelHandler:

    def build_fuel_dict(self, row):
        result = {}
        result['fuel_id'] = row[0]
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

    def build_fuel_attributes(self, fuel_id, person_id, brand, description, quantity, unit_price, date_posted,
                              curr_quantity, is_supply, type_id, address_id):
        result = {
            'fuel_id': fuel_id,
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

    def get_all_fuel_posts(self):
        dao = FuelDAO()
        result_list = dao.getAllFuel()
        for row in result_list:
            result = self.build_fuel_dict(row)
            result_list.append(result)
        return jsonify(Fuel_Posts=result_list)

    def get_all_fuel_supplies(self):
        dao = FuelDAO()
        result_list = dao.getAllFuelSupplies()
        for row in result_list:
            result = self.build_fuel_dict(row)
            result_list.append(result)
        return jsonify(Fuel_Supplies=result_list)

    def get_all_fuel_requests(self):
        dao = FuelDAO()
        result_list = dao.getAllFuelRequests()
        for row in result_list:
            result = self.build_fuel_dict(row)
            result_list.append(result)
        return jsonify(Fuel_Requests=result_list)

    def get_all_available_fuel_supplies(self):
        dao = FuelDAO()
        result_list = dao.getAllAvailableFuelSupplies()
        for row in result_list:
            result = self.build_fuel_dict(row)
            result_list.append(result)
        return jsonify(Fuel_Supplies=result_list)

    def get_all_unfulfilled_fuel_requests(self):
        dao = FuelDAO()
        result_list = dao.getAllUnfulfilledFuelRequests()
        for row in result_list:
            result = self.build_fuel_dict(row)
            result_list.append(result)
        return jsonify(Fuel_Requests=result_list)

    def get_fuel_post_by_id(self, fuel_id):
        dao = FuelDAO()
        row = dao.getFuelById(fuel_id)
        if not row:
            return jsonify(Error="Post Not Found"), 404
        else:
            result = self.build_fuel_dict(row)
        return jsonify(Fuel_Post=result)

    def get_fuel_posts_by_person_id(self, person_id):
        dao = FuelDAO()
        result_list = dao.getFuelByPersonId(person_id)
        for row in result_list:
            result = self.build_fuel_dict(row)
            result_list.append(result)
        return jsonify(Fuel_Posts=result_list)

    def get_fuel_supplies_by_person_id(self, person_id):
        dao = FuelDAO()
        result_list = dao.getFuelSuppliesByPersonId(person_id)
        for row in result_list:
            result = self.build_fuel_dict(row)
            result_list.append(result)
        return jsonify(Fuel_Posts=result_list)

    def get_fuel_requests_by_person_id(self, person_id):
        dao = FuelDAO()
        result_list = dao.getFuelRequestsByPersonId(person_id)
        for row in result_list:
            result = self.build_fuel_dict(row)
            result_list.append(result)
        return jsonify(Fuel_Posts=result_list)

    def search_fuel_posts(self, args):
        brand = args['brand']
        fuel_type = args['fuel_type']
        dao = FuelDAO()

        if len(args) == 2 and brand and fuel_type:
            fuel_list = dao.getFuelByBrandAndType(brand, fuel_type)
        elif len(args) == 1 and brand:
            fuel_list = dao.getFuelByBrand(brand)
        elif len(args) == 1 and fuel_type:
            fuel_list = dao.getFuelByType(fuel_type)
        else:
            return jsonify(Error="Malformed query string"), 400
        result_list = []
        for row in fuel_list:
            result = self.build_fuel_dict(row)
            result_list.append(result)
        return jsonify(Fuel_Posts=result_list)

    def search_fuel_supplies(self, args):
        brand = args['brand']
        max_price = args['unit_price']
        fuel_type = args['fuel_type']
        dao = FuelDAO()

        if len(args) == 3 and brand and max_price and fuel_type:
            fuel_list = dao.getFuelSuppliesByBrandAndTypeAndMaxPrice(brand, fuel_type, max_price)
        elif len(args) == 2 and brand and fuel_type:
            fuel_list = dao.getFuelSuppliesByBrandAndType(brand, fuel_type)
        elif len(args) == 1 and brand:
            fuel_list = dao.getFuelSuppliesByBrand(brand)
        elif len(args) == 1 and max_price:
            fuel_list = dao.getFuelSuppliesByMaxPrice(max_price)
        elif len(args) == 1 and fuel_type:
            fuel_list = dao.getFuelSuppliesByType(fuel_type)
        else:
            return jsonify(Error="Malformed query string"), 400
        result_list = []
        for row in fuel_list:
            result = self.build_fuel_dict(row)
            result_list.append(result)
        return jsonify(Fuel_Posts=result_list)

    def search_fuel_requests(self, args):
        brand = args['brand']
        fuel_type = args['fuel_type']
        dao = FuelDAO()

        if len(args) == 2 and brand and fuel_type:
            fuel_list = dao.getFuelRequestsByBrandAndType(brand, fuel_type)
        elif len(args) == 1 and brand:
            fuel_list = dao.getFuelRequestsByBrand(brand)
        elif len(args) == 1 and fuel_type:
            fuel_list = dao.getFuelRequestsByType(fuel_type)
        else:
            return jsonify(Error="Malformed query string"), 400
        result_list = []
        for row in fuel_list:
            result = self.build_fuel_dict(row)
            result_list.append(result)
        return jsonify(Fuel_Posts=result_list)

    def insert_fuel_supply(self, form):
        if len(form) != 8:
            return jsonify(Error="Malformed post request"), 400
        else:
            dao = FuelDAO()
            person_id = form['person_id']
            brand = form['brand']
            description = form['description']
            quantity = form['quantity']
            unit_price = form['unit_price']
            date_posted = form['date_posted']
            curr_quantity = quantity
            is_supply = True
            type_id = dao.getFuelTypeId(form['fuel_type'])
            address_id = form['address_id']

            if person_id and brand and description and unit_price and quantity and date_posted and type_id and \
                    address_id:
                fuel_id = dao.insert(person_id, brand, description, quantity, unit_price, date_posted, curr_quantity,
                                     is_supply, type_id, address_id)
                result = self.build_fuel_attributes(fuel_id, person_id, brand, description, quantity, unit_price,
                                                    date_posted, curr_quantity, is_supply, type_id, address_id)
                return jsonify(Supply=result), 201
            else:
                return jsonify(Error="Unexpected attributes in post request"), 400

    def insert_fuel_supply_json(self, json):
        dao = FuelDAO()
        person_id = json['person_id']
        brand = json['brand']
        description = json['description']
        quantity = json['quantity']
        unit_price = json['unit_price']
        date_posted = json['date_posted']
        curr_quantity = quantity
        is_supply = True
        type_id = dao.getFuelTypeId(json['fuel_type'])
        address_id = json['address_id']

        if person_id and brand and description and unit_price and quantity and date_posted and type_id and \
                address_id:
            fuel_id = dao.insert(person_id, brand, description, quantity, unit_price, date_posted, curr_quantity,
                                 is_supply, type_id, address_id)
            result = self.build_fuel_attributes(fuel_id, person_id, brand, description, quantity, unit_price,
                                                date_posted, curr_quantity, is_supply, type_id, address_id)
            return jsonify(Supply=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request"), 400

    def insert_fuel_request(self, form):
        if len(form) != 8:
            return jsonify(Error="Malformed post request"), 400
        else:
            dao = FuelDAO()
            person_id = form['person_id']
            brand = form['brand']
            description = form['description']
            quantity = form['quantity']
            unit_price = form['unit_price']
            date_posted = form['date_posted']
            curr_quantity = quantity
            is_supply = False
            type_id = dao.getFuelTypeId(form['fuel_type'])
            address_id = form['address_id']

            if person_id and brand and description and unit_price and quantity and date_posted and type_id and \
                    address_id:
                fuel_id = dao.insert(person_id, brand, description, quantity, unit_price, date_posted, curr_quantity,
                                     is_supply, type_id, address_id)
                result = self.build_fuel_attributes(fuel_id, person_id, brand, description, quantity, unit_price,
                                                    date_posted, curr_quantity, is_supply, type_id, address_id)
                return jsonify(Supply=result), 201
            else:
                return jsonify(Error="Unexpected attributes in post request"), 400

    def insert_fuel_request_json(self, json):
        dao = FuelDAO()
        person_id = json['person_id']
        brand = json['brand']
        description = json['description']
        quantity = json['quantity']
        unit_price = json['unit_price']
        date_posted = json['date_posted']
        curr_quantity = quantity
        is_supply = False
        type_id = dao.getFuelTypeId(json['fuel_type'])
        address_id = json['address_id']

        if person_id and brand and description and unit_price and quantity and date_posted and type_id and \
                address_id:
            fuel_id = dao.insert(person_id, brand, description, quantity, unit_price, date_posted, curr_quantity,
                                 is_supply, type_id, address_id)
            result = self.build_fuel_attributes(fuel_id, person_id, brand, description, quantity, unit_price,
                                                date_posted, curr_quantity, is_supply, type_id, address_id)
            return jsonify(Supply=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request"), 400

    def delete_fuel_post(self, fuel_id):
        dao = FuelDAO()
        if not dao.getFuelById(fuel_id):
            return jsonify(Error="Post not found."), 404
        else:
            dao.delete(fuel_id)
        return jsonify(DeleteStatus="OK"), 200

    def update_fuel_post(self, fuel_id, form):
        dao = FuelDAO()
        if not dao.getFuelById(fuel_id):
            return jsonify(Error="Post not found."), 404
        else:
            if len(form) != 9:
                return jsonify(Error="Malformed update request"), 400
            else:
                brand = form['brand']
                description = form['description']
                unit_price = form['unit_price']
                curr_quantity = form['quantity']
                type_id = dao.getFuelTypeId(form['fuel_type'])
                address_id = form['address_id']

                if int(curr_quantity) < 0:
                    return jsonify(Error="Cannot put negative value"), 400
                if brand and description and unit_price and curr_quantity and type_id and address_id:
                    dao.update(fuel_id, brand, description, unit_price, curr_quantity, type_id, address_id)
                    row = dao.getFuelById(fuel_id)
                    result = self.build_fuel_dict(row)
                    return jsonify(Part=result), 200
                else:
                    return jsonify(Error="Unexpected attributes in update request"), 400
