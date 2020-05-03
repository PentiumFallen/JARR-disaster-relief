from flask import jsonify
from backend.dao.waterTransaction import WaterTransactionDAO
import datetime, pytz


class WaterTransactionHandler:
    def build_water_trans_dict(self, row):
        result = {
            'water_trans_id': row[0],
            'water_id': row[1],
            'person_id': row[2],
            'tquantity': row[3],
            'tunit_price': row[4],
            'trans_total': row[5],
            'date_completed': row[6]}
        return result

    def build_water_trans_attributes(self, water_trans_id, water_id, person_id, tquantity, tunit_price, trans_total, date_completed):
        result = {
            'water_trans_id': water_trans_id,
            'water_id': water_id,
            'person_id': person_id,
            'tquantity': tquantity,
            'tunit_price': tunit_price,
            'trans_total': trans_total,
            'date_completed': date_completed}
        return result

    def getAllWaterTransaction(self):
        dao = WaterTransactionDAO()
        water_transaction_list = dao.getAllWaterTransactions()
        result_list = []
        for row in water_transaction_list:
            result = self.build_water_trans_dict(row)
            result_list.append(result)
        return jsonify(WaterTransactions=result_list)

    def getWaterTransactionById(self, tid):
        dao = WaterTransactionDAO()
        row = dao.getTransactionById(tid)
        if not row:
            return jsonify(Error = "Transaction Not Found"), 404
        else:
            waterTransaction = self.build_water_trans_dict(row)
            return jsonify(WaterTransaction = waterTransaction)

    def insertWaterTransaction(self, form):
        print("form: ", form)
        if len(form) != 4:
            return jsonify(Error = "Malformed post request"), 400
        else:
            water_id = form['water_id']
            person_id = form['person_id']
            tquantity = form['tquantity']
            tunit_price = form['tunit_price']
            trans_total = tquantity * tunit_price
            date_completed = datetime.datetime.now(pytz.timezone('US/Eastern')).timestamp().timestamp()
            if water_id and person_id and tquantity and tunit_price:
                dao = WaterTransactionDAO()
                water_trans_id = dao.insert(water_id,person_id,tquantity,tunit_price,trans_total,date_completed)
                result = self.build_water_trans_attributes(water_trans_id, water_id, person_id, tquantity, tunit_price, trans_total, date_completed)
                return jsonify(WaterTransaction=result), 201
            else:
                return jsonify(Error="Unexpected attributes in post request"), 400

    def insertWaterTransactionJson(self, json):
        water_id = json['water_id']
        person_id = json['person_id']
        tquantity = json['tquantity']
        tunit_price = json['tunit_price']
        trans_total = tquantity * tunit_price
        date_completed = datetime.datetime.now(pytz.timezone('US/Eastern')).timestamp()
        if water_id and person_id and tquantity and tunit_price:
            dao = WaterTransactionDAO()
            water_trans_id = dao.insert(water_id, person_id, tquantity, tunit_price, trans_total, date_completed)
            result = self.build_water_trans_attributes(water_trans_id, water_id, person_id, tquantity, tunit_price,
                                                       trans_total, date_completed)
            return jsonify(WaterTransaction=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request"), 400

    # Should never be used but still here
    def deleteWaterTransaction(self, tid):
        dao = WaterTransactionDAO()
        if not dao.getTransactionById(tid):
            return jsonify(Error = "Transaction not found."), 404
        else:
            dao.delete(tid)
            return jsonify(DeleteStatus = "OK"), 200

    def updatePart(self, tid, form):
        dao = WaterTransactionDAO()
        if not dao.getTransactionById(tid):
            return jsonify(Error = "Transaction not found."), 404
        else:
            if len(form) != 4:
                return jsonify(Error="Malformed update request"), 400
            else:
                water_id = form['water_id']
                person_id = form['person_id']
                tquantity = form['tquantity']
                tunit_price = form['tunit_price']
                trans_total = tquantity * tunit_price
                if water_id and person_id and tquantity and tunit_price:
                    dao.update(tid, water_id,person_id,tquantity,tunit_price,trans_total)
                    result = self.build_water_trans_attributes(tid, water_id,person_id,tquantity,tunit_price,trans_total,' ')
                    return jsonify(WaterTransaction=result), 200
                else:
                    return jsonify(Error="Unexpected attributes in update request"), 400