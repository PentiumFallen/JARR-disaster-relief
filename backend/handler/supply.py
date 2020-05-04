from flask import jsonify
from backend.dao.supply import SupplyDAO
#from backend.dao.resource import ResourceDAO


class SupplyHandler:

    # Joined to resource
    def build_supply_dict(self, row):
        #ToDo: Check what Python does with null values in columns!
        print(row)
        if not row[3]:
            result = {
                'supply_id': row[0],
                'resource_id': row[1],
                'category': row[2],
                'person_id': row[4],
                'name': row[5],
                'quantity': row[6],
                'brand': row[7],
                'sdescription': row[8],
                'available': row[9],
                'sunit_price': row[10],
                'date_offered': row[11],
                'address_id': row[12]
            }
        else:
            result = {
                'supply_id': row[0],
                'resource_id': row[1],
                'category': row[2],
                'subcategory': row[3],
                'person_id': row[4],
                'name': row[5],
                'quantity': row[6],
                'brand': row[7],
                'sdescription': row[8],
                'available': row[9],
                'sunit_price': row[10],
                'date_offered': row[11],
                'address_id': row[12]
            }
            return result

    def build_supply_attributes(self, supply_id, resource_id, category_id, person_id, name, quantity, brand,
                                description, available, sunit_price, address_id):
        result = {
            'supply_id': supply_id,
            'resource_id': resource_id,
            'category_id': category_id,
            'person_id': person_id,
            'name': name,
            'quantity': quantity,
            'brand': brand,
            'sdescription': description,
            'available': available,
            'sunit_price': sunit_price,
            'address_id': address_id
        }
        return result

    def build_supply_count(self, row):
        result = {
            'category': row[0],
            'amount': row[1]
        }
        return result

    def get_all_supplies(self):
        dao = SupplyDAO()
        supply_list = dao.getAllSupplies()
        result_list = []
        for row in supply_list:
            result = self.build_supply_dict(row)
            result_list.append(result)
        return jsonify(Supplies=result_list)

    def get_all_available_supplies(self):
        dao = SupplyDAO()
        supply_list = dao.getAllAvailableSupplies()
        result_list = []
        for row in supply_list:
            result = self.build_supply_dict(row)
            result_list.append(result)
        return jsonify(Available_Supplies=result_list)

    def get_total_supplies(self):
        dao = SupplyDAO()
        amount = dao.getTotalSupplies()
        return jsonify(Total_Supplies=amount)

    def get_total_available_supplies(self):
        dao = SupplyDAO()
        amount = dao.getTotalAvailableSupplies()
        return jsonify(Total_Available_Supplies=amount)

    def get_total_supplies_per_category(self):
        dao = SupplyDAO()
        count_list = dao.getTotalSuppliesPerCategory()
        result_list = []
        for row in count_list:
            result = self.build_supply_count(row)
            result_list.append(result)
        return jsonify(Supply_Count=result_list)

    def get_total_available_supplies_per_category(self):
        dao = SupplyDAO()
        count_list = dao.getTotalAvailableSuppliesPerCategory()
        result_list = []
        for row in count_list:
            result = self.build_supply_count(row)
            result_list.append(result)
        return jsonify(Available_Supply_Count=result_list)

    def get_supply_by_id(self, supply_id):
        dao = SupplyDAO()
        row = dao.getSupplyById(supply_id)
        if not row:
            return jsonify(Error="Post Not Found"), 404
        else:
            result = self.build_supply_dict(row)
        return jsonify(Supply_Post=result)

    def get_supplies_by_person_id(self, person_id):
        dao = SupplyDAO()
        supply_list = dao.getSuppliesByPersonId(person_id)
        result_list = []
        for row in supply_list:
            result = self.build_supply_dict(row)
            result_list.append(result)
        return jsonify(Supply_Posts=result_list)

    def search_supplies(self, args):
        brand = args['brand']
        max_price = args['max_price']
        category = args['category']
        subcategory = args['subcategory']
        dao = SupplyDAO()

        if len(args) == 4 and brand and max_price and category and subcategory:
            supply_list = dao.getSuppliesByBrandAndCategoryAndSubcategoryAndMaxPrice(brand, category,subcategory, max_price)
        elif len(args) == 3 and brand and max_price and category:
            supply_list = dao.getSuppliesByBrandAndCategoryAndMaxPrice(brand, category, max_price)
        elif len(args) == 3 and brand and subcategory and category:
            supply_list = dao.getSuppliesByBrandAndCategoryAndSubcategory(brand, category, subcategory)
        elif len(args) == 2 and brand and category:
            supply_list = dao.getSuppliesByBrandAndCategory(brand, category)
        elif len(args) == 1 and brand:
            supply_list = dao.getSuppliesByBrand(brand)
        elif len(args) == 1 and max_price:
            supply_list = dao.getSuppliesByMaxPrice(max_price)
        elif len(args) == 1 and category:
            supply_list = dao.getSuppliesByCategory(category)
        else:
            return jsonify(Error="Malformed query string"), 400
        result_list = []
        for row in supply_list:
            result = self.build_supply_dict(row)
            result_list.append(result)
        return jsonify(Supply_Posts=result_list)

    def search_available_supplies(self, args):
        brand = args['brand']
        max_price = args['unit_price']
        category = args['category']
        subcategory = args['subcategory']
        dao = SupplyDAO()

        if len(args) == 4 and brand and max_price and category and subcategory:
            supply_list = dao.getAvailableSuppliesByBrandAndCategoryAndSubcategoryAndMaxPrice(brand, category,subcategory, max_price)
        elif len(args) == 3 and brand and max_price and category:
            supply_list = dao.getAvailableSuppliesByBrandAndCategoryAndMaxPrice(brand, category, max_price)
        elif len(args) == 3 and brand and subcategory and category:
            supply_list = dao.getAvailableSuppliesByBrandAndCategoryAndSubcategory(brand, category, subcategory)
        elif len(args) == 2 and brand and category:
            supply_list = dao.getAvailableSuppliesByBrandAndCategory(brand, category)
        elif len(args) == 1 and brand:
            supply_list = dao.getAvailableSuppliesByBrand(brand)
        elif len(args) == 1 and max_price:
            supply_list = dao.getAvailableSuppliesByMaxPrice(max_price)
        elif len(args) == 1 and category:
            supply_list = dao.getAvailableSuppliesByCategory(category)
        else:
            return jsonify(Error="Malformed query string"), 400
        result_list = []
        for row in supply_list:
            result = self.build_supply_dict(row)
            result_list.append(result)
        return jsonify(Supply_Posts=result_list)

    def insert_supply(self, form):
        if len(form) != 8:
            return jsonify(Error="Malformed post request"), 400
        else:
            dao = SupplyDAO()
            category_id = form['category_id']
            person_id = form['person_id']
            name = form['name']
            quantity = form['quantity']
            brand = form['brand']
            description = form['description']
            unit_price = form['sunit_price']
            address_id = form['address_id']

            if person_id and category_id and name and brand and description and unit_price and quantity \
                    and address_id:
                available = quantity
                resource_id = ResourceDAO().insert(category_id, person_id, name, quantity, brand)
                supply_id = dao.insert(resource_id, person_id, description, available, unit_price,
                                       address_id)
                result = self.build_supply_attributes(supply_id, resource_id, category_id, person_id, name, quantity,
                                                      brand, description, available, unit_price, address_id)
                return jsonify(Supply=result), 201
            else:
                return jsonify(Error="Unexpected attributes in post request"), 400

    def insert_supply_json(self, json):
        dao = SupplyDAO()
        category_id = json['category_id']
        person_id = json['person_id']
        name = json['name']
        quantity = json['quantity']
        brand = json['brand']
        description = json['description']
        available = quantity
        unit_price = json['sunit_price']
        address_id = json['address_id']

        if person_id and category_id and name and available and brand and description and unit_price and quantity \
                and address_id:
            #resource_id = ResourceDAO().insert(category_id, person_id, name, quantity, brand)
            resource_id = 0
            supply_id = dao.insert(resource_id, person_id, description, available, unit_price, address_id)
            result = self.build_supply_attributes(supply_id, resource_id, category_id, person_id, name, quantity, brand,
                                                  description, available, unit_price, address_id)
            return jsonify(Supply=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request"), 400

    def delete_supply(self, supply_id):
        dao = SupplyDAO()
        if not dao.getSupplyById(supply_id):
            return jsonify(Error="Post not found."), 404
        else:
            dao.delete(supply_id)
        return jsonify(DeleteStatus="OK"), 200

    def update_supply(self, supply_id, form):
        dao = SupplyDAO()
        if not dao.getSupplyById(supply_id):
            return jsonify(Error="Post not found."), 404
        else:
            if len(form) != 4:
                return jsonify(Error="Malformed update request"), 400
            else:
                description = form['description']
                unit_price = form['sunit_price']
                available = form['available']
                address_id = form['address_id']

                if int(available) < 0:
                    return jsonify(Error="Cannot put negative value in available"), 400
                if description and unit_price and available and address_id:
                    dao.update(supply_id, description, available, unit_price, address_id)
                    row = dao.getSupplyById(supply_id)
                    result = self.build_supply_dict(row)
                    return jsonify(Part=result), 200
                else:
                    return jsonify(Error="Unexpected attributes in update request"), 400
