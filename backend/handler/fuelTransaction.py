from flask import jsonify
from backend.dao.fuelTransaction import FuelTransactionDAO
import datetime, pytz


class FuelTransactionHandler:
    def build_fuel_trans_dict(self, row):
        result = {
            'fuel_trans_id': row[0],
            'fuel_id': row[1],
            'person_id': row[2],
            'tquantity': row[3],
            'tunit_price': row[4],
            'trans_total': row[5],
            'date_completed': row[6]}
        return result

    def build_fuel_trans_attributes(self, fuel_trans_id, fuel_id, person_id, tquantity, tunit_price, trans_total, date_completed):
        result = {
            'fuel_trans_id': fuel_trans_id,
            'fuel_id': fuel_id,
            'person_id': person_id,
            'tquantity': tquantity,
            'tunit_price': tunit_price,
            'trans_total': trans_total,
            'date_completed': date_completed}
        return result

    def getAllFuelTransaction(self):
        dao = FuelTransactionDAO()
        fuel_transaction_list = dao.getAllFuelTransactions()
        result_list = []
        for row in fuel_transaction_list:
            result = self.build_fuel_trans_dict(row)
            result_list.append(result)
        return jsonify(FuelTransactions=result_list)

    def getFuelTransactionById(self, tid):
        dao = FuelTransactionDAO()
        row = dao.getTransactionById(tid)
        if not row:
            return jsonify(Error = "Transaction Not Found"), 404
        else:
            fuelTransaction = self.build_fuel_trans_dict(row)
            return jsonify(FuelTransaction = fuelTransaction)

    def insertFuelTransaction(self, form):
        print("form: ", form)
        if len(form) != 4:
            return jsonify(Error = "Malformed post request"), 400
        else:
            fuel_id = form['fuel_id']
            person_id = form['person_id']
            tquantity = form['tquantity']
            tunit_price = form['tunit_price']
            trans_total = tquantity * tunit_price
            date_completed = datetime.datetime.now(pytz.timezone('US/Eastern')).timestamp()
            if fuel_id and person_id and tquantity and tunit_price:
                dao = FuelTransactionDAO()
                fuel_trans_id = dao.insert(fuel_id,person_id,tquantity,tunit_price,trans_total,date_completed)
                result = self.build_fuel_trans_attributes(fuel_trans_id, fuel_id, person_id, tquantity, tunit_price, trans_total, date_completed)
                return jsonify(FuelTransaction=result), 201
            else:
                return jsonify(Error="Unexpected attributes in post request"), 400

    def insertFuelTransactionJson(self, json):
        fuel_id = json['fuel_id']
        person_id = json['person_id']
        tquantity = json['tquantity']
        tunit_price = json['tunit_price']
        trans_total = tquantity * tunit_price
        date_completed = datetime.datetime.now(pytz.timezone('US/Eastern')).timestamp()
        if fuel_id and person_id and tquantity and tunit_price:
            dao = FuelTransactionDAO()
            fuel_trans_id = dao.insert(fuel_id, person_id, tquantity, tunit_price, trans_total, date_completed)
            result = self.build_fuel_trans_attributes(fuel_trans_id, fuel_id, person_id, tquantity, tunit_price,
                                                       trans_total, date_completed)
            return jsonify(FuelTransaction=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request"), 400

    # Should never be used but still here
    def deleteFuelTransaction(self, tid):
        dao = FuelTransactionDAO()
        if not dao.getTransactionById(tid):
            return jsonify(Error = "Transaction not found."), 404
        else:
            dao.delete(tid)
            return jsonify(DeleteStatus = "OK"), 200

    def updatePart(self, tid, form):
        dao = FuelTransactionDAO()
        if not dao.getTransactionById(tid):
            return jsonify(Error = "Transaction not found."), 404
        else:
            if len(form) != 4:
                return jsonify(Error="Malformed update request"), 400
            else:
                fuel_id = form['fuel_id']
                person_id = form['person_id']
                tquantity = form['tquantity']
                tunit_price = form['tunit_price']
                trans_total = tquantity * tunit_price
                if fuel_id and person_id and tquantity and tunit_price:
                    dao.update(tid, fuel_id,person_id,tquantity,tunit_price,trans_total)
                    result = self.build_fuel_trans_attributes(tid, fuel_id,person_id,tquantity,tunit_price,trans_total,' ')
                    return jsonify(FuelTransaction=result), 200
                else:
                    return jsonify(Error="Unexpected attributes in update request"), 400