from flask import jsonify
from backend.dao.medical_device import MedicalDeviceDAO


class MedicalDeviceHandler:

    def build_medical_device_dict(self, row):
        result = {}
        result['medical_dev_id'] = row[0]
        result['person_id'] = row[1]
        result['brand'] = row[2]
        result['description'] = row[3]
        result['quantity'] = row[4]
        result['unit_price'] = row[5]
        result['date_posted'] = row[6]
        result['curr_quantity'] = row[7]
        result['usage'] = row[8]
        result['is_supply'] = row[9]
        result['address_id'] = row[10]
        return result

    def build_medical_device_attributes(self, medical_dev_id, person_id, brand, description, quantity, unit_price,
                                    date_posted, curr_quantity, usage, is_supply, address_id):
        result = {
            'medical_dev_id': medical_dev_id,
            'person_id': person_id,
            'brand': brand,
            'description': description,
            'quantity': quantity,
            'unit_price': unit_price,
            'date_posted': date_posted,
            'curr_quantity': curr_quantity,
            'usage': usage,
            'is_supply': is_supply,
            'address_id': address_id
        }
        return result

    def get_all_medical_device_posts(self):
        dao = MedicalDeviceDAO()
        result_list = dao.getAllMedicalDevice()
        for row in result_list:
            result = self.build_medical_device_dict(row)
            result_list.append(result)
        return jsonify(Medical_Device_Posts=result_list)

    def get_all_medical_device_supplies(self):
        dao = MedicalDeviceDAO()
        result_list = dao.getAllMedicalDeviceSupplies()
        for row in result_list:
            result = self.build_medical_device_dict(row)
            result_list.append(result)
        return jsonify(Medical_Device_Supplies=result_list)

    def get_all_medical_device_requests(self):
        dao = MedicalDeviceDAO()
        result_list = dao.getAllMedicalDeviceRequests()
        for row in result_list:
            result = self.build_medical_device_dict(row)
            result_list.append(result)
        return jsonify(Medical_Device_Requests=result_list)

    def get_all_available_medical_device_supplies(self):
        dao = MedicalDeviceDAO()
        result_list = dao.getAllAvailableMedicalDeviceSupplies()
        for row in result_list:
            result = self.build_medical_device_dict(row)
            result_list.append(result)
        return jsonify(Medical_Device_Supplies=result_list)

    def get_all_unfulfilled_medical_device_requests(self):
        dao = MedicalDeviceDAO()
        result_list = dao.getAllUnfulfilledMedicalDeviceRequests()
        for row in result_list:
            result = self.build_medical_device_dict(row)
            result_list.append(result)
        return jsonify(Medical_Device_Requests=result_list)

    def get_medical_device_post_by_id(self, medical_dev_id):
        dao = MedicalDeviceDAO()
        row = dao.getMedicalDeviceById(medical_dev_id)
        if not row:
            return jsonify(Error="Post Not Found"), 404
        else:
            result = self.build_medical_device_dict(row)
        return jsonify(Medical_Device_Post=result)

    def get_medical_device_posts_by_person_id(self, person_id):
        dao = MedicalDeviceDAO()
        result_list = dao.getMedicalDeviceByPersonId(person_id)
        for row in result_list:
            result = self.build_medical_device_dict(row)
            result_list.append(result)
        return jsonify(Medical_Device_Posts=result_list)

    def get_medical_device_supplies_by_person_id(self, person_id):
        dao = MedicalDeviceDAO()
        result_list = dao.getMedicalDeviceSuppliesByPersonId(person_id)
        for row in result_list:
            result = self.build_medical_device_dict(row)
            result_list.append(result)
        return jsonify(Medical_Device_Posts=result_list)

    def get_medical_device_requests_by_person_id(self, person_id):
        dao = MedicalDeviceDAO()
        result_list = dao.getMedicalDeviceRequestsByPersonId(person_id)
        for row in result_list:
            result = self.build_medical_device_dict(row)
            result_list.append(result)
        return jsonify(Medical_Device_Posts=result_list)

    def search_medical_device_posts(self, args):
        brand = args['brand']
        usage = args['usage']
        dao = MedicalDeviceDAO()

        if len(args) == 2 and brand and usage:
            medical_device_list = dao.getMedicalDeviceByBrandAndUsage(brand, usage)
        elif len(args) == 1 and brand:
            medical_device_list = dao.getMedicalDeviceByBrand(brand)
        elif len(args) == 1 and usage:
            medical_device_list = dao.getMedicalDeviceByUsage(usage)
        else:
            return jsonify(Error="Malformed query string"), 400
        result_list = []
        for row in medical_device_list:
            result = self.build_medical_device_dict(row)
            result_list.append(result)
        return jsonify(Medical_Device_Posts=result_list)

    def search_medical_device_supplies(self, args):
        brand = args['brand']
        max_price = args['unit_price']
        usage = args['usage']
        dao = MedicalDeviceDAO()

        if len(args) == 3 and brand and max_price and usage:
            medical_device_list = dao.getMedicalDeviceSuppliesByBrandAndUsageAndMaxPrice(brand, usage, max_price)
        elif len(args) == 2 and brand and usage:
            medical_device_list = dao.getMedicalDeviceSuppliesByBrandAndUsage(brand, usage)
        elif len(args) == 1 and brand:
            medical_device_list = dao.getMedicalDeviceSuppliesByBrand(brand)
        elif len(args) == 1 and max_price:
            medical_device_list = dao.getMedicalDeviceSuppliesByMaxPrice(max_price)
        elif len(args) == 1 and usage:
            medical_device_list = dao.getMedicalDeviceSuppliesByUsage(usage)
        else:
            return jsonify(Error="Malformed query string"), 400
        result_list = []
        for row in medical_device_list:
            result = self.build_medical_device_dict(row)
            result_list.append(result)
        return jsonify(Medical_Device_Posts=result_list)

    def search_medical_device_requests(self, args):
        brand = args['brand']
        usage = args['usage']
        dao = MedicalDeviceDAO()

        if len(args) == 2 and brand and usage:
            medical_device_list = dao.getMedicalDeviceRequestsByBrandAndUsage(brand, usage)
        elif len(args) == 1 and brand:
            medical_device_list = dao.getMedicalDeviceRequestsByBrand(brand)
        elif len(args) == 1 and usage:
            medical_device_list = dao.getMedicalDeviceRequestsByUsage(usage)
        else:
            return jsonify(Error="Malformed query string"), 400
        result_list = []
        for row in medical_device_list:
            result = self.build_medical_device_dict(row)
            result_list.append(result)
        return jsonify(medical_device_Posts=result_list)

    def insert_medical_device_supply(self, form):
        if len(form) != 8:
            return jsonify(Error="Malformed post request"), 400
        else:
            dao = MedicalDeviceDAO()
            person_id = form['person_id']
            brand = form['brand']
            description = form['description']
            quantity = form['quantity']
            unit_price = form['unit_price']
            date_posted = form['date_posted']
            curr_quantity = quantity
            usage = form['usage']
            is_supply = True
            address_id = form['address_id']

            if person_id and brand and description and unit_price and quantity and date_posted and address_id and usage:
                medical_dev_id = dao.insert(person_id, brand, description, quantity, unit_price, date_posted,
                                           curr_quantity, usage, is_supply, address_id)
                result = self.build_medical_device_attributes(medical_dev_id, person_id, brand, description, quantity,
                                                          unit_price, date_posted, curr_quantity, usage, is_supply, address_id)
                return jsonify(Supply=result), 201
            else:
                return jsonify(Error="Unexpected attributes in post request"), 400

    def insert_medical_device_supply_json(self, json):
        dao = MedicalDeviceDAO()
        person_id = json['person_id']
        brand = json['brand']
        description = json['description']
        quantity = json['quantity']
        unit_price = json['unit_price']
        date_posted = json['date_posted']
        curr_quantity = quantity
        usage = json['usage']
        is_supply = True
        address_id = json['address_id']

        if person_id and brand and description and unit_price and quantity and date_posted and address_id and usage:
            medical_dev_id = dao.insert(person_id, brand, description, quantity, unit_price, date_posted, curr_quantity, usage,
                                       is_supply, address_id)
            result = self.build_medical_device_attributes(medical_dev_id, person_id, brand, description, quantity,
                                                      unit_price,
                                                      date_posted, curr_quantity, usage, is_supply, address_id)
            return jsonify(Supply=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request"), 400

    def insert_medical_device_request(self, form):
        if len(form) != 8:
            return jsonify(Error="Malformed post request"), 400
        else:
            dao = MedicalDeviceDAO()
            person_id = form['person_id']
            brand = form['brand']
            description = form['description']
            quantity = form['quantity']
            unit_price = form['unit_price']
            date_posted = form['date_posted']
            curr_quantity = quantity
            usage = form['usage']
            is_supply = False
            address_id = form['address_id']

            if person_id and brand and description and unit_price and quantity and date_posted and address_id and usage:
                medical_dev_id = dao.insert(person_id, brand, description, quantity, unit_price, date_posted,
                                           curr_quantity, usage, is_supply, address_id)
                result = self.build_medical_device_attributes(medical_dev_id, person_id, brand, description, quantity,
                                                          unit_price, date_posted, curr_quantity, usage, is_supply, address_id)
                return jsonify(Supply=result), 201
            else:
                return jsonify(Error="Unexpected attributes in post request"), 400

    def insert_medical_device_request_json(self, json):
        dao = MedicalDeviceDAO()
        person_id = json['person_id']
        brand = json['brand']
        description = json['description']
        quantity = json['quantity']
        unit_price = json['unit_price']
        date_posted = json['date_posted']
        curr_quantity = quantity
        usage = json['usage']
        is_supply = False
        address_id = json['address_id']

        if person_id and brand and description and unit_price and quantity and date_posted and usage and \
                address_id:
            medical_dev_id = dao.insert(person_id, brand, description, quantity, unit_price, date_posted, curr_quantity,
                                       usage, is_supply, address_id)
            result = self.build_medical_device_attributes(medical_dev_id, person_id, brand, description, quantity,
                                                      unit_price, date_posted, curr_quantity, usage, is_supply, address_id)
            return jsonify(Supply=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request"), 400

    def delete_medical_device_post(self, medical_dev_id):
        dao = MedicalDeviceDAO()
        if not dao.getMedicalDeviceById(medical_dev_id):
            return jsonify(Error="Post not found."), 404
        else:
            dao.delete(medical_dev_id)
        return jsonify(DeleteStatus="OK"), 200


    def update_medical_device(self, medical_dev_id, form):
        dao = MedicalDeviceDAO()
        if not dao.getMedicalDeviceById(medical_dev_id):
            return jsonify(Error="Post not found."), 404
        else:
            if len(form) != 9:
                return jsonify(Error="Malformed update request"), 400
            else:
                brand = form['brand']
                description = form['description']
                unit_price = form['unit_price']
                curr_quantity = form['quantity']
                usage = form['usage']
                address_id = form['address_id']

                if int(curr_quantity) < 0:
                    return jsonify(Error="Cannot put negative value"), 400
                if brand and description and unit_price and curr_quantity and address_id and usage:
                    dao.update(medical_dev_id, brand, description, unit_price, curr_quantity, usage, address_id)
                    row = dao.getMedicalDeviceById(medical_dev_id)
                    result = self.build_medical_device_dict(row)
                    return jsonify(Part=result), 200
                else:
                    return jsonify(Error="Unexpected attributes in update request"), 400