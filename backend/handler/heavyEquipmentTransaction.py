from flask import jsonify
from backend.dao.heavyEquipmentTransaction import HeavyEquipmentTransactionDAO



class HeavyEquipmentTransactionHandler:
    def build_he_trans_dict(self, row):
        result = {
            'heavy_equip_trans_id': row[0],
            'heavy_equip_id': row[1],
            'person_id': row[2],
            'tquantity': row[3],
            'tunit_price': row[4],
            'trans_total': row[5]}
        return result



    def build_he_trans_attributes(self, heavy_equip_trans_id, heavy_equip_id, person_id, tquantity, tunit_price, trans_total):
        result = {
            'heavy_equip_trans_id': heavy_equip_trans_id,
            'heavy_equip_id': heavy_equip_id,
            'person_id': person_id,
            'tquantity': tquantity,
            'tunit_price': tunit_price,
            'trans_total': trans_total}
        return result

    def getAllHeavyEquipmentTransactions(self):
        dao = HeavyEquipmentTransactionDAO()
        he_transaction_list = dao.getAllHeavyEquipmentTransactions()
        result_list = []
        for row in he_transaction_list:
            result = self.build_he_trans_dict(row)
            result_list.append(result)
        return jsonify(HeavyEquipmentTransactions=result_list)

    def getHeavyEquipmentTransactionById(self, tid):
        dao = HeavyEquipmentTransactionDAO()
        row = dao.getTransactionById(tid)
        if not row:
            return jsonify(Error = "Transaction Not Found"), 404
        else:
            HeavyEquipmentTransaction = self.build_he_trans_dict(row)
            return jsonify(HeavyEquipmentTransaction = HeavyEquipmentTransaction)

    def insertHeavyEquipmentTransaction(self, form):
        print("form: ", form)
        if len(form) != 4:
            return jsonify(Error = "Malformed post request"), 400
        else:
            heavy_equip_id = form['heavy_equip_id']
            person_id = form['person_id']
            tquantity = form['tquantity']
            tunit_price = form['tunit_price']
            trans_total = tquantity * tunit_price
            if heavy_equip_id and person_id and tquantity and tunit_price:
                dao = HeavyEquipmentTransactionDAO()
                heavy_equip_trans_id = dao.insert(heavy_equip_id, person_id, tquantity, tunit_price, trans_total)
                result = self.build_he_trans_attributes(heavy_equip_trans_id, heavy_equip_id, person_id, tquantity, tunit_price, trans_total)
                return jsonify(HeavyEquipmentTransaction=result), 201
            else:
                return jsonify(Error="Unexpected attributes in post request"), 400

    def insertHeavyEquipmentTransactionJson(self, json):
        heavy_equip_id = json['heavy_equip_id']
        person_id = json['person_id']
        tquantity = json['tquantity']
        tunit_price = json['tunit_price']
        trans_total = tquantity * tunit_price
        if heavy_equip_id and person_id and tquantity and tunit_price:
            dao = HeavyEquipmentTransactionDAO()
            heavy_equip_trans_id = dao.insert(heavy_equip_id, person_id, tquantity, tunit_price, trans_total)
            result = self.build_he_trans_attributes(heavy_equip_trans_id, heavy_equip_id, person_id, tquantity, tunit_price,
                                                       trans_total)
            return jsonify(HeavyEquipmentTransaction=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request"), 400

    # Should never be used but still here
    def deleteHeavyEquipmentTransaction(self, tid):
        dao = HeavyEquipmentTransactionDAO()
        if not dao.getTransactionById(tid):
            return jsonify(Error = "Transaction not found."), 404
        else:
            dao.delete(tid)
            return jsonify(DeleteStatus = "OK"), 200