from flask import jsonify
from backend.dao.clothingTransaction import ClothingTransactionDAO
import datetime
import pytz


class ClothingTransactionHandler:
    def build_c_trans_dict(self, row):
        result = {
            'clothing_trans_id': row[0],
            'clothing_id': row[1],
            'person_id': row[2],
            'tquantity': row[3],
            'tunit_price': row[4],
            'trans_total': row[5],
            'date_completed': row[6]}
        return result

    def build_c_trans_attributes(self, clothing_trans_id, clothing_id, person_id, tquantity, tunit_price, trans_total, date_completed):
        result = {
            'clothing_trans_id': clothing_trans_id,
            'clothing_id': clothing_id,
            'person_id': person_id,
            'tquantity': tquantity,
            'tunit_price': tunit_price,
            'trans_total': trans_total,
            'date_completed': date_completed}
        return result

    def getAllClothingTransactions(self):
        dao = ClothingTransactionDAO()
        t_transaction_list = dao.getAllClothingTransactions()
        result_list = []
        for row in t_transaction_list:
            result = self.build_c_trans_dict(row)
            result_list.append(result)
        return jsonify(ClothingTransactions=result_list)

    def getClothingTransactionById(self, tid):
        dao = ClothingTransactionDAO()
        row = dao.getTransactionById(tid)
        if not row:
            return jsonify(Error = "Transaction Not Found"), 404
        else:
            ClothingTransaction = self.build_c_trans_dict(row)
            return jsonify(ClothingTransaction = ClothingTransaction)

    def insertClothingTransaction(self, form):
        print("form: ", form)
        if len(form) != 4:
            return jsonify(Error = "Malformed post request"), 400
        else:
            clothing_id = form['clothing_id']
            person_id = form['person_id']
            tquantity = form['tquantity']
            tunit_price = form['tunit_price']
            trans_total = tquantity * tunit_price
            date_completed = datetime.datetime.now(pytz.timezone('US/Eastern'))
            if clothing_id and person_id and tquantity and tunit_price:
                dao = ClothingTransactionDAO()
                clothing_trans_id = dao.insert(clothing_id, person_id, tquantity, tunit_price, trans_total, date_completed)
                result = self.build_c_trans_attributes(clothing_trans_id, clothing_id, person_id, tquantity, tunit_price, trans_total, date_completed)
                return jsonify(ClothingTransaction=result), 201
            else:
                return jsonify(Error="Unexpected attributes in post request"), 400

    def insertClothingTransactionJson(self, json):
        clothing_id = json['clothing_id']
        person_id = json['person_id']
        tquantity = json['tquantity']
        tunit_price = json['tunit_price']
        trans_total = tquantity * tunit_price
        date_completed = datetime.datetime.now(pytz.timezone('US/Eastern'))
        if clothing_id and person_id and tquantity and tunit_price:
            dao = ClothingTransactionDAO()
            clothing_trans_id = dao.insert(clothing_id, person_id, tquantity, tunit_price, trans_total, date_completed)
            result = self.build_c_trans_attributes(clothing_trans_id, clothing_id, person_id, tquantity, tunit_price,
                                                       trans_total, date_completed)
            return jsonify(ClothingTransaction=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request"), 400

    # Should never be used but still here
    def deleteClothingTransaction(self, tid):
        dao = ClothingTransactionDAO()
        if not dao.getTransactionById(tid):
            return jsonify(Error = "Transaction not found."), 404
        else:
            dao.delete(tid)
            return jsonify(DeleteStatus = "OK"), 200