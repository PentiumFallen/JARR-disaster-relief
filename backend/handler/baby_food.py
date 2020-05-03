from flask import jsonify
from backend.dao.baby_food import BabyFoodDAO


class BabyFoodHandler:

    def build_bf_dict(self, row):
        result = {}
        result['bf_id'] = row[0]
        result['person_id'] = row[1]
        result['brand'] = row[2]
        result['flavor'] = row[3]
        result['description'] = row[4]
        result['quantity'] = row[5]
        result['unit_price'] = row[6]
        result['date_posted'] = row[7]
        result['curr_quantity'] = row[8]
        result['is_supply'] = row[9]
        result['address_id'] = row[10]
        return result

    def build_bf_attributes(self, bf_id, person_id, brand, flavor, description, quantity, unit_price, date_posted,
                            curr_quantity, is_supply, address_id):
        result = {
            'bf_id': bf_id,
            'person_id': person_id,
            'brand': brand,
            'flavor': flavor,
            'description': description,
            'quantity': quantity,
            'unit_price': unit_price,
            'date_posted': date_posted,
            'curr_quantity': curr_quantity,
            'is_supply': is_supply,
            'address_id': address_id,
        }
        return result

    def get_all_bf_posts(self):
        dao = BabyFoodDAO()
        result_list = dao.getAllBabyFood()
        for row in result_list:
            result = self.build_bf_dict(row)
            result_list.append(result)
        return jsonify(Baby_Food_Posts=result_list)

    def get_all_bf_supplies(self):
        dao = BabyFoodDAO()
        result_list = dao.getAllBabyFoodSupplies()
        for row in result_list:
            result = self.build_bf_dict(row)
            result_list.append(result)
        return jsonify(Baby_Food_Supplies=result_list)

    def get_all_bf_requests(self):
        dao = BabyFoodDAO()
        result_list = dao.getAllBabyFoodRequests()
        for row in result_list:
            result = self.build_bf_dict(row)
            result_list.append(result)
        return jsonify(Baby_Food_Requests=result_list)

    def get_all_available_bf_supplies(self):
        dao = BabyFoodDAO()
        result_list = dao.getAllAvailableBabyFoodSupplies()
        for row in result_list:
            result = self.build_bf_dict(row)
            result_list.append(result)
        return jsonify(Baby_Food_Supplies=result_list)

    def get_all_unfulfilled_bf_requests(self):
        dao = BabyFoodDAO()
        result_list = dao.getAllUnfulfilledBabyFoodRequests()
        for row in result_list:
            result = self.build_bf_dict(row)
            result_list.append(result)
        return jsonify(Baby_Food_Requests=result_list)

    def get_bf_post_by_id(self, bf_id):
        dao = BabyFoodDAO()
        row = dao.getBabyFoodById(bf_id)
        if not row:
            return jsonify(Error="Post Not Found"), 404
        else:
            result = self.build_bf_dict(row)
        return jsonify(Baby_Food_Post=result)

    def get_bf_posts_by_person_id(self, person_id):
        dao = BabyFoodDAO()
        result_list = dao.getBabyFoodByPersonId(person_id)
        for row in result_list:
            result = self.build_bf_dict(row)
            result_list.append(result)
        return jsonify(Baby_Food_Posts=result_list)

    def get_bf_supplies_by_person_id(self, person_id):
        dao = BabyFoodDAO()
        result_list = dao.getBabyFoodSuppliesByPersonId(person_id)
        for row in result_list:
            result = self.build_bf_dict(row)
            result_list.append(result)
        return jsonify(Baby_Food_Posts=result_list)

    def get_bf_requests_by_person_id(self, person_id):
        dao = BabyFoodDAO()
        result_list = dao.getBabyFoodRequestsByPersonId(person_id)
        for row in result_list:
            result = self.build_bf_dict(row)
            result_list.append(result)
        return jsonify(Baby_Food_Posts=result_list)

    def search_bf_posts(self, args):
        brand = args['brand']
        flavor = args['flavor']
        dao = BabyFoodDAO()

        if len(args) == 2 and brand and flavor:
            bf_list = dao.getBabyFoodByBrandAndFlavor(brand, flavor)
        elif len(args) == 1 and brand:
            bf_list = dao.getBabyFoodByBrand(brand)
        elif len(args) == 1 and flavor:
            bf_list = dao.getBabyFoodByFlavor(flavor)
        else:
            return jsonify(Error="Malformed query string"), 400
        result_list = []
        for row in bf_list:
            result = self.build_bf_dict(row)
            result_list.append(result)
        return jsonify(Baby_Food_Posts=result_list)

    def search_bf_supplies(self, args):
        brand = args['brand']
        max_price = args['unit_price']
        flavor = args['flavor']
        dao = BabyFoodDAO()

        if len(args) == 3 and brand and max_price and flavor:
            bf_list = dao.getBabyFoodSuppliesByBrandAndFlavorAndMaxPrice(brand, flavor, max_price)
        elif len(args) == 2 and brand and flavor:
            bf_list = dao.getBabyFoodSuppliesByBrandAndFlavor(brand, flavor)
        elif len(args) == 1 and brand:
            bf_list = dao.getBabyFoodSuppliesByBrand(brand)
        elif len(args) == 1 and max_price:
            bf_list = dao.getBabyFoodSuppliesByMaxPrice(max_price)
        elif len(args) == 1 and flavor:
            bf_list = dao.getBabyFoodSuppliesByFlavor(flavor)
        else:
            return jsonify(Error="Malformed query string"), 400
        result_list = []
        for row in bf_list:
            result = self.build_bf_dict(row)
            result_list.append(result)
        return jsonify(Baby_Food_Posts=result_list)

    def search_bf_requests(self, args):
        brand = args['brand']
        flavor = args['flavor']
        dao = BabyFoodDAO()

        if len(args) == 2 and brand and flavor:
            bf_list = dao.getBabyFoodRequestsByBrandAndFlavor(brand, flavor)
        elif len(args) == 1 and brand:
            bf_list = dao.getBabyFoodRequestsByBrand(brand)
        elif len(args) == 1 and flavor:
            bf_list = dao.getBabyFoodRequestsByFlavor(flavor)
        else:
            return jsonify(Error="Malformed query string"), 400
        result_list = []
        for row in bf_list:
            result = self.build_bf_dict(row)
            result_list.append(result)
        return jsonify(Baby_Food_Posts=result_list)

    def insert_bf_supply(self, form):
        if len(form) != 8:
            return jsonify(Error="Malformed post request"), 400
        else:
            dao = BabyFoodDAO()
            person_id = form['person_id']
            brand = form['brand']
            flavor = form['flavor']
            description = form['description']
            quantity = form['quantity']
            unit_price = form['unit_price']
            date_posted = form['date_posted']
            curr_quantity = quantity
            is_supply = True
            address_id = form['address_id']

            if person_id and brand and description and unit_price and quantity and date_posted and flavor and \
                    address_id:
                bf_id = dao.insert(person_id, brand, flavor, description, quantity, unit_price, date_posted,
                                   curr_quantity, is_supply, address_id)
                result = self.build_bf_attributes(bf_id, person_id, brand, flavor, description, quantity, unit_price,
                                                  date_posted, curr_quantity, is_supply, address_id)
                return jsonify(Supply=result), 201
            else:
                return jsonify(Error="Unexpected attributes in post request"), 400

    def insert_bf_supply_json(self, json):
        dao = BabyFoodDAO()
        person_id = json['person_id']
        brand = json['brand']
        flavor = json['flavor']
        description = json['description']
        quantity = json['quantity']
        unit_price = json['unit_price']
        date_posted = json['date_posted']
        curr_quantity = quantity
        is_supply = True
        address_id = json['address_id']

        if person_id and brand and description and unit_price and quantity and date_posted and flavor and \
                address_id:
            bf_id = dao.insert(person_id, brand, flavor, description, quantity, unit_price, date_posted, curr_quantity,
                               is_supply, address_id)
            result = self.build_bf_attributes(bf_id, person_id, brand, flavor, description, quantity, unit_price,
                                              date_posted, curr_quantity, is_supply, address_id)
            return jsonify(Supply=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request"), 400

    def insert_bf_request(self, form):
        if len(form) != 8:
            return jsonify(Error="Malformed post request"), 400
        else:
            dao = BabyFoodDAO()
            person_id = form['person_id']
            brand = form['brand']
            flavor = form['flavor']
            description = form['description']
            quantity = form['quantity']
            unit_price = form['unit_price']
            date_posted = form['date_posted']
            curr_quantity = quantity
            is_supply = False
            address_id = form['address_id']

            if person_id and brand and description and unit_price and quantity and date_posted and flavor and \
                    address_id:
                bf_id = dao.insert(person_id, brand, flavor, description, quantity, unit_price, date_posted, curr_quantity,
                                   is_supply, address_id)
                result = self.build_bf_attributes(bf_id, person_id, brand, flavor, description, quantity, unit_price,
                                                  date_posted, curr_quantity, is_supply, address_id)
                return jsonify(Supply=result), 201
            else:
                return jsonify(Error="Unexpected attributes in post request"), 400

    def insert_bf_request_json(self, json):
        dao = BabyFoodDAO()
        person_id = json['person_id']
        brand = json['brand']
        flavor = json['flavor']
        description = json['description']
        quantity = json['quantity']
        unit_price = json['unit_price']
        date_posted = json['date_posted']
        curr_quantity = quantity
        is_supply = False
        address_id = json['address_id']

        if person_id and brand and description and unit_price and quantity and date_posted and flavor and \
                address_id:
            bf_id = dao.insert(person_id, brand, flavor, description, quantity, unit_price, date_posted, curr_quantity,
                               is_supply, address_id)
            result = self.build_bf_attributes(bf_id, person_id, brand, flavor, description, quantity, unit_price,
                                              date_posted, curr_quantity, is_supply, address_id)
            return jsonify(Supply=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request"), 400

    def delete_bf_post(self, bf_id):
        dao = BabyFoodDAO()
        if not dao.getBabyFoodById(bf_id):
            return jsonify(Error="Post not found."), 404
        else:
            dao.delete(bf_id)
        return jsonify(DeleteStatus="OK"), 200

    def update_bf_post(self, bf_id, form):
        dao = BabyFoodDAO()
        if not dao.getBabyFoodById(bf_id):
            return jsonify(Error="Post not found."), 404
        else:
            if len(form) != 9:
                return jsonify(Error="Malformed update request"), 400
            else:
                brand = form['brand']
                flavor = form['flavor']
                description = form['description']
                unit_price = form['unit_price']
                curr_quantity = form['quantity']
                address_id = form['address_id']

                if int(curr_quantity) < 0:
                    return jsonify(Error="Cannot put negative value"), 400
                if brand and description and unit_price and curr_quantity and flavor and address_id:
                    dao.update(bf_id, brand, flavor, description, unit_price, curr_quantity, address_id)
                    row = dao.getBabyFoodById(bf_id)
                    result = self.build_bf_dict(row)
                    return jsonify(Part=result), 200
                else:
                    return jsonify(Error="Unexpected attributes in update request"), 400
