from flask import jsonify
from backend.dao.BatteryTransaction import BatteryTransactionDAO
import datetime
import pytz


class BatteryTransactionHandler:
    def build_b_trans_dict(self, row):
        result = {
            'battery_trans_id': row[0],
            'battery_id': row[1],
            'person_id': row[2],
            'tquantity': row[3],
            'tunit_price': row[4],
            'trans_total': row[5],
            'date_completed': row[6]}
        return result

    def build_b_trans_attributes(self, battery_trans_id, battery_id, person_id, tquantity, tunit_price, trans_total,
                                 date_completed):
        result = {
            'battery_trans_id': battery_trans_id,
            'battery_id': battery_id,
            'person_id': person_id,
            'tquantity': tquantity,
            'tunit_price': tunit_price,
            'trans_total': trans_total,
            'date_completed': date_completed}
        return result

    def getAllBatteryTransactions(self):
        dao = BatteryTransactionDAO()
        b_transaction_list = dao.getAllBatteryTransactions()
        result_list = []
        for row in b_transaction_list:
            result = self.build_b_trans_dict(row)
            result_list.append(result)
        return jsonify(BatteryTransactions=result_list)

    def getBatteryTransactionById(self, tid):
        dao = BatteryTransactionDAO()
        row = dao.getTransactionById(tid)
        if not row:
            return jsonify(Error="Transaction Not Found"), 404
        else:
            BatteryTransaction = self.build_b_trans_dict(row)
            return jsonify(BatteryTransaction=BatteryTransaction)

    def insertBatteryTransaction(self, form):
        print("form: ", form)
        if len(form) != 4:
            return jsonify(Error="Malformed post request"), 400
        else:
            battery_id = form['battery_id']
            person_id = form['person_id']
            tquantity = form['tquantity']
            tunit_price = form['tunit_price']
            trans_total = tquantity * tunit_price
            date_completed = datetime.datetime.now(pytz.timezone('US/Eastern'))
            if battery_id and person_id and tquantity and tunit_price:
                dao = BatteryTransactionDAO()
                battery_trans_id = dao.insert(battery_id, person_id, tquantity, tunit_price, trans_total,
                                              date_completed)
                result = self.build_b_trans_attributes(battery_trans_id, battery_id, person_id, tquantity, tunit_price,
                                                       trans_total, date_completed)
                return jsonify(BatteryTransaction=result), 201
            else:
                return jsonify(Error="Unexpected attributes in post request"), 400

    def insertBatteryTransactionJson(self, json):
        battery_id = json['battery_id']
        person_id = json['person_id']
        tquantity = json['tquantity']
        tunit_price = json['tunit_price']
        trans_total = tquantity * tunit_price
        date_completed = datetime.datetime.now(pytz.timezone('US/Eastern'))
        if battery_id and person_id and tquantity and tunit_price:
            dao = BatteryTransactionDAO()
            battery_trans_id = dao.insert(battery_id, person_id, tquantity, tunit_price, trans_total, date_completed)
            result = self.build_b_trans_attributes(battery_trans_id, battery_id, person_id, tquantity, tunit_price,
                                                   trans_total, date_completed)
            return jsonify(BatteryTransaction=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request"), 400

    # Should never be used but still here
    def deleteBatteryTransaction(self, tid):
        dao = BatteryTransactionDAO()
        if not dao.getTransactionById(tid):
            return jsonify(Error="Transaction not found."), 404
        else:
            dao.delete(tid)
            return jsonify(DeleteStatus="OK"), 200
