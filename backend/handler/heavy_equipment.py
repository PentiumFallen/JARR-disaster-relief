from flask import jsonify
from backend.dao.heavy_equipment import HeavyEquipmentDAO


class HeavyEquipmentHandler:

    def build_heavy_equipment_dict(self, row):
        result = {}
        result['heavy_equipment_id'] = row[0]
        result['person_id'] = row[1]
        result['brand'] = row[2]
        result['description'] = row[3]
        result['quantity'] = row[4]
        result['unit_price'] = row[5]
        result['date_posted'] = row[6]
        result['curr_quantity'] = row[7]
        result['is_supply'] = row[8]
        result['equipment_name'] = row[9]
        result['address_id'] = row[10]
        return result

    def build_heavy_equipment_attributes(self, heavy_equipment_id, person_id, brand, equipment_name, description, quantity, unit_price, date_posted,
                               curr_quantity, is_supply, address_id):
        result = {
            'heavy_equipment_id': heavy_equipment_id,
            'person_id': person_id,
            'brand': brand,
            'description': description,
            'quantity': quantity,
            'unit_price': unit_price,
            'date_posted': date_posted,
            'curr_quantity': curr_quantity,
            'is_supply': is_supply,
            'equipment_name': equipment_name,
            'address_id': address_id,
        }
        return result

    def get_all_heavy_equipment_posts(self):
        dao = HeavyEquipmentDAO()
        result_list = dao.getAllHeavyEquipment()
        for row in result_list:
            result = self.build_heavy_equipment_dict(row)
            result_list.append(result)
        return jsonify(Heavy_Equipment_Posts=result_list)

    def get_all_heavy_equipment_supplies(self):
        dao = HeavyEquipmentDAO()
        result_list = dao.getAllHeavyEquipmentSupplies()
        for row in result_list:
            result = self.build_heavy_equipment_dict(row)
            result_list.append(result)
        return jsonify(Heavy_Equipment_Supplies=result_list)

    def get_all_heavy_equipment_requests(self):
        dao = HeavyEquipmentDAO()
        result_list = dao.getAllHeavyEquipmentRequests()
        for row in result_list:
            result = self.build_heavy_equipment_dict(row)
            result_list.append(result)
        return jsonify(Heavy_Equipment_Requests=result_list)

    def get_all_available_heavy_equipment_supplies(self):
        dao = HeavyEquipmentDAO()
        result_list = dao.getAllAvailableHeavyEquipmentSupplies()
        for row in result_list:
            result = self.build_heavy_equipment_dict(row)
            result_list.append(result)
        return jsonify(Heavy_Equipment_Supplies=result_list)

    def get_all_unfulfilled_heavy_equipment_requests(self):
        dao = HeavyEquipmentDAO()
        result_list = dao.getAllUnfulfilledHeavyEquipmentRequests()
        for row in result_list:
            result = self.build_heavy_equipment_dict(row)
            result_list.append(result)
        return jsonify(Heavy_Equipment_Requests=result_list)

    def get_heavy_equipment_post_by_id(self, heavy_equipment_id):
        dao = HeavyEquipmentDAO()
        row = dao.getHeavyEquipmentById(heavy_equipment_id)
        if not row:
            return jsonify(Error="Post Not Found"), 404
        else:
            result = self.build_heavy_equipment_dict(row)
        return jsonify(Heavy_Equipment_Post=result)

    def get_heavy_equipment_posts_by_person_id(self, person_id):
        dao = HeavyEquipmentDAO()
        result_list = dao.getHeavyEquipmentByPersonId(person_id)
        for row in result_list:
            result = self.build_heavy_equipment_dict(row)
            result_list.append(result)
        return jsonify(Heavy_Equipment_Posts=result_list)

    def get_heavy_equipment_supplies_by_person_id(self, person_id):
        dao = HeavyEquipmentDAO()
        result_list = dao.getHeavyEquipmentSuppliesByPersonId(person_id)
        for row in result_list:
            result = self.build_heavy_equipment_dict(row)
            result_list.append(result)
        return jsonify(Heavy_Equipment_Posts=result_list)

    def get_heavy_equipment_requests_by_person_id(self, person_id):
        dao = HeavyEquipmentDAO()
        result_list = dao.getHeavyEquipmentRequestsByPersonId(person_id)
        for row in result_list:
            result = self.build_heavy_equipment_dict(row)
            result_list.append(result)
        return jsonify(Heavy_Equipment_Posts=result_list)

    def search_heavy_equipment_posts(self, args):
        brand = args['brand']
        equipment_name = args['equipment_name']
        dao = HeavyEquipmentDAO()

        if len(args) == 2 and brand and equipment_name:
            heavy_equipment_list = dao.getHeavyEquipmentByBrandAndName(brand, equipment_name)
        elif len(args) == 1 and brand:
            heavy_equipment_list = dao.getHeavyEquipmenttByBrand(brand)
        elif len(args) == 1 and equipment_name:
            heavy_equipment_list = dao.getHeavyEquipmentByName(equipment_name)
        else:
            return jsonify(Error="Malformed query string"), 400
        result_list = []
        for row in heavy_equipment_list:
            result = self.build_heavy_equipment_dict(row)
            result_list.append(result)
        return jsonify(Heavy_Equipment_Posts=result_list)

    def search_heavy_equipment_supplies(self, args):
        brand = args['brand']
        max_price = args['unit_price']
        equipment_name = args['equipment_name']
        dao = HeavyEquipmentDAO()

        if len(args) == 3 and brand and max_price and equipment_name:
            heavy_equipment_list = dao.getHeavyEquipmentSuppliesByBrandAndNameAndMaxPrice(brand, equipment_name, max_price)
        elif len(args) == 2 and brand and equipment_name:
            heavy_equipment_list = dao.getHeavyEquipmentSuppliesByBrandAndName(brand, equipment_name)
        elif len(args) == 1 and brand:
            heavy_equipment_list = dao.getHeavyEquipmentSuppliesByBrand(brand)
        elif len(args) == 1 and max_price:
            heavy_equipment_list = dao.getHeavyEquipmentSuppliesByMaxPrice(max_price)
        elif len(args) == 1 and equipment_name:
            heavy_equipment_list = dao.getHeavyEquipmentSuppliesByName(equipment_name)
        else:
            return jsonify(Error="Malformed query string"), 400
        result_list = []
        for row in heavy_equipment_list:
            result = self.build_heavy_equipment_dict(row)
            result_list.append(result)
        return jsonify(Heavy_Equipment_Posts=result_list)

    def search_heavy_equipment_requests(self, args):
        brand = args['brand']
        equipment_name = args['equipment_name']
        dao = HeavyEquipmentDAO()

        if len(args) == 2 and brand and equipment_name:
            heavy_equipment_list = dao.HeavyEquipmentRequestsByBrandAndName(brand, equipment_name)
        elif len(args) == 1 and brand:
            heavy_equipment_list = dao.HeavyEquipmentRequestsByBrand(brand)
        elif len(args) == 1 and equipment_name:
            heavy_equipment_list = dao.HeavyEquipmentRequestsByName(equipment_name)
        else:
            return jsonify(Error="Malformed query string"), 400
        result_list = []
        for row in heavy_equipment_list:
            result = self.build_heavy_equipment_dict(row)
            result_list.append(result)
        return jsonify(Heavy_Equipment_Posts=result_list)

    def insert_heavy_equipment_supply(self, form):
        if len(form) != 8:
            return jsonify(Error="Malformed post request"), 400
        else:
            dao = HeavyEquipmentDAO()
            person_id = form['person_id']
            brand = form['brand']
            equipment_name = form['equipment_name']
            description = form['description']
            quantity = form['quantity']
            unit_price = form['unit_price']
            date_posted = form['date_posted']
            curr_quantity = quantity
            is_supply = True
            address_id = form['address_id']

            if person_id and brand and equipment_name and description and unit_price and quantity and date_posted and \
                    address_id:
                heavy_equipment_id = dao.insert(person_id, brand, description, quantity, unit_price, date_posted, curr_quantity,
                                      is_supply, address_id)
                result = self.build_heavy_equipment_attributes(heavy_equipment_id, person_id, brand, equipment_name, description, quantity, unit_price,
                                                     date_posted, curr_quantity, is_supply, address_id)
                return jsonify(Supply=result), 201
            else:
                return jsonify(Error="Unexpected attributes in post request"), 400

    def insert_heavy_equipment_supply_json(self, json):
        dao = HeavyEquipmentDAO()
        person_id = json['person_id']
        brand = json['brand']
        equipment_name = json['equipment_name']
        description = json['description']
        quantity = json['quantity']
        unit_price = json['unit_price']
        date_posted = json['date_posted']
        curr_quantity = quantity
        is_supply = True
        address_id = json['address_id']

        if person_id and brand and equipment_name and description and unit_price and quantity and date_posted and \
                address_id:
            heavy_equipment_id = dao.insert(person_id, brand, description, quantity, unit_price, date_posted, curr_quantity,
                                  is_supply, address_id)
            result = self.build_heavy_equipment_attributes(heavy_equipment_id, person_id, brand, description, quantity, unit_price,
                                                 date_posted, curr_quantity, is_supply, address_id)
            return jsonify(Supply=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request"), 400

    def insert_heavy_equipment_request(self, form):
        if len(form) != 8:
            return jsonify(Error="Malformed post request"), 400
        else:
            dao = HeavyEquipmentDAO()
            person_id = form['person_id']
            brand = form['brand']
            equipment_name = form['equipment_name']
            description = form['description']
            quantity = form['quantity']
            unit_price = form['unit_price']
            date_posted = form['date_posted']
            curr_quantity = quantity
            is_supply = False
            address_id = form['address_id']

            if person_id and brand and equipment_name and description and unit_price and quantity and date_posted and \
                    address_id:
                heavy_equipment_id = dao.insert(person_id, brand, description, quantity, unit_price, date_posted, curr_quantity,
                                      is_supply, address_id)
                result = self.build_heavy_equipment_attributes(heavy_equipment_id, person_id, brand, description, quantity, unit_price,
                                                     date_posted, curr_quantity, is_supply, address_id)
                return jsonify(Supply=result), 201
            else:
                return jsonify(Error="Unexpected attributes in post request"), 400

    def insert_heavy_equipment_request_json(self, json):
        dao = HeavyEquipmentDAO()
        person_id = json['person_id']
        brand = json['brand']
        equipment_name = json['equipment_name']
        description = json['description']
        quantity = json['quantity']
        unit_price = json['unit_price']
        date_posted = json['date_posted']
        curr_quantity = quantity
        is_supply = False
        address_id = json['address_id']

        if person_id and brand and equipment_name and description and unit_price and quantity and date_posted and \
                address_id:
            heavy_equipment_id = dao.insert(person_id, brand, description, quantity, unit_price, date_posted, curr_quantity,
                                  is_supply, address_id)
            result = self.build_heavy_equipment_attributes(heavy_equipment_id, person_id, brand, description, quantity, unit_price,
                                                 date_posted, curr_quantity, is_supply, address_id)
            return jsonify(Supply=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request"), 400

    def delete_heavy_equipment_post(self, heavy_equipment_id):
        dao = HeavyEquipmentDAO()
        if not dao.getHeavyEquipmentById(heavy_equipment_id):
            return jsonify(Error="Post not found."), 404
        else:
            dao.delete(heavy_equipment_id)
        return jsonify(DeleteStatus="OK"), 200

    def update_supply(self, heavy_equipment_id, form):
        dao = HeavyEquipmentDAO()
        if not dao.getHeavyEquipmentById(heavy_equipment_id):
            return jsonify(Error="Post not found."), 404
        else:
            if len(form) != 9:
                return jsonify(Error="Malformed update request"), 400
            else:
                brand = form['brand']
                equipment_name = form['equipment_name']
                description = form['description']
                unit_price = form['unit_price']
                curr_quantity = form['quantity']
                address_id = form['address_id']

                if int(curr_quantity) < 0:
                    return jsonify(Error="Cannot put negative value"), 400
                if brand and equipment_name and description and unit_price and curr_quantity and address_id:
                    dao.update(heavy_equipment_id, brand, equipment_name, description, unit_price, curr_quantity, address_id)
                    row = dao.getHeavyEquipmenttById(heavy_equipment_id)
                    result = self.build_heavy_equipment_dict(row)
                    return jsonify(Part=result), 200
                else:
                    return jsonify(Error="Unexpected attributes in update request"), 400
