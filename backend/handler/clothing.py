from flask import jsonify
from backend.dao.clothing import ClothingDAO


class ClothingHandler:

    def build_clothing_dict(self, row):
        result = {}
        result['clothing_id'] = row[0]
        result['person_id'] = row[1]
        result['brand'] = row[2]
        result['clothing_type'] = row[3]
        result['description'] = row[4]
        result['quantity'] = row[5]
        result['unit_price'] = row[6]
        result['date_posted'] = row[7]
        result['curr_quantity'] = row[8]
        result['is_supply'] = row[9]
        result['address_id'] = row[10]
        return result

    def build_clothing_attributes(self, clothing_id, person_id, brand, clothing_type, description, quantity, unit_price, date_posted,
                               curr_quantity, is_supply, address_id):
        result = {
            'clothing_id': clothing_id,
            'person_id': person_id,
            'brand': brand,
            'clothing_type': clothing_type,
            'description': description,
            'quantity': quantity,
            'unit_price': unit_price,
            'date_posted': date_posted,
            'curr_quantity': curr_quantity,
            'is_supply': is_supply,
            'address_id': address_id,
        }
        return result

    def get_all_clothing_posts(self):
        dao = ClothingDAO()
        result_list = dao.getAllClothing()
        for row in result_list:
            result = self.build_clothing_dict(row)
            result_list.append(result)
        return jsonify(Clothing_Posts=result_list)

    def get_all_clothing_supplies(self):
        dao = ClothingDAO()
        result_list = dao.getAllClothingSupplies()
        for row in result_list:
            result = self.build_clothing_dict(row)
            result_list.append(result)
        return jsonify(Clothing_Supplies=result_list)

    def get_all_clothing_requests(self):
        dao = ClothingDAO()
        result_list = dao.getAllClothingRequests()
        for row in result_list:
            result = self.build_clothing_dict(row)
            result_list.append(result)
        return jsonify(Clothing_Requests=result_list)

    def get_all_available_clothing_supplies(self):
        dao = ClothingDAO()
        result_list = dao.getAllAvailableClothingSupplies()
        for row in result_list:
            result = self.build_clothing_dict(row)
            result_list.append(result)
        return jsonify(Clothing_Supplies=result_list)

    def get_all_unfulfilled_clothing_requests(self):
        dao = ClothingDAO()
        result_list = dao.getAllUnfulfilledClothingRequests()
        for row in result_list:
            result = self.build_clothing_dict(row)
            result_list.append(result)
        return jsonify(Clothing_Requests=result_list)

    def get_clothing_post_by_id(self, clothing_id):
        dao = ClothingDAO()
        row = dao.getClothingById(clothing_id)
        if not row:
            return jsonify(Error="Post Not Found"), 404
        else:
            result = self.build_clothing_dict(row)
        return jsonify(clothing_Post=result)

    def get_clothing_posts_by_person_id(self, person_id):
        dao = ClothingDAO()
        result_list = dao.getClothingByPersonId(person_id)
        for row in result_list:
            result = self.build_clothing_dict(row)
            result_list.append(result)
        return jsonify(Clothing_Posts=result_list)

    def get_clothing_supplies_by_person_id(self, person_id):
        dao = ClothingDAO()
        result_list = dao.getClothingSuppliesByPersonId(person_id)
        for row in result_list:
            result = self.build_clothing_dict(row)
            result_list.append(result)
        return jsonify(Clothing_Posts=result_list)

    def get_clothing_requests_by_person_id(self, person_id):
        dao = ClothingDAO()
        result_list = dao.getClothingRequestsByPersonId(person_id)
        for row in result_list:
            result = self.build_clothing_dict(row)
            result_list.append(result)
        return jsonify(Clothing_Posts=result_list)

    def search_clothing_posts(self, args):
        brand = args['brand']
        clothing_type = args['clothing_type']
        dao = ClothingDAO()

        if len(args) == 2 and brand and clothing_type:
            clothing_list = dao.getClothingByBrandAndType(brand, clothing_type)
        elif len(args) == 1 and brand:
            clothing_list = dao.getClothingByBrand(brand)
        elif len(args) == 1 and clothing_type:
            clothing_list = dao.getClothingByType(clothing_type)
        else:
            return jsonify(Error="Malformed query string"), 400
        result_list = []
        for row in clothing_list:
            result = self.build_clothing_dict(row)
            result_list.append(result)
        return jsonify(Clothing_Posts=result_list)

    def search_clothing_supplies(self, args):
        brand = args['brand']
        max_price = args['unit_price']
        clothing_type = args['clothing_type']
        dao = ClothingDAO()

        if len(args) == 3 and brand and max_price and clothing_type:
            clothing_list = dao.getClothingSuppliesByBrandAndTypeAndMaxPrice(brand, clothing_type, max_price)
        elif len(args) == 2 and brand and clothing_type:
            clothing_list = dao.getClothingSuppliesByBrandAndType(brand, clothing_type)
        elif len(args) == 1 and brand:
            clothing_list = dao.getClothingSuppliesByBrand(brand)
        elif len(args) == 1 and max_price:
            clothing_list = dao.getClothingSuppliesByMaxPrice(max_price)
        elif len(args) == 1 and clothing_type:
            clothing_list = dao.getClothingSuppliesByType(clothing_type)
        else:
            return jsonify(Error="Malformed query string"), 400
        result_list = []
        for row in clothing_list:
            result = self.build_clothing_dict(row)
            result_list.append(result)
        return jsonify(Clothing_Posts=result_list)

    def search_clothing_requests(self, args):
        brand = args['brand']
        clothing_type = args['clothing_type']
        dao = ClothingDAO()

        if len(args) == 2 and brand and clothing_type:
            clothing_list = dao.getClothingRequestsByBrandAndType(brand, clothing_type)
        elif len(args) == 1 and brand:
            clothing_list = dao.getClothingRequestsByBrand(brand)
        elif len(args) == 1 and clothing_type:
            clothing_list = dao.getClothingRequestsByType(clothing_type)
        else:
            return jsonify(Error="Malformed query string"), 400
        result_list = []
        for row in clothing_list:
            result = self.build_clothing_dict(row)
            result_list.append(result)
        return jsonify(Clothing_Posts=result_list)

    def insert_clothing_supply(self, form):
        if len(form) != 8:
            return jsonify(Error="Malformed post request"), 400
        else:
            dao = ClothingDAO()
            person_id = form['person_id']
            brand = form['brand']
            clothing_type = form['clothing_type']
            description = form['description']
            quantity = form['quantity']
            unit_price = form['unit_price']
            date_posted = form['date_posted']
            curr_quantity = quantity
            is_supply = True
            address_id = form['address_id']

            if person_id and brand and clothing_type and description and unit_price and quantity and date_posted and \
                    address_id:
                clothing_id = dao.insert(person_id, brand, description, quantity, unit_price, date_posted, curr_quantity,
                                      is_supply, address_id)
                result = self.build_clothing_attributes(clothing_id, person_id, brand, clothing_type, description, quantity, unit_price,
                                                     date_posted, curr_quantity, is_supply, address_id)
                return jsonify(Supply=result), 201
            else:
                return jsonify(Error="Unexpected attributes in post request"), 400

    def insert_clothing_supply_json(self, json):
        dao = ClothingDAO()
        person_id = json['person_id']
        brand = json['brand']
        clothing_type = json['clothing_type']
        description = json['description']
        quantity = json['quantity']
        unit_price = json['unit_price']
        date_posted = json['date_posted']
        curr_quantity = quantity
        is_supply = True
        address_id = json['address_id']

        if person_id and brand and clothing_type and description and unit_price and quantity and date_posted and \
                address_id:
            clothing_id = dao.insert(person_id, brand, description, quantity, unit_price, date_posted, curr_quantity,
                                  is_supply, address_id)
            result = self.build_clothing_attributes(clothing_id, person_id, brand, description, quantity, unit_price,
                                                 date_posted, curr_quantity, is_supply, address_id)
            return jsonify(Supply=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request"), 400

    def insert_clothing_request(self, form):
        if len(form) != 8:
            return jsonify(Error="Malformed post request"), 400
        else:
            dao = ClothingDAO()
            person_id = form['person_id']
            brand = form['brand']
            clothing_type = form['clothing_type']
            description = form['description']
            quantity = form['quantity']
            unit_price = form['unit_price']
            date_posted = form['date_posted']
            curr_quantity = quantity
            is_supply = False
            address_id = form['address_id']

            if person_id and brand and clothing_type and description and unit_price and quantity and date_posted and \
                    address_id:
                clothing_id = dao.insert(person_id, brand, description, quantity, unit_price, date_posted, curr_quantity,
                                      is_supply, address_id)
                result = self.build_clothing_attributes(clothing_id, person_id, brand, description, quantity, unit_price,
                                                     date_posted, curr_quantity, is_supply, address_id)
                return jsonify(Supply=result), 201
            else:
                return jsonify(Error="Unexpected attributes in post request"), 400

    def insert_clothing_request_json(self, json):
        dao = ClothingDAO()
        person_id = json['person_id']
        brand = json['brand']
        clothing_type = json['clothing_type']
        description = json['description']
        quantity = json['quantity']
        unit_price = json['unit_price']
        date_posted = json['date_posted']
        curr_quantity = quantity
        is_supply = False
        address_id = json['address_id']

        if person_id and brand and clothing_type and description and unit_price and quantity and date_posted and \
                address_id:
            clothing_id = dao.insert(person_id, brand, description, quantity, unit_price, date_posted, curr_quantity,
                                  is_supply, address_id)
            result = self.build_clothing_attributes(clothing_id, person_id, brand, description, quantity, unit_price,
                                                 date_posted, curr_quantity, is_supply, address_id)
            return jsonify(Supply=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request"), 400

    def delete_clothing_post(self, clothing_id):
        dao = ClothingDAO()
        if not dao.getClothingById(clothing_id):
            return jsonify(Error="Post not found."), 404
        else:
            dao.delete(clothing_id)
        return jsonify(DeleteStatus="OK"), 200

    def update_supply(self, clothing_id, form):
        dao = ClothingDAO()
        if not dao.getClothingById(clothing_id):
            return jsonify(Error="Post not found."), 404
        else:
            if len(form) != 9:
                return jsonify(Error="Malformed update request"), 400
            else:
                brand = form['brand']
                clothing_type = form['clothing_type']
                description = form['description']
                unit_price = form['unit_price']
                curr_quantity = form['quantity']
                address_id = form['address_id']

                if int(curr_quantity) < 0:
                    return jsonify(Error="Cannot put negative value"), 400
                if brand and clothing_type and description and unit_price and curr_quantity and address_id:
                    dao.update(clothing_id, brand, clothing_type, description, unit_price, curr_quantity, address_id)
                    row = dao.getClothingById(clothing_id)
                    result = self.build_clothing_dict(row)
                    return jsonify(Part=result), 200
                else:
                    return jsonify(Error="Unexpected attributes in update request"), 400
