from flask import jsonify
from backend.dao.tool import ToolDao


class ToolHandler:

    def build_tool_dict(self, row):
        result = {}
        result['tool_id'] = row[0]
        result['person_id'] = row[1]
        result['brand'] = row[2]
        result['tool_name'] = row[3]
        result['description'] = row[4]
        result['quantity'] = row[5]
        result['unit_price'] = row[6]
        result['date_posted'] = row[7]
        result['curr_quantity'] = row[8]
        result['is_supply'] = row[9]
        result['address_id'] = row[10]
        return result

    def build_tool_attributes(self, tool_id, person_id, brand, tool_name, description, quantity, unit_price, date_posted,
                               curr_quantity, is_supply, address_id):
        result = {
            'tool_id': tool_id,
            'person_id': person_id,
            'brand': brand,
            'tool_name': tool_name,
            'description': description,
            'quantity': quantity,
            'unit_price': unit_price,
            'date_posted': date_posted,
            'curr_quantity': curr_quantity,
            'is_supply': is_supply,
            'address_id': address_id,
        }
        return result

    def get_all_tool_posts(self):
        dao = ToolDao()
        result_list = dao.getAllTool()
        for row in result_list:
            result = self.build_tool_dict(row)
            result_list.append(result)
        return jsonify(Tool_Posts=result_list)

    def get_all_tool_supplies(self):
        dao = ToolDao()
        result_list = dao.getAllToolSupplies()
        for row in result_list:
            result = self.build_tool_dict(row)
            result_list.append(result)
        return jsonify(Tool_Supplies=result_list)

    def get_all_tool_requests(self):
        dao = ToolDao()
        result_list = dao.getAllToolRequests()
        for row in result_list:
            result = self.build_tool_dict(row)
            result_list.append(result)
        return jsonify(Tool_Requests=result_list)

    def get_all_available_tool_supplies(self):
        dao = ToolDao()
        result_list = dao.getAllAvailableToolSupplies()
        for row in result_list:
            result = self.build_tool_dict(row)
            result_list.append(result)
        return jsonify(Tool_Supplies=result_list)

    def get_all_unfulfilled_tool_requests(self):
        dao = ToolDao()
        result_list = dao.getAllUnfulfilledToolRequests()
        for row in result_list:
            result = self.build_tool_dict(row)
            result_list.append(result)
        return jsonify(Tool_Requests=result_list)

    def get_tool_post_by_id(self, tool_id):
        dao = ToolDao()
        row = dao.gettoolById(tool_id)
        if not row:
            return jsonify(Error="Post Not Found"), 404
        else:
            result = self.build_tool_dict(row)
        return jsonify(tool_Post=result)

    def get_tool_posts_by_person_id(self, person_id):
        dao = ToolDao()
        result_list = dao.getToolByPersonId(person_id)
        for row in result_list:
            result = self.build_tool_dict(row)
            result_list.append(result)
        return jsonify(Tool_Posts=result_list)

    def get_tool_supplies_by_person_id(self, person_id):
        dao = ToolDao()
        result_list = dao.getToolSuppliesByPersonId(person_id)
        for row in result_list:
            result = self.build_tool_dict(row)
            result_list.append(result)
        return jsonify(Tool_Posts=result_list)

    def get_tool_requests_by_person_id(self, person_id):
        dao = ToolDao()
        result_list = dao.getToolRequestsByPersonId(person_id)
        for row in result_list:
            result = self.build_tool_dict(row)
            result_list.append(result)
        return jsonify(Tool_Posts=result_list)

    def search_tool_posts(self, args):
        brand = args['brand']
        tool_name = args['tool_name']
        dao = ToolDao()

        if len(args) == 2 and brand and tool_name:
            tool_list = dao.getToolByBrandAndName(brand, tool_name)
        elif len(args) == 1 and brand:
            tool_list = dao.getToolByBrand(brand)
        elif len(args) == 1 and tool_name:
            tool_list = dao.getToolByName(tool_name)
        else:
            return jsonify(Error="Malformed query string"), 400
        result_list = []
        for row in tool_list:
            result = self.build_tool_dict(row)
            result_list.append(result)
        return jsonify(Tool_Posts=result_list)

    def search_tool_supplies(self, args):
        brand = args['brand']
        max_price = args['unit_price']
        tool_name = args['tool_name']
        dao = ToolDao()

        if len(args) == 3 and brand and max_price and tool_name:
            tool_list = dao.getToolSuppliesByBrandAndNameAndMaxPrice(brand, tool_name, max_price)
        elif len(args) == 2 and brand and tool_name:
            tool_list = dao.getToolSuppliesByBrandAndName(brand, tool_name)
        elif len(args) == 1 and brand:
            tool_list = dao.gettoolSuppliesByBrand(brand)
        elif len(args) == 1 and max_price:
            tool_list = dao.getToolSuppliesByMaxPrice(max_price)
        elif len(args) == 1 and tool_name:
            tool_list = dao.getToolSuppliesByName(tool_name)
        else:
            return jsonify(Error="Malformed query string"), 400
        result_list = []
        for row in tool_list:
            result = self.build_tool_dict(row)
            result_list.append(result)
        return jsonify(Tool_Posts=result_list)

    def search_tool_requests(self, args):
        brand = args['brand']
        tool_name = args['tool_name']
        dao = ToolDao()

        if len(args) == 2 and brand and tool_name:
            tool_list = dao.getToolRequestsByBrandAndName(brand, tool_name)
        elif len(args) == 1 and brand:
            tool_list = dao.getToolRequestsByBrand(brand)
        elif len(args) == 1 and tool_name:
            tool_list = dao.getr(tool_name)
        else:
            return jsonify(Error="Malformed query string"), 400
        result_list = []
        for row in tool_list:
            result = self.build_tool_dict(row)
            result_list.append(result)
        return jsonify(Tool_Posts=result_list)

    def insert_tool_supply(self, form):
        if len(form) != 8:
            return jsonify(Error="Malformed post request"), 400
        else:
            dao = ToolDao()
            person_id = form['person_id']
            brand = form['brand']
            tool_name = form['tool_name']
            description = form['description']
            quantity = form['quantity']
            unit_price = form['unit_price']
            date_posted = form['date_posted']
            curr_quantity = quantity
            is_supply = True
            address_id = form['address_id']

            if person_id and brand and tool_name and description and unit_price and quantity and date_posted and \
                    address_id:
                tool_id = dao.insert(person_id, brand, description, quantity, unit_price, date_posted, curr_quantity,
                                      is_supply, address_id)
                result = self.build_tool_attributes(tool_id, person_id, brand, tool_name, description, quantity, unit_price,
                                                     date_posted, curr_quantity, is_supply, address_id)
                return jsonify(Supply=result), 201
            else:
                return jsonify(Error="Unexpected attributes in post request"), 400

    def insert_tool_supply_json(self, json):
        dao = ToolDao()
        person_id = json['person_id']
        brand = json['brand']
        tool_name = json['tool_name']
        description = json['description']
        quantity = json['quantity']
        unit_price = json['unit_price']
        date_posted = json['date_posted']
        curr_quantity = quantity
        is_supply = True
        address_id = json['address_id']

        if person_id and brand and tool_name and description and unit_price and quantity and date_posted and \
                address_id:
            tool_id = dao.insert(person_id, brand, description, quantity, unit_price, date_posted, curr_quantity,
                                  is_supply, address_id)
            result = self.build_tool_attributes(tool_id, person_id, brand, description, quantity, unit_price,
                                                 date_posted, curr_quantity, is_supply, address_id)
            return jsonify(Supply=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request"), 400

    def insert_tool_request(self, form):
        if len(form) != 8:
            return jsonify(Error="Malformed post request"), 400
        else:
            dao = ToolDao()
            person_id = form['person_id']
            brand = form['brand']
            tool_name = form['tool_name']
            description = form['description']
            quantity = form['quantity']
            unit_price = form['unit_price']
            date_posted = form['date_posted']
            curr_quantity = quantity
            is_supply = False
            address_id = form['address_id']

            if person_id and brand and tool_name and description and unit_price and quantity and date_posted and \
                    address_id:
                tool_id = dao.insert(person_id, brand, description, quantity, unit_price, date_posted, curr_quantity,
                                      is_supply, address_id)
                result = self.build_tool_attributes(tool_id, person_id, brand, description, quantity, unit_price,
                                                     date_posted, curr_quantity, is_supply, address_id)
                return jsonify(Supply=result), 201
            else:
                return jsonify(Error="Unexpected attributes in post request"), 400

    def insert_tool_request_json(self, json):
        dao = ToolDao()
        person_id = json['person_id']
        brand = json['brand']
        tool_name = json['tool_name']
        description = json['description']
        quantity = json['quantity']
        unit_price = json['unit_price']
        date_posted = json['date_posted']
        curr_quantity = quantity
        is_supply = False
        address_id = json['address_id']

        if person_id and brand and tool_name and description and unit_price and quantity and date_posted and \
                address_id:
            tool_id = dao.insert(person_id, brand, description, quantity, unit_price, date_posted, curr_quantity,
                                  is_supply, address_id)
            result = self.build_tool_attributes(tool_id, person_id, brand, description, quantity, unit_price,
                                                 date_posted, curr_quantity, is_supply, address_id)
            return jsonify(Supply=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request"), 400

    def delete_tool_post(self, tool_id):
        dao = ToolDao()
        if not dao.getToolById(tool_id):
            return jsonify(Error="Post not found."), 404
        else:
            dao.delete(tool_id)
        return jsonify(DeleteStatus="OK"), 200

    def update_supply(self, tool_id, form):
        dao = ToolDao()
        if not dao.getToolById(tool_id):
            return jsonify(Error="Post not found."), 404
        else:
            if len(form) != 9:
                return jsonify(Error="Malformed update request"), 400
            else:
                brand = form['brand']
                tool_name = form['tool_name']
                description = form['description']
                unit_price = form['unit_price']
                curr_quantity = form['quantity']
                address_id = form['address_id']

                if int(curr_quantity) < 0:
                    return jsonify(Error="Cannot put negative value"), 400
                if brand and tool_name and description and unit_price and curr_quantity and address_id:
                    dao.update(tool_id, brand, tool_name, description, unit_price, curr_quantity, address_id)
                    row = dao.gettoolById(tool_id)
                    result = self.build_tool_dict(row)
                    return jsonify(Part=result), 200
                else:
                    return jsonify(Error="Unexpected attributes in update request"), 400
