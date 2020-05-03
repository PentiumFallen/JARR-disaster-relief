from flask import jsonify
from backend.dao.medication import MedicationDAO


class MedicationHandler:

    def build_medication_dict(self, row):
        result = {}
        result['Medication_id'] = row[0]
        result['person_id'] = row[1]
        result['brand'] = row[2]
        result['description'] = row[3]
        result['quantity'] = row[4]
        result['unit_price'] = row[5]
        result['date_posted'] = row[6]
        result['curr_quantity'] = row[7]
        result['is_supply'] = row[8]
        result['address_id'] = row[9]
        return result

    def build_medication_attributes(self, medication_id, person_id, brand, description, quantity, unit_price,
                                    date_posted, curr_quantity, is_supply, address_id):
        result = {
            'Medication_id': medication_id,
            'person_id': person_id,
            'brand': brand,
            'description': description,
            'quantity': quantity,
            'unit_price': unit_price,
            'date_posted': date_posted,
            'curr_quantity': curr_quantity,
            'is_supply': is_supply,
            'address_id': address_id
        }
        return result

    def build_medication_ingredient_dict(self, row):
        result = {}
        result['ing_id'] = row[0]
        result['medication_id'] = row[1]
        result['ing_name'] = row[2]
        result['usage'] = row[3]
        return result

    def build_medication_ingredient_attributes(self, ing_id, medication_id, ing_name, usage):
        result = {
            'ing_id': ing_id,
            'medication_id': medication_id,
            'ing_name': ing_name,
            'usage': usage
        }
        return result

    def get_all_medication_posts(self):
        dao = MedicationDAO()
        result_list = dao.getAllMedication()
        for row in result_list:
            result = self.build_medication_dict(row)
            result_list.append(result)
        return jsonify(Medication_Posts=result_list)

    def get_all_medication_supplies(self):
        dao = MedicationDAO()
        result_list = dao.getAllMedicationSupplies()
        for row in result_list:
            result = self.build_medication_dict(row)
            result_list.append(result)
        return jsonify(Medication_Supplies=result_list)

    def get_all_medication_requests(self):
        dao = MedicationDAO()
        result_list = dao.getAllMedicationRequests()
        for row in result_list:
            result = self.build_medication_dict(row)
            result_list.append(result)
        return jsonify(Medication_Requests=result_list)

    def get_all_available_medication_supplies(self):
        dao = MedicationDAO()
        result_list = dao.getAllAvailableMedicationSupplies()
        for row in result_list:
            result = self.build_medication_dict(row)
            result_list.append(result)
        return jsonify(Medication_Supplies=result_list)

    def get_all_unfulfilled_medication_requests(self):
        dao = MedicationDAO()
        result_list = dao.getAllUnfulfilledMedicationRequests()
        for row in result_list:
            result = self.build_medication_dict(row)
            result_list.append(result)
        return jsonify(Medication_Requests=result_list)

    def get_medication_post_by_id(self, medication_id):
        dao = MedicationDAO()
        row = dao.getMedicationById(medication_id)
        if not row:
            return jsonify(Error="Post Not Found"), 404
        else:
            result = self.build_medication_dict(row)
        return jsonify(Medication_Post=result)

    def get_medication_posts_by_person_id(self, person_id):
        dao = MedicationDAO()
        result_list = dao.getMedicationByPersonId(person_id)
        for row in result_list:
            result = self.build_medication_dict(row)
            result_list.append(result)
        return jsonify(Medication_Posts=result_list)

    def get_medication_ingredients_by_id(self, medication_id):
        dao = MedicationDAO()
        result_list = dao.getMedicationIngredientsById(medication_id)
        for row in result_list:
            result = self.build_medication_ingredient_dict(row)
            result_list.append(result)
        return jsonify(Medication_Posts=result_list)

    def get_medication_supplies_by_person_id(self, person_id):
        dao = MedicationDAO()
        result_list = dao.getMedicationSuppliesByPersonId(person_id)
        for row in result_list:
            result = self.build_medication_dict(row)
            result_list.append(result)
        return jsonify(Medication_Posts=result_list)

    def get_medication_requests_by_person_id(self, person_id):
        dao = MedicationDAO()
        result_list = dao.getMedicationRequestsByPersonId(person_id)
        for row in result_list:
            result = self.build_medication_dict(row)
            result_list.append(result)
        return jsonify(Medication_Posts=result_list)

    def search_medication_posts(self, args):
        brand = args['brand']
        usage = args['usage']
        dao = MedicationDAO()

        if len(args) == 2 and brand and usage:
            medication_list = dao.getMedicationByBrandAndUsage(brand, usage)
        elif len(args) == 1 and brand:
            medication_list = dao.getMedicationByBrand(brand)
        elif len(args) == 1 and usage:
            medication_list = dao.getMedicationByUsage(usage)
        else:
            return jsonify(Error="Malformed query string"), 400
        result_list = []
        for row in medication_list:
            result = self.build_medication_dict(row)
            result_list.append(result)
        return jsonify(Medication_Posts=result_list)

    def search_medication_supplies(self, args):
        brand = args['brand']
        max_price = args['unit_price']
        usage = args['usage']
        ingredient = args['ing_name']
        dao = MedicationDAO()

        if len(args) == 3 and brand and max_price and usage:
            medication_list = dao.getMedicationSuppliesByBrandAndUsageAndMaxPrice(brand, usage, max_price)
        elif len(args) == 3 and brand and max_price and ingredient:
            medication_list = dao.getMedicationSuppliesByBrandAndIngredientAndMaxPrice(brand, ingredient, max_price)
        elif len(args) == 2 and brand and usage:
            medication_list = dao.getMedicationSuppliesByBrandAndUsage(brand, usage)
        elif len(args) == 2 and brand and ingredient:
            medication_list = dao.getMedicationSuppliesByBrandAndIngredient(brand, ingredient)
        elif len(args) == 1 and brand:
            medication_list = dao.getMedicationSuppliesByBrand(brand)
        elif len(args) == 1 and max_price:
            medication_list = dao.getMedicationSuppliesByMaxPrice(max_price)
        elif len(args) == 1 and usage:
            medication_list = dao.getMedicationSuppliesByUsage(usage)
        elif len(args) == 1 and ingredient:
            medication_list = dao.getMedicationSuppliesByIngredient(ingredient)
        else:
            return jsonify(Error="Malformed query string"), 400
        result_list = []
        for row in medication_list:
            result = self.build_medication_dict(row)
            result_list.append(result)
        return jsonify(Medication_Posts=result_list)

    def search_medication_requests(self, args):
        brand = args['brand']
        usage = args['usage']
        ingredient = args['ing_name']
        dao = MedicationDAO()

        if len(args) == 2 and brand and usage:
            medication_list = dao.getMedicationRequestsByBrandAndUsage(brand, usage)
        elif len(args) == 2 and brand and ingredient:
            medication_list = dao.getMedicationRequestsByBrandAndIngredient(brand, ingredient)
        elif len(args) == 1 and brand:
            medication_list = dao.getMedicationRequestsByBrand(brand)
        elif len(args) == 1 and usage:
            medication_list = dao.getMedicationRequestsByUsage(usage)
        elif len(args) == 1 and ingredient:
            medication_list = dao.getMedicationRequestsByIngredient(ingredient)
        else:
            return jsonify(Error="Malformed query string"), 400
        result_list = []
        for row in medication_list:
            result = self.build_medication_dict(row)
            result_list.append(result)
        return jsonify(Medication_Posts=result_list)

    def insert_medication_supply(self, form):
        if len(form) != 8:
            return jsonify(Error="Malformed post request"), 400
        else:
            dao = MedicationDAO()
            person_id = form['person_id']
            brand = form['brand']
            description = form['description']
            quantity = form['quantity']
            unit_price = form['unit_price']
            date_posted = form['date_posted']
            curr_quantity = quantity
            is_supply = True
            address_id = form['address_id']

            if person_id and brand and description and unit_price and quantity and date_posted and address_id:
                medication_id = dao.insert(person_id, brand, description, quantity, unit_price, date_posted,
                                           curr_quantity, is_supply, address_id)
                result = self.build_medication_attributes(medication_id, person_id, brand, description, quantity,
                                                          unit_price, date_posted, curr_quantity, is_supply, address_id)
                return jsonify(Supply=result), 201
            else:
                return jsonify(Error="Unexpected attributes in post request"), 400

    def insert_medication_supply_json(self, json):
        dao = MedicationDAO()
        person_id = json['person_id']
        brand = json['brand']
        description = json['description']
        quantity = json['quantity']
        unit_price = json['unit_price']
        date_posted = json['date_posted']
        curr_quantity = quantity
        is_supply = True
        address_id = json['address_id']

        if person_id and brand and description and unit_price and quantity and date_posted and address_id:
            medication_id = dao.insert(person_id, brand, description, quantity, unit_price, date_posted, curr_quantity,
                                       is_supply, address_id)
            result = self.build_medication_attributes(medication_id, person_id, brand, description, quantity,
                                                      unit_price,
                                                      date_posted, curr_quantity, is_supply, address_id)
            return jsonify(Supply=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request"), 400

    def insert_medication_request(self, form):
        if len(form) != 8:
            return jsonify(Error="Malformed post request"), 400
        else:
            dao = MedicationDAO()
            person_id = form['person_id']
            brand = form['brand']
            description = form['description']
            quantity = form['quantity']
            unit_price = form['unit_price']
            date_posted = form['date_posted']
            curr_quantity = quantity
            is_supply = False
            address_id = form['address_id']

            if person_id and brand and description and unit_price and quantity and date_posted and address_id:
                medication_id = dao.insert(person_id, brand, description, quantity, unit_price, date_posted,
                                           curr_quantity, is_supply, address_id)
                result = self.build_medication_attributes(medication_id, person_id, brand, description, quantity,
                                                          unit_price, date_posted, curr_quantity, is_supply, address_id)
                return jsonify(Supply=result), 201
            else:
                return jsonify(Error="Unexpected attributes in post request"), 400

    def insert_medication_request_json(self, json):
        dao = MedicationDAO()
        person_id = json['person_id']
        brand = json['brand']
        description = json['description']
        quantity = json['quantity']
        unit_price = json['unit_price']
        date_posted = json['date_posted']
        curr_quantity = quantity
        is_supply = False
        address_id = json['address_id']

        if person_id and brand and description and unit_price and quantity and date_posted and \
                address_id:
            medication_id = dao.insert(person_id, brand, description, quantity, unit_price, date_posted, curr_quantity,
                                       is_supply, address_id)
            result = self.build_medication_attributes(medication_id, person_id, brand, description, quantity,
                                                      unit_price, date_posted, curr_quantity, is_supply, address_id)
            return jsonify(Supply=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request"), 400

    def insert_medication_ingredient(self, medication_id, form):
        if len(form) != 2:
            return jsonify(Error="Malformed post request"), 400
        else:
            dao = MedicationDAO()
            ing_name = form['ing_name']
            usage = form['usage']
            ing_id = dao.insertIngredient(medication_id, ing_name, usage)
            if ing_name and usage:
                result = {
                    'ing_id': ing_id,
                    'medication_id': medication_id,
                    'ing_name': ing_name,
                    'usage': usage
                }
                return jsonify(Supply=result), 201
            else:
                return jsonify(Error="Unexpected attributes in post request"), 400

    def insert_medication_ingredient_json(self, medication_id, json):
        dao = MedicationDAO()
        ing_name = json['ing_name']
        usage = json['usage']
        ing_id = dao.insertIngredient(medication_id, ing_name, usage)
        if ing_name and usage:
            result = {
                'ing_id': ing_id,
                'medication_id': medication_id,
                'ing_name': ing_name,
                'usage': usage
            }
            return jsonify(Supply=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request"), 400

    def delete_medication_post(self, medication_id):
        dao = MedicationDAO()
        if not dao.getMedicationById(medication_id):
            return jsonify(Error="Post not found."), 404
        else:
            dao.delete(medication_id)
        return jsonify(DeleteStatus="OK"), 200

    def delete_medication_ingredient(self, ing_id):
        dao = MedicationDAO()
        if not dao.getMedicationIngredientById(ing_id):
            return jsonify(Error="Post not found."), 404
        else:
            dao.deleteIngredient(ing_id)
        return jsonify(DeleteStatus="OK"), 200

    def update_medication(self, medication_id, form):
        dao = MedicationDAO()
        if not dao.getMedicationById(medication_id):
            return jsonify(Error="Post not found."), 404
        else:
            if len(form) != 9:
                return jsonify(Error="Malformed update request"), 400
            else:
                brand = form['brand']
                description = form['description']
                unit_price = form['unit_price']
                curr_quantity = form['quantity']
                address_id = form['address_id']

                if int(curr_quantity) < 0:
                    return jsonify(Error="Cannot put negative value"), 400
                if brand and description and unit_price and curr_quantity and address_id:
                    dao.update(medication_id, brand, description, unit_price, curr_quantity, address_id)
                    row = dao.getMedicationById(medication_id)
                    result = self.build_medication_dict(row)
                    return jsonify(Part=result), 200
                else:
                    return jsonify(Error="Unexpected attributes in update request"), 400
