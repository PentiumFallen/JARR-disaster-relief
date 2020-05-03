from flask import jsonify
from backend.dao.power_generator import PowerGeneratorDAO


class PowerGeneratorHandler:

    def build_power_generator_dict(self, row):
        result = {}
        result['generator_id'] = row[0]
        result['person_id'] = row[1]
        result['brand'] = row[2]
        result['watts'] = row[3]
        result['description'] = row[4]
        result['quantity'] = row[5]
        result['unit_price'] = row[6]
        result['date_posted'] = row[7]
        result['curr_quantity'] = row[8]
        result['is_supply'] = row[9]
        result['fuel_used'] = row[10]
        result['address_id'] = row[11]
        return result

    def build_power_generator_attributes(self, generator_id, person_id, brand, watts, description, quantity, unit_price, date_posted,
                               curr_quantity, is_supply, fuel_used, address_id):
        result = {
            'generator_id': generator_id,
            'person_id': person_id,
            'brand': brand,
            'watts': watts,
            'description': description,
            'quantity': quantity,
            'unit_price': unit_price,
            'date_posted': date_posted,
            'curr_quantity': curr_quantity,
            'is_supply': is_supply,
            'fuel_used': fuel_used,
            'address_id': address_id,
        }
        return result

    def get_all_power_generator_posts(self):
        dao = PowerGeneratorDAO()
        result_list = dao.getAllPowerGenerator()
        for row in result_list:
            result = self.build_power_generator_dict(row)
            result_list.append(result)
        return jsonify(Power_Generator_Posts=result_list)

    def get_all_power_generator_supplies(self):
        dao = PowerGeneratorDAO()
        result_list = dao.getAllPowerGeneratorSupplies()
        for row in result_list:
            result = self.build_power_generator_dict(row)
            result_list.append(result)
        return jsonify(Power_Generator_Supplies=result_list)

    def get_all_power_generator_requests(self):
        dao = PowerGeneratorDAO()
        result_list = dao.getAllPowerGeneratorRequests()
        for row in result_list:
            result = self.build_power_generator_dict(row)
            result_list.append(result)
        return jsonify(Power_Generator_Requests=result_list)

    def get_all_available_power_generator_supplies(self):
        dao = PowerGeneratorDAO()
        result_list = dao.getAllAvailablePowerGeneratorSupplies()
        for row in result_list:
            result = self.build_power_generator_dict(row)
            result_list.append(result)
        return jsonify(Power_Generator_Supplies=result_list)

    def get_all_unfulfilled_power_generator_requests(self):
        dao = PowerGeneratorDAO()
        result_list = dao.getAllUnfulfilledPowerGeneratorRequests()
        for row in result_list:
            result = self.build_power_generator_dict(row)
            result_list.append(result)
        return jsonify(Power_Generator_Requests=result_list)

    def get_power_generator_post_by_id(self, generator_id):
        dao = PowerGeneratorDAO()
        row = dao.getPowerGeneratorById(generator_id)
        if not row:
            return jsonify(Error="Post Not Found"), 404
        else:
            result = self.build_power_generator_dict(row)
        return jsonify(Power_Generator_Post=result)

    def get_power_generator_posts_by_person_id(self, person_id):
        dao = PowerGeneratorDAO()
        result_list = dao.getPowerGeneratorByPersonId(person_id)
        for row in result_list:
            result = self.build_power_generator_dict(row)
            result_list.append(result)
        return jsonify(Power_Generator_Posts=result_list)

    def get_power_generator_supplies_by_person_id(self, person_id):
        dao = PowerGeneratorDAO()
        result_list = dao.getPowerGeneratorSuppliesByPersonId(person_id)
        for row in result_list:
            result = self.build_power_generator_dict(row)
            result_list.append(result)
        return jsonify(Power_Generator_Posts=result_list)

    def get_power_generator_requests_by_person_id(self, person_id):
        dao = PowerGeneratorDAO()
        result_list = dao.getPowerGeneratorRequestsByPersonId(person_id)
        for row in result_list:
            result = self.build_power_generator_dict(row)
            result_list.append(result)
        return jsonify(Power_Generator_Posts=result_list)

    def search_power_generator_posts(self, args):
        brand = args['brand']
        watts = args['watts']
        dao = PowerGeneratorDAO()

        if len(args) == 2 and brand and watts:
            power_generator_list = dao.getPowerGeneratorByBrandAndWatts(brand, watts)
        elif len(args) == 1 and brand:
            power_generator_list = dao.getPowerGeneratorByBrand(brand)
        elif len(args) == 1 and watts:
            power_generator_list = dao.getPowerGeneratorByWatts(watts)
        else:
            return jsonify(Error="Malformed query string"), 400
        result_list = []
        for row in power_generator_list:
            result = self.build_power_generator_dict(row)
            result_list.append(result)
        return jsonify(Power_Generator_Posts=result_list)

    def search_power_generator_supplies(self, args):
        brand = args['brand']
        max_price = args['unit_price']
        watts = args['watts']
        dao = PowerGeneratorDAO()

        if len(args) == 3 and brand and max_price and watts:
            power_generator_list = dao.getPowerGeneratorSuppliesByBrandAndWattsAndMaxPrice(brand, watts, max_price)
        elif len(args) == 2 and brand and watts:
            power_generator_list = dao.getPowerGeneratorSuppliesByBrandAndWatts(brand, watts)
        elif len(args) == 1 and brand:
            power_generator_list = dao.getPowerGeneratorSuppliesByBrand(brand)
        elif len(args) == 1 and max_price:
            power_generator_list = dao.getPowerGeneratorrSuppliesByMaxPrice(max_price)
        elif len(args) == 1 and watts:
            power_generator_list = dao.getPowerGeneratorSuppliesByWatts(watts)
        else:
            return jsonify(Error="Malformed query string"), 400
        result_list = []
        for row in power_generator_list:
            result = self.build_power_generator_dict(row)
            result_list.append(result)
        return jsonify(Power_Penerator_Posts=result_list)

    def search_power_generator_requests(self, args):
        brand = args['brand']
        watts = args['watts']
        dao = PowerGeneratorDAO()

        if len(args) == 2 and brand and watts:
            power_generator_list = dao.getPowerGeneratorRequestsByBrandAndWatts(brand, watts)
        elif len(args) == 1 and brand:
            power_generator_list = dao.getPowerGeneratorRequestsByBrand(brand)
        elif len(args) == 1 and watts:
            power_generator_list = dao.getPowerGeneratorRequestsByWatts(watts)
        else:
            return jsonify(Error="Malformed query string"), 400
        result_list = []
        for row in power_generator_list:
            result = self.build_power_generator_dict(row)
            result_list.append(result)
        return jsonify(Power_Generator_Posts=result_list)

    def insert_power_generator_supply(self, form):
        if len(form) != 8:
            return jsonify(Error="Malformed post request"), 400
        else:
            dao = PowerGeneratorDAO()
            person_id = form['person_id']
            brand = form['brand']
            watts = form['watts']
            description = form['description']
            quantity = form['quantity']
            unit_price = form['unit_price']
            date_posted = form['date_posted']
            curr_quantity = quantity
            is_supply = True
            fuel_used = False
            address_id = form['address_id']

            if person_id and brand and watts and description and unit_price and quantity and date_posted and \
                    address_id:
                generator_id = dao.insert(person_id, brand, watts, description, quantity, unit_price, date_posted, curr_quantity,
                                      is_supply, fuel_used, address_id)
                result = self.build_power_generator_attributes(generator_id, person_id, brand, watts, description, quantity, unit_price,
                                                     date_posted, curr_quantity, is_supply, fuel_used, address_id)
                return jsonify(Supply=result), 201
            else:
                return jsonify(Error="Unexpected attributes in post request"), 400

    def insert_power_generator_supply_json(self, json):
        dao = PowerGeneratorDAO()
        person_id = json['person_id']
        brand = json['brand']
        watts = json['watts']
        description = json['description']
        quantity = json['quantity']
        unit_price = json['unit_price']
        date_posted = json['date_posted']
        curr_quantity = quantity
        is_supply = True
        fuel_used = False
        address_id = json['address_id']

        if person_id and brand and watts and description and unit_price and quantity and date_posted and \
                address_id:
            generator_id = dao.insert(person_id, brand, watts, description, quantity, unit_price, date_posted, curr_quantity,
                                  is_supply, fuel_used, address_id)
            result = self.build_power_generator_attributes(generator_id, person_id, brand, watts, description, quantity, unit_price,
                                                 date_posted, curr_quantity, is_supply, fuel_used, address_id)
            return jsonify(Supply=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request"), 400

    def insert_power_generator_request(self, form):
        if len(form) != 8:
            return jsonify(Error="Malformed post request"), 400
        else:
            dao = PowerGeneratorDAO()
            person_id = form['person_id']
            brand = form['brand']
            watts = form['watts']
            description = form['description']
            quantity = form['quantity']
            unit_price = form['unit_price']
            date_posted = form['date_posted']
            curr_quantity = quantity
            is_supply = False
            fuel_used = False
            address_id = form['address_id']

            if person_id and brand and watts and description and unit_price and quantity and date_posted and \
                    address_id:
                generator_id = dao.insert(person_id, brand, watts, description, quantity, unit_price, date_posted, curr_quantity,
                                      is_supply, fuel_used, address_id)
                result = self.build_power_generator_attributes(generator_id, person_id, brand, watts, description, quantity, unit_price,
                                                     date_posted, curr_quantity, is_supply, fuel_used, address_id)
                return jsonify(Supply=result), 201
            else:
                return jsonify(Error="Unexpected attributes in post request"), 400

    def insert_power_generator_request_json(self, json):
        dao = PowerGeneratorDAO()
        person_id = json['person_id']
        brand = json['brand']
        watts = json['watts']
        description = json['description']
        quantity = json['quantity']
        unit_price = json['unit_price']
        date_posted = json['date_posted']
        curr_quantity = quantity
        is_supply = False
        fuel_used = False
        address_id = json['address_id']

        if person_id and brand and watts and description and unit_price and quantity and date_posted and \
                address_id:
            generator_id = dao.insert(person_id, brand, watts, description, quantity, unit_price, date_posted, curr_quantity,
                                  is_supply, fuel_used, address_id)
            result = self.build_power_generator_attributes(generator_id, person_id, brand, watts, description, quantity, unit_price,
                                                 date_posted, curr_quantity, is_supply, fuel_used, address_id)
            return jsonify(Supply=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request"), 400

    def delete_power_generator_post(self, generator_id):
        dao = PowerGeneratorDAO()
        if not dao.getPowerGeneratorById(generator_id):
            return jsonify(Error="Post not found."), 404
        else:
            dao.delete(generator_id)
        return jsonify(DeleteStatus="OK"), 200

    def update_supply(self, generator_id, form):
        dao = PowerGeneratorDAO()
        if not dao.getPowerGeneratorById(generator_id):
            return jsonify(Error="Post not found."), 404
        else:
            if len(form) != 9:
                return jsonify(Error="Malformed update request"), 400
            else:
                brand = form['brand']
                watts = form['watts']
                description = form['description']
                unit_price = form['unit_price']
                curr_quantity = form['quantity']
                address_id = form['address_id']

                if int(curr_quantity) < 0:
                    return jsonify(Error="Cannot put negative value"), 400
                if brand and watts and description and unit_price and curr_quantity and address_id:
                    dao.update(generator_id, brand, watts, description, unit_price, curr_quantity, address_id)
                    row = dao.getpower_generatorById(generator_id)
                    result = self.build_power_generator_dict(row)
                    return jsonify(Part=result), 200
                else:
                    return jsonify(Error="Unexpected attributes in update request"), 400
