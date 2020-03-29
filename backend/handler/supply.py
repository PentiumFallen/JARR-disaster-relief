from flask import jsonify

class SupplyHandler:
    def build_supply_dict(self, row):
        result = {
            'supply_id': row[0],
            'scategory': row[1],
            'sname': row[2],
            'sdescription': row[3],
            'saddress': row[4],
            'sprice': row[5],
            'sfulfilled': row[6]
        }
        return result

    def build_supply_attributes(self, supply_id, scategory, sname, sdescription, saddress, sprice, sfulfilled):
        result = {
            'supply_id': supply_id,
            'scategory': scategory,
            'sname': sname,
            'sdescription': sdescription,
            'saddress': saddress,
            'sprice': sprice,
            'sfulfilled': sfulfilled
        }
        return result

    def get_all_supplies(self):
        # dao = SupplyDAO()
        # supply_list = dao.get_all_supplies()
        result_list = ['Get all supplies works!']
        # for row in supply_list:
        #     result = self.build_supply_dict(row)
        #     result_list.append(result)
        return jsonify(Supplies=result_list)

    def get_supply_by_id(self, supply_id):
        # dao = PartsDAO()
        # row = dao.getPartById(pid)
        # if not row:
        #     return jsonify(Error = "Supply Not Found"), 404
        # else:
        #     supply = self.build_supply_dict(row)
        supply = 'Got supply ' + str(supply_id) + '!'
        return jsonify(Supply=supply)

    def search_supply(self, args):
        category = args.get("category")
        name = args.get("name")
        # Add more! #
        # dao = PartsDAO()
        supply_list = []
        # if (len(args) == 2) and category and name:
        #     supply_list = dao.getSupplyByCategoryAndName(category, name)
        # elif (len(args) == 1) and category:
        #     supply_list = dao.getSupplyByCategory(category)
        # elif (len(args) == 1) and name:
        #     supply_list = dao.getSupplyByName(name)
        # else:
        #     return jsonify(Error = "Malformed query string"), 400
        result_list = []
        result_list.append('Search supply works!')
        # for row in supply_list:
        #     result = self.build_part_dict(row)
        #     result_list.append(result)
        return jsonify(Supplies=result_list)

    def match_supplies_to_request(self, args):
        category = args.get("category")
        max_price = args.get("max_price")
        name = args.get("name")
        supply_list = []
        # if (len(args) == 1) and name:
        #     supply_list = dao.getSupplyBycategory(category)
        # elif (len(args) == 2) and category and max_price:
        #     supply_list = dao.getSupplyByCategoryAndMaxPrice(category, max_price)
        # elif (len(args) == 3) and category and max_price and name:
        #     supply_list = dao.getSupplyByCategoryNameAndMaxPrice(category, name, max_price)
        # else:
        #     return jsonify(Error = "Malformed querry string"), 400
        result_list = []
        result_list.append('Match supplies to request works!')
        # for row in supply_list:
        #     result = self.build_part_dict(row)
        #     result_list.append(result)
        return jsonify(Supplies=result_list)

    def insert_supply(self, form):
        if len(form) != 5:
            return jsonify(Error="Malformed post request"), 400
        else:
            scategory = form['scategory']
            sname = form['sname']
            sdescription = form['sdescription']
            saddress = form['saddress']
            sprice = form['sprice']
            sfulfilled = form['sfulfilled']
            if scategory and sname and sdescription and saddress and sprice and sfulfilled:
                # dao = SupplyDAO()
                # pid = dao.insert(scategory, sname, sdescription, saddress, sprice, sfulfilled)
                # result = build_supply_attributes(self, supply_id, scategory, sname, sdescription, saddress, sprice, sfulfilled)
                result = 'Insert works!'
                return jsonify(Supply=result), 201
            else:
                return jsonify(Error="Unexpected attributes in post request"), 400

    def insert_supply_json(self, json):
        scategory = json['scategory']
        sname = json['sname']
        sdescription = json['sdescription']
        saddress = json['saddress']
        sprice = json['sprice']
        sfulfilled = json['sfulfilled']
        if scategory and sname and saddress and sdescription and sprice and sfulfilled:
            # dao = PartsDAO()
            # pid = dao.insert(pname, pcolor, pmaterial, pprice, sfulfilled)
            # result = self.build_part_attributes(pid, pname, pcolor, pmaterial, pprice, sfulfilled)
            return jsonify(Part="Insert supply json works!"), 201
        else:
            return jsonify(Error="Unexpected attributes in post request"), 400

    def delete_supply(self, supply_id):
        # dao = SupplyDAO()
        # if not dao.getSupplyById(supply_id):
        #     return jsonify(Error = "Part not found."), 404
        # else:
        #     dao.delete(supply_id)
        return jsonify(DeleteStatus="OK"), 200

    def update_supply(self, supply_id, form):
        # dao = SupplyDAO()
        # if not dao.getPartById(supply_id):
        #     return jsonify(Error="Supply not found."), 404
        # else:
        #     if len(form) != 4:
        #         return jsonify(Error="Malformed update request"), 400
        #     else:
        #         scategory = form['scategory']
        #         sname = form['sname']
        #         sdescription = form['sdescription']
        #         saddress = form['saddress']
        #         sprice = form['sprice']
        #         sfulfilled = form['sfulfilled']
        #         if scategory and sname and saddress and sdescription and sprice:
        #             dao.update(supply_id, scategory, sname, sdescription, saddress, sprice, sfulfilled)
        #             result = self.build_part_attributes(supply_id, scategory, sname, sdescription, saddress, sprice, sfulfilled)
        #             return jsonify(Part=result), 200
        #         else:
        #             return jsonify(Error="Unexpected attributes in update request"), 400
        return jsonify(Supply="Update works!")

