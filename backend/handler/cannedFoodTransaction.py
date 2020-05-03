from flask import jsonify
from backend.dao.cannedFoodTransaction import CannedFoodTransactionDAO
import datetime, pytz


class CannedFoodTransactionHandler:
    def build_cf_trans_dict(self, row):
        result = {
            'cf_trans_id': row[0],
            'cf_id': row[1],
            'person_id': row[2],
            'tquantity': row[3],
            'tunit_price': row[4],
            'trans_total': row[5],
            'date_completed': row[6]}
        return result

    def build_cf_trans_attributes(self, cf_trans_id, cf_id, person_id, tquantity, tunit_price, trans_total, date_completed):
        result = {
            'cf_trans_id': cf_trans_id,
            'cf_id': cf_id,
            'person_id': person_id,
            'tquantity': tquantity,
            'tunit_price': tunit_price,
            'trans_total': trans_total,
            'date_completed': date_completed}
        return result

    def getAllCannedFoodTransaction(self):
        dao = CannedFoodTransactionDAO()
        cf_transaction_list = dao.getAllCannedFoodTransactions()
        result_list = []
        for row in cf_transaction_list:
            result = self.build_cf_trans_dict(row)
            result_list.append(result)
        return jsonify(CannedFoodTransactions=result_list)

    def getCannedFoodTransactionById(self, tid):
        dao = CannedFoodTransactionDAO()
        row = dao.getTransactionById(tid)
        if not row:
            return jsonify(Error = "Transaction Not Found"), 404
        else:
            cannedFoodTransaction = self.build_cf_trans_dict(row)
            return jsonify(CannedFoodTransaction = cannedFoodTransaction)

    def insertCannedFoodTransaction(self, form):
        print("form: ", form)
        if len(form) != 4:
            return jsonify(Error = "Malformed post request"), 400
        else:
            cf_id = form['cf_id']
            person_id = form['person_id']
            tquantity = form['tquantity']
            tunit_price = form['tunit_price']
            trans_total = tquantity * tunit_price
            date_completed = datetime.datetime.now(pytz.timezone('US/Eastern'))
            if cf_id and person_id and tquantity and tunit_price:
                dao = CannedFoodTransactionDAO()
                cf_trans_id = dao.insert(cf_id,person_id,tquantity,tunit_price,trans_total,date_completed)
                result = self.build_cf_trans_attributes(cf_trans_id, cf_id, person_id, tquantity, tunit_price, trans_total, date_completed)
                return jsonify(CannedFoodTransaction=result), 201
            else:
                return jsonify(Error="Unexpected attributes in post request"), 400

    def insertCannedFoodTransactionJson(self, json):
        cf_id = json['cf_id']
        person_id = json['person_id']
        tquantity = json['tquantity']
        tunit_price = json['tunit_price']
        trans_total = tquantity * tunit_price
        date_completed = datetime.datetime.now(pytz.timezone('US/Eastern'))
        if cf_id and person_id and tquantity and tunit_price:
            dao = CannedFoodTransactionDAO()
            cf_trans_id = dao.insert(cf_id, person_id, tquantity, tunit_price, trans_total, date_completed)
            result = self.build_cf_trans_attributes(cf_trans_id, cf_id, person_id, tquantity, tunit_price,
                                                       trans_total, date_completed)
            return jsonify(CannedFoodTransaction=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request"), 400

    # Should never be used but still here
    def deleteCannedFoodTransaction(self, tid):
        dao = CannedFoodTransactionDAO()
        if not dao.getTransactionById(tid):
            return jsonify(Error = "Transaction not found."), 404
        else:
            dao.delete(tid)
            return jsonify(DeleteStatus = "OK"), 200

    def updatePart(self, tid, form):
        dao = CannedFoodTransactionDAO()
        if not dao.getTransactionById(tid):
            return jsonify(Error = "Transaction not found."), 404
        else:
            if len(form) != 4:
                return jsonify(Error="Malformed update request"), 400
            else:
                cf_id = form['cf_id']
                person_id = form['person_id']
                tquantity = form['tquantity']
                tunit_price = form['tunit_price']
                trans_total = tquantity * tunit_price
                if cf_id and person_id and tquantity and tunit_price:
                    dao.update(tid, cf_id,person_id,tquantity,tunit_price,trans_total)
                    result = self.build_cf_trans_attributes(tid, cf_id,person_id,tquantity,tunit_price,trans_total,' ')
                    return jsonify(CannedFoodTransaction=result), 200
                else:
                    return jsonify(Error="Unexpected attributes in update request"), 400