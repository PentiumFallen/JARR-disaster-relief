from flask import jsonify
from backend.dao.babyFoodTransaction import BabyFoodTransactionDAO
import datetime, pytz


class BabyFoodTransactionHandler:
    def build_bf_trans_dict(self, row):
        result = {
            'bf_trans_id': row[0],
            'bf_id': row[1],
            'person_id': row[2],
            'tquantity': row[3],
            'tunit_price': row[4],
            'trans_total': row[5],
            'date_completed': row[6]}
        return result

    def build_bf_trans_attributes(self, bf_trans_id, bf_id, person_id, tquantity, tunit_price, trans_total, date_completed):
        result = {
            'bf_trans_id': bf_trans_id,
            'bf_id': bf_id,
            'person_id': person_id,
            'tquantity': tquantity,
            'tunit_price': tunit_price,
            'trans_total': trans_total,
            'date_completed': date_completed}
        return result

    def getAllBabyFoodTransaction(self):
        dao = BabyFoodTransactionDAO()
        bf_transaction_list = dao.getAllBabyFoodTransactions()
        result_list = []
        for row in bf_transaction_list:
            result = self.build_bf_trans_dict(row)
            result_list.append(result)
        return jsonify(BabyFoodTransactions=result_list)

    def getBabyFoodTransactionById(self, tid):
        dao = BabyFoodTransactionDAO()
        row = dao.getTransactionById(tid)
        if not row:
            return jsonify(Error = "Transaction Not Found"), 404
        else:
            babyFoodTransaction = self.build_bf_trans_dict(row)
            return jsonify(BabyFoodTransaction = babyFoodTransaction)

    def insertBabyFoodTransaction(self, form):
        print("form: ", form)
        if len(form) != 4:
            return jsonify(Error = "Malformed post request"), 400
        else:
            bf_id = form['bf_id']
            person_id = form['person_id']
            tquantity = form['tquantity']
            tunit_price = form['tunit_price']
            trans_total = tquantity * tunit_price
            date_completed = datetime.datetime.now(pytz.timezone('US/Eastern'))
            if bf_id and person_id and tquantity and tunit_price:
                dao = BabyFoodTransactionDAO()
                bf_trans_id = dao.insert(bf_id,person_id,tquantity,tunit_price,trans_total,date_completed)
                result = self.build_bf_trans_attributes(bf_trans_id, bf_id, person_id, tquantity, tunit_price, trans_total, date_completed)
                return jsonify(BabyFoodTransaction=result), 201
            else:
                return jsonify(Error="Unexpected attributes in post request"), 400

    def insertBabyFoodTransactionJson(self, json):
        bf_id = json['bf_id']
        person_id = json['person_id']
        tquantity = json['tquantity']
        tunit_price = json['tunit_price']
        trans_total = tquantity * tunit_price
        date_completed = datetime.datetime.now(pytz.timezone('US/Eastern'))
        if bf_id and person_id and tquantity and tunit_price:
            dao = BabyFoodTransactionDAO()
            bf_trans_id = dao.insert(bf_id, person_id, tquantity, tunit_price, trans_total, date_completed)
            result = self.build_bf_trans_attributes(bf_trans_id, bf_id, person_id, tquantity, tunit_price,
                                                       trans_total, date_completed)
            return jsonify(BabyFoodTransaction=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request"), 400

    # Should never be used but still here
    def deleteBabyFoodTransaction(self, tid):
        dao = BabyFoodTransactionDAO()
        if not dao.getTransactionById(tid):
            return jsonify(Error = "Transaction not found."), 404
        else:
            dao.delete(tid)
            return jsonify(DeleteStatus = "OK"), 200

    def updatePart(self, tid, form):
        dao = BabyFoodTransactionDAO()
        if not dao.getTransactionById(tid):
            return jsonify(Error = "Transaction not found."), 404
        else:
            if len(form) != 4:
                return jsonify(Error="Malformed update request"), 400
            else:
                bf_id = form['bf_id']
                person_id = form['person_id']
                tquantity = form['tquantity']
                tunit_price = form['tunit_price']
                trans_total = tquantity * tunit_price
                if bf_id and person_id and tquantity and tunit_price:
                    dao.update(tid, bf_id,person_id,tquantity,tunit_price,trans_total)
                    result = self.build_bf_trans_attributes(tid, bf_id,person_id,tquantity,tunit_price,trans_total,' ')
                    return jsonify(BabyFoodTransaction=result), 200
                else:
                    return jsonify(Error="Unexpected attributes in update request"), 400