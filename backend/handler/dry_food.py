from flask import jsonify
from backend.dao.dry_food import DryFoodDAO


class DryFoodHandler:

    def build_df_dict(self, row):
        result = {}
        result['df_id'] = row[0]
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

    def build_df_attributes(self, df_id, person_id, brand, food_type, description, quantity, unit_price, date_posted,
                            curr_quantity, is_supply, address_id):
        result = {
            'df_id': df_id,
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

    def get_all_df_posts(self):
        dao = DryFoodDAO()
        result_list = dao.getAllDryFood()
        for row in result_list:
            result = self.build_df_dict(row)
            result_list.append(result)
        return jsonify(Dry_Food_Posts=result_list)

    def get_all_df_supplies(self):
        dao = DryFoodDAO()
        result_list = dao.getAllDryFoodSupplies()
        for row in result_list:
            result = self.build_df_dict(row)
            result_list.append(result)
        return jsonify(Dry_Food_Supplies=result_list)

    def get_all_df_requests(self):
        dao = DryFoodDAO()
        result_list = dao.getAllDryFoodRequests()
        for row in result_list:
            result = self.build_df_dict(row)
            result_list.append(result)
        return jsonify(Dry_Food_Requests=result_list)

    def get_all_available_df_supplies(self):
        dao = DryFoodDAO()
        result_list = dao.getAllAvailableDryFoodSupplies()
        for row in result_list:
            result = self.build_df_dict(row)
            result_list.append(result)
        return jsonify(Dry_Food_Supplies=result_list)

    def get_all_unfulfilled_df_requests(self):
        dao = DryFoodDAO()
        result_list = dao.getAllUnfulfilledDryFoodRequests()
        for row in result_list:
            result = self.build_df_dict(row)
            result_list.append(result)
        return jsonify(Dry_Food_Requests=result_list)

    def get_df_post_by_id(self, df_id):
        dao = DryFoodDAO()
        row = dao.getDryFoodById(df_id)
        if not row:
            return jsonify(Error="Post Not Found"), 404
        else:
            result = self.build_df_dict(row)
        return jsonify(Dry_Food_Post=result)

    def get_df_posts_by_person_id(self, person_id):
        dao = DryFoodDAO()
        result_list = dao.getDryFoodByPersonId(person_id)
        for row in result_list:
            result = self.build_df_dict(row)
            result_list.append(result)
        return jsonify(Dry_Food_Posts=result_list)

    def get_df_supplies_by_person_id(self, person_id):
        dao = DryFoodDAO()
        result_list = dao.getDryFoodSuppliesByPersonId(person_id)
        for row in result_list:
            result = self.build_df_dict(row)
            result_list.append(result)
        return jsonify(Dry_Food_Posts=result_list)

    def get_df_requests_by_person_id(self, person_id):
        dao = DryFoodDAO()
        result_list = dao.getDryFoodRequestsByPersonId(person_id)
        for row in result_list:
            result = self.build_df_dict(row)
            result_list.append(result)
        return jsonify(Dry_Food_Posts=result_list)

    def search_df_posts(self, args):
        brand = args['brand']
        food_type = args['food_type']
        dao = DryFoodDAO()

        if len(args) == 2 and brand and food_type:
            df_list = dao.getDryFoodByBrandAndFoodType(brand, food_type)
        elif len(args) == 1 and brand:
            df_list = dao.getDryFoodByBrand(brand)
        elif len(args) == 1 and food_type:
            df_list = dao.getDryFoodByFoodType(food_type)
        else:
            return jsonify(Error="Malformed query string"), 400
        result_list = []
        for row in df_list:
            result = self.build_df_dict(row)
            result_list.append(result)
        return jsonify(Dry_Food_Posts=result_list)

    def search_df_supplies(self, args):
        brand = args['brand']
        max_price = args['unit_price']
        food_type = args['food_type']
        dao = DryFoodDAO()

        if len(args) == 3 and brand and max_price and food_type:
            df_list = dao.getDryFoodSuppliesByBrandAndFoodTypeAndMaxPrice(brand, food_type, max_price)
        elif len(args) == 2 and brand and food_type:
            df_list = dao.getDryFoodSuppliesByBrandAndFoodType(brand, food_type)
        elif len(args) == 1 and brand:
            df_list = dao.getDryFoodSuppliesByBrand(brand)
        elif len(args) == 1 and max_price:
            df_list = dao.getDryFoodSuppliesByMaxPrice(max_price)
        elif len(args) == 1 and food_type:
            df_list = dao.getDryFoodSuppliesByFoodType(food_type)
        else:
            return jsonify(Error="Malformed query string"), 400
        result_list = []
        for row in df_list:
            result = self.build_df_dict(row)
            result_list.append(result)
        return jsonify(Dry_Food_Posts=result_list)

    def search_df_requests(self, args):
        brand = args['brand']
        food_type = args['food_type']
        dao = DryFoodDAO()

        if len(args) == 2 and brand and food_type:
            df_list = dao.getDryFoodRequestsByBrandAndFoodType(brand, food_type)
        elif len(args) == 1 and brand:
            df_list = dao.getDryFoodRequestsByBrand(brand)
        elif len(args) == 1 and food_type:
            df_list = dao.getDryFoodRequestsByFoodType(food_type)
        else:
            return jsonify(Error="Malformed query string"), 400
        result_list = []
        for row in df_list:
            result = self.build_df_dict(row)
            result_list.append(result)
        return jsonify(Dry_Food_Posts=result_list)

    def insert_df_supply(self, form):
        if len(form) != 8:
            return jsonify(Error="Malformed post request"), 400
        else:
            dao = DryFoodDAO()
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
                df_id = dao.insert(person_id, brand, food_type, description, quantity, unit_price, date_posted,
                                   curr_quantity, is_supply, address_id)
                result = self.build_df_attributes(df_id, person_id, brand, food_type, description, quantity, unit_price,
                                                  date_posted, curr_quantity, is_supply, address_id)
                return jsonify(Dry_Food=result), 201
            else:
                return jsonify(Error="Unexpected attributes in post request"), 400

    def insert_df_supply_json(self, json):
        dao = DryFoodDAO()
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
            df_id = dao.insert(person_id, brand, food_type, description, quantity, unit_price, date_posted,
                               curr_quantity, is_supply, address_id)
            result = self.build_df_attributes(df_id, person_id, brand, food_type, description, quantity, unit_price,
                                              date_posted, curr_quantity, is_supply, address_id)
            return jsonify(Dry_Food=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request"), 400

    def insert_df_request(self, form):
        if len(form) != 8:
            return jsonify(Error="Malformed post request"), 400
        else:
            dao = DryFoodDAO()
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
                df_id = dao.insert(person_id, brand, food_type, description, quantity, unit_price, date_posted,
                                   curr_quantity, is_supply, address_id)
                result = self.build_df_attributes(df_id, person_id, brand, food_type, description, quantity, unit_price,
                                                  date_posted, curr_quantity, is_supply, address_id)
                return jsonify(Dry_Food=result), 201
            else:
                return jsonify(Error="Unexpected attributes in post request"), 400

    def insert_df_request_json(self, json):
        dao = DryFoodDAO()
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
            df_id = dao.insert(person_id, brand, food_type, description, quantity, unit_price, date_posted,
                               curr_quantity, is_supply, address_id)
            result = self.build_df_attributes(df_id, person_id, brand, food_type, description, quantity, unit_price,
                                              date_posted, curr_quantity, is_supply, address_id)
            return jsonify(Dry_Food=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request"), 400

    def delete_df_post(self, df_id):
        dao = DryFoodDAO()
        if not dao.getDryFoodById(df_id):
            return jsonify(Error="Post not found."), 404
        else:
            dao.delete(df_id)
        return jsonify(DeleteStatus="OK"), 200

    def update_df_post(self, df_id, form):
        dao = DryFoodDAO()
        if not dao.getDryFoodById(df_id):
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
                    dao.update(df_id, brand, food_type, description, unit_price, curr_quantity, address_id)
                    row = dao.getDryFoodById(df_id)
                    result = self.build_df_dict(row)
                    return jsonify(Part=result), 200
                else:
                    return jsonify(Error="Unexpected attributes in update request"), 400
