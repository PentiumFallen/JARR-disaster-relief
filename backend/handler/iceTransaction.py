from flask import jsonify
from backend.dao.iceTransaction import IceTransactionDAO



class IceTransactionHandler:
    def build_ice_trans_dict(self, row):
        result = {
            'ice_trans_id': row[0],
            'ice_id': row[1],
            'person_id': row[2],
            'tquantity': row[3],
            'tunit_price': row[4],
            'trans_total': row[5]}
        return result



    def build_ice_trans_attributes(self, ice_trans_id, ice_id, person_id, tquantity, tunit_price, trans_total):
        result = {
            'ice_trans_id': ice_trans_id,
            'ice_id': ice_id,
            'person_id': person_id,
            'tquantity': tquantity,
            'tunit_price': tunit_price,
            'trans_total': trans_total}
        return result

    def getAllIceTransaction(self):
        dao = IceTransactionDAO()
        ice_transaction_list = dao.getAllIceTransactions()
        result_list = []
        for row in ice_transaction_list:
            result = self.build_ice_trans_dict(row)
            result_list.append(result)
        return jsonify(IceTransactions=result_list)

    def getIceTransactionById(self, tid):
        dao = IceTransactionDAO()
        row = dao.getTransactionById(tid)
        if not row:
            return jsonify(Error = "Transaction Not Found"), 404
        else:
            iceTransaction = self.build_ice_trans_dict(row)
            return jsonify(IceTransaction = iceTransaction)

    def insertIceTransaction(self, form):
        print("form: ", form)
        if len(form) != 4:
            return jsonify(Error = "Malformed post request"), 400
        else:
            ice_id = form['ice_id']
            person_id = form['person_id']
            tquantity = form['tquantity']
            tunit_price = form['tunit_price']
            trans_total = tquantity * tunit_price
            if ice_id and person_id and tquantity and tunit_price:
                dao = IceTransactionDAO()
                ice_trans_id = dao.insert(ice_id,person_id,tquantity,tunit_price,trans_total)
                result = self.build_ice_trans_attributes(ice_trans_id, ice_id, person_id, tquantity, tunit_price, trans_total)
                return jsonify(IceTransaction=result), 201
            else:
                return jsonify(Error="Unexpected attributes in post request"), 400

    def insertIceTransactionJson(self, json):
        ice_id = json['ice_id']
        person_id = json['person_id']
        tquantity = json['tquantity']
        tunit_price = json['tunit_price']
        trans_total = tquantity * tunit_price
        if ice_id and person_id and tquantity and tunit_price:
            dao = IceTransactionDAO()
            ice_trans_id = dao.insert(ice_id, person_id, tquantity, tunit_price, trans_total)
            result = self.build_ice_trans_attributes(ice_trans_id, ice_id, person_id, tquantity, tunit_price,
                                                       trans_total)
            return jsonify(IceTransaction=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request"), 400

    # Should never be used but still here
    def deleteIceTransaction(self, tid):
        dao = IceTransactionDAO()
        if not dao.getTransactionById(tid):
            return jsonify(Error = "Transaction not found."), 404
        else:
            dao.delete(tid)
            return jsonify(DeleteStatus = "OK"), 200

    def updateTransaction(self, tid, form):
        dao = IceTransactionDAO()
        if not dao.getTransactionById(tid):
            return jsonify(Error = "Transaction not found."), 404
        else:
            if len(form) != 4:
                return jsonify(Error="Malformed update request"), 400
            else:
                ice_id = form['ice_id']
                person_id = form['person_id']
                tquantity = form['tquantity']
                tunit_price = form['tunit_price']
                trans_total = tquantity * tunit_price
                if ice_id and person_id and tquantity and tunit_price:
                    dao.update(tid, ice_id,person_id,tquantity,tunit_price,trans_total)
                    result = self.build_ice_trans_attributes(tid, ice_id,person_id,tquantity,tunit_price,trans_total)
                    return jsonify(IceTransaction=result), 200
                else:
                    return jsonify(Error="Unexpected attributes in update request"), 400