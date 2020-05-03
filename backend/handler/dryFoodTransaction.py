from flask import jsonify
from backend.dao.dryFoodTransaction import DryFoodTransactionDAO
import datetime, pytz


class DryFoodTransactionHandler:
    def build_df_trans_dict(self, row):
        result = {
            'df_trans_id': row[0],
            'df_id': row[1],
            'person_id': row[2],
            'tquantity': row[3],
            'tunit_price': row[4],
            'trans_total': row[5],
            'date_completed': row[6]}
        return result

    def build_df_trans_attributes(self, df_trans_id, df_id, person_id, tquantity, tunit_price, trans_total, date_completed):
        result = {
            'df_trans_id': df_trans_id,
            'df_id': df_id,
            'person_id': person_id,
            'tquantity': tquantity,
            'tunit_price': tunit_price,
            'trans_total': trans_total,
            'date_completed': date_completed}
        return result

    def getAllDryFoodTransaction(self):
        dao = DryFoodTransactionDAO()
        df_transaction_list = dao.getAllDryFoodTransactions()
        result_list = []
        for row in df_transaction_list:
            result = self.build_df_trans_dict(row)
            result_list.append(result)
        return jsonify(DryFoodTransactions=result_list)

    def getDryFoodTransactionById(self, tid):
        dao = DryFoodTransactionDAO()
        row = dao.getTransactionById(tid)
        if not row:
            return jsonify(Error = "Transaction Not Found"), 404
        else:
            dryFoodTransaction = self.build_df_trans_dict(row)
            return jsonify(DryFoodTransaction = dryFoodTransaction)

    def insertDryFoodTransaction(self, form):
        print("form: ", form)
        if len(form) != 4:
            return jsonify(Error = "Malformed post request"), 400
        else:
            df_id = form['df_id']
            person_id = form['person_id']
            tquantity = form['tquantity']
            tunit_price = form['tunit_price']
            trans_total = tquantity * tunit_price
            date_completed = datetime.datetime.now(pytz.timezone('US/Eastern')).timestamp()
            if df_id and person_id and tquantity and tunit_price:
                dao = DryFoodTransactionDAO()
                df_trans_id = dao.insert(df_id,person_id,tquantity,tunit_price,trans_total,date_completed)
                result = self.build_df_trans_attributes(df_trans_id, df_id, person_id, tquantity, tunit_price, trans_total, date_completed)
                return jsonify(DryFoodTransaction=result), 201
            else:
                return jsonify(Error="Unexpected attributes in post request"), 400

    def insertDryFoodTransactionJson(self, json):
        df_id = json['df_id']
        person_id = json['person_id']
        tquantity = json['tquantity']
        tunit_price = json['tunit_price']
        trans_total = tquantity * tunit_price
        date_completed = datetime.datetime.now(pytz.timezone('US/Eastern')).timestamp()
        if df_id and person_id and tquantity and tunit_price:
            dao = DryFoodTransactionDAO()
            df_trans_id = dao.insert(df_id, person_id, tquantity, tunit_price, trans_total, date_completed)
            result = self.build_df_trans_attributes(df_trans_id, df_id, person_id, tquantity, tunit_price,
                                                       trans_total, date_completed)
            return jsonify(DryFoodTransaction=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request"), 400

    # Should never be used but still here
    def deleteDryFoodTransaction(self, tid):
        dao = DryFoodTransactionDAO()
        if not dao.getTransactionById(tid):
            return jsonify(Error = "Transaction not found."), 404
        else:
            dao.delete(tid)
            return jsonify(DeleteStatus = "OK"), 200

    def updatePart(self, tid, form):
        dao = DryFoodTransactionDAO()
        if not dao.getTransactionById(tid):
            return jsonify(Error = "Transaction not found."), 404
        else:
            if len(form) != 4:
                return jsonify(Error="Malformed update request"), 400
            else:
                df_id = form['df_id']
                person_id = form['person_id']
                tquantity = form['tquantity']
                tunit_price = form['tunit_price']
                trans_total = tquantity * tunit_price
                if df_id and person_id and tquantity and tunit_price:
                    dao.update(tid, df_id,person_id,tquantity,tunit_price,trans_total)
                    result = self.build_df_trans_attributes(tid, df_id,person_id,tquantity,tunit_price,trans_total,' ')
                    return jsonify(DryFoodTransaction=result), 200
                else:
                    return jsonify(Error="Unexpected attributes in update request"), 400