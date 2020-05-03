from flask import jsonify
from backend.dao.powerGeneratorTransaction import PowerGeneratorTransactionDAO
import datetime
import pytz


class PowerGeneratorTransactionHandler:
    def build_pg_trans_dict(self, row):
        result = {
            'generator_trans_id': row[0],
            'generator_id': row[1],
            'person_id': row[2],
            'tquantity': row[3],
            'tunit_price': row[4],
            'trans_total': row[5],
            'date_completed': row[6]}
        return result

    def build_pg_trans_attributes(self, generator_trans_id, generator_id, person_id, tquantity, tunit_price, trans_total, date_completed):
        result = {
            'generator_trans_id': generator_trans_id,
            'generator_id': generator_id,
            'person_id': person_id,
            'tquantity': tquantity,
            'tunit_price': tunit_price,
            'trans_total': trans_total,
            'date_completed': date_completed}
        return result

    def getAllPowerGeneratorTransactions(self):
        dao = PowerGeneratorTransactionDAO()
        t_transaction_list = dao.getAllPowerGeneratorTransactions()
        result_list = []
        for row in t_transaction_list:
            result = self.build_pg_trans_dict(row)
            result_list.append(result)
        return jsonify(PowerGeneratorTransactions=result_list)

    def getPowerGeneratorTransactionById(self, tid):
        dao = PowerGeneratorTransactionDAO()
        row = dao.getTransactionById(tid)
        if not row:
            return jsonify(Error = "Transaction Not Found"), 404
        else:
            PowerGeneratorTransaction = self.build_pg_trans_dict(row)
            return jsonify(PowerGeneratorTransaction = PowerGeneratorTransaction)

    def insertPowerGeneratorTransaction(self, form):
        print("form: ", form)
        if len(form) != 4:
            return jsonify(Error = "Malformed post request"), 400
        else:
            generator_id = form['generator_id']
            person_id = form['person_id']
            tquantity = form['tquantity']
            tunit_price = form['tunit_price']
            trans_total = tquantity * tunit_price
            date_completed = datetime.datetime.now(pytz.timezone('US/Eastern'))
            if generator_id and person_id and tquantity and tunit_price:
                dao = PowerGeneratorTransactionDAO()
                generator_trans_id = dao.insert(generator_id, person_id, tquantity, tunit_price, trans_total, date_completed)
                result = self.build_pg_trans_attributes(generator_trans_id, generator_id, person_id, tquantity, tunit_price, trans_total, date_completed)
                return jsonify(PowerGeneratorTransaction=result), 201
            else:
                return jsonify(Error="Unexpected attributes in post request"), 400

    def insertPowerGeneratorTransactionJson(self, json):
        generator_id = json['generator_id']
        person_id = json['person_id']
        tquantity = json['tquantity']
        tunit_price = json['tunit_price']
        trans_total = tquantity * tunit_price
        date_completed = datetime.datetime.now(pytz.timezone('US/Eastern'))
        if generator_id and person_id and tquantity and tunit_price:
            dao = PowerGeneratorTransactionDAO()
            generator_trans_id = dao.insert(generator_id, person_id, tquantity, tunit_price, trans_total, date_completed)
            result = self.build_pg_trans_attributes(generator_trans_id, generator_id, person_id, tquantity, tunit_price,
                                                       trans_total, date_completed)
            return jsonify(PowerGeneratorTransaction=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request"), 400

    # Should never be used but still here
    def deletePowerGeneratorTransaction(self, tid):
        dao = PowerGeneratorTransactionDAO()
        if not dao.getTransactionById(tid):
            return jsonify(Error = "Transaction not found."), 404
        else:
            dao.delete(tid)
            return jsonify(DeleteStatus = "OK"), 200