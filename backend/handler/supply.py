from flask import jsonify
from backend.dao.supply import SupplyDAO


class SupplyHandler:
    def build_supply_dict(self, row):
        print(row[0])
        result = {
            'supply_id': row[0],
            'scategory': row[1],
            'sdescription': row[2],
            'saddress': row[3],
            'sprice': row[4]
        }
        return result

    def build_supply_attributes(self, supply_id, scategory, sdescription, saddress, sprice):
        result = {
            'supply_id': supply_id,
            'scategory': scategory,
            'sdescription': sdescription,
            'saddress': saddress,
            'sprice': sprice,
        }
        return result

    def get_all_supplies(self):
        dao = SupplyDAO()
        result_list = dao.getAllSupplies()
        for row in result_list:
            result = self.build_supply_dict(row)
            result_list.append(result)
        return jsonify(Supplies=result_list)

    def get_supply_by_id(self, supply_id):
        dao = SupplyDAO()
        row = dao.getSupplyById(supply_id)
        if not row:
            return jsonify(Error="Supply Not Found"), 404
        else:
            supply = self.build_supply_dict(row)
        return jsonify(Supply=supply)

    def get_supplies_by_person_id(self, person_id):
        supplies = 'Got supplies of person number ' + str(person_id)
        return jsonify(Supplies=supplies)

    def search_supply(self, args):
        category = args.get("category")
        address = args.get("address")
        dao = SupplyDAO()
        supply_list = []
        if (len(args) == 2) and category and address:
            supply_list = dao.getSuppliesByCategoryAndAddress(category, address)
        elif (len(args) == 1) and category:
            supply_list = dao.getSuppliesByCategory(category)
        elif (len(args) == 1) and address:
            supply_list = dao.getSuppliesByAddress(address)
        else:
            return jsonify(Error = "Malformed query string"), 400
        result_list = []
        for row in supply_list:
            result = self.build_supply_dict(row)
            result_list.append(result)
        return jsonify(Supplies=result_list)

    def match_supplies_to_request(self, args):
        dao = SupplyDAO()
        category = args.get("category")
        max_price = args.get("max_price")
        address = args.get("address")
        supply_list = []
        if (len(args) == 1) and category:
            supply_list = dao.getSuppliesByCategory(category)
        elif (len(args) == 2) and category and max_price:
            supply_list = dao.getSuppliesByCategoryAndMaxPrice(category, max_price)
        elif (len(args) == 3) and category and max_price and address:
            supply_list = dao.getSuppliesByCategoryAddressAndMaxPrice(category, address, max_price)
        else:
            return jsonify(Error = "Malformed querry string"), 400
        result_list = []
        for row in supply_list:
            result = self.build_supply_dict(row)
            result_list.append(result)
        return jsonify(Supplies=result_list)

    def insert_supply(self, form):
        if len(form) != 4:
            return jsonify(Error="Malformed post request"), 400
        else:
            scategory = form['scategory']
            sdescription = form['sdescription']
            saddress = form['saddress']
            sprice = form['sprice']
            if scategory and sdescription and saddress and sprice:
                dao = SupplyDAO()
                supply_id = dao.insert(scategory, sdescription, saddress, sprice)
                result = self.build_supply_attributes(supply_id, scategory, sdescription, saddress, sprice)
                return jsonify(Supply=result), 201
            else:
                return jsonify(Error="Unexpected attributes in post request"), 400

    def insert_supply_json(self, json):
        scategory = json['scategory']
        sdescription = json['sdescription']
        saddress = json['saddress']
        sprice = json['sprice']
        if scategory and saddress and sdescription and sprice:
            dao = SupplyDAO()
            supply_id = dao.insert(scategory, sdescription, saddress, sprice)
            result = self.build_supply_attributes(supply_id, scategory, sdescription, saddress, sprice)
            return jsonify(Part=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request"), 400

    def delete_supply(self, supply_id):
        dao = SupplyDAO()
        if not dao.getSupplyById(supply_id):
            return jsonify(Error="Part not found."), 404
        else:
            dao.delete(supply_id)
        return jsonify(DeleteStatus="OK"), 200

    def update_supply(self, supply_id, form):
        dao = SupplyDAO()
        if not dao.getSupplyById(supply_id):
            return jsonify(Error="Supply not found."), 404
        else:
            if len(form) != 4:
                return jsonify(Error="Malformed update request"), 400
            else:
                scategory = form['scategory']
                sdescription = form['sdescription']
                saddress = form['saddress']
                sprice = form['sprice']
                if scategory and saddress and sdescription and sprice:
                    dao.update(supply_id, scategory, sdescription, saddress, sprice)
                    result = self.build_supply_attributes(supply_id, scategory, sdescription, saddress, sprice)
                    return jsonify(Part=result), 200
                else:
                    return jsonify(Error="Unexpected attributes in update request"), 400

