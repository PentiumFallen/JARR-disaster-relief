from flask import jsonify
from backend.dao.medicationTransaction import MedicationTransactionDAO



class MedicationTransactionHandler:
    def build_med_trans_dict(self, row):
        result = {
            'med_trans_id': row[0],
            'med_id': row[1],
            'person_id': row[2],
            'tquantity': row[3],
            'tunit_price': row[4],
            'trans_total': row[5]}
        return result



    def build_med_trans_attributes(self, med_trans_id, med_id, person_id, tquantity, tunit_price, trans_total):
        result = {
            'med_trans_id': med_trans_id,
            'med_id': med_id,
            'person_id': person_id,
            'tquantity': tquantity,
            'tunit_price': tunit_price,
            'trans_total': trans_total}
        return result

    def getAllMedicationTransaction(self):
        dao = MedicationTransactionDAO()
        med_transaction_list = dao.getAllMedicationTransactions()
        result_list = []
        for row in med_transaction_list:
            result = self.build_med_trans_dict(row)
            result_list.append(result)
        return jsonify(MedicationTransactions=result_list)

    def getMedicationTransactionById(self, tid):
        dao = MedicationTransactionDAO()
        row = dao.getTransactionById(tid)
        if not row:
            return jsonify(Error = "Transaction Not Found"), 404
        else:
            medicationTransaction = self.build_med_trans_dict(row)
            return jsonify(MedicationTransaction = medicationTransaction)

    def insertMedicationTransaction(self, form):
        print("form: ", form)
        if len(form) != 4:
            return jsonify(Error = "Malformed post request"), 400
        else:
            med_id = form['med_id']
            person_id = form['person_id']
            tquantity = form['tquantity']
            tunit_price = form['tunit_price']
            trans_total = tquantity * tunit_price
            if med_id and person_id and tquantity and tunit_price:
                dao = MedicationTransactionDAO()
                med_trans_id = dao.insert(med_id,person_id,tquantity,tunit_price,trans_total)
                result = self.build_med_trans_attributes(med_trans_id, med_id, person_id, tquantity, tunit_price, trans_total)
                return jsonify(MedicationTransaction=result), 201
            else:
                return jsonify(Error="Unexpected attributes in post request"), 400

    def insertMedicationTransactionJson(self, json):
        med_id = json['med_id']
        person_id = json['person_id']
        tquantity = json['tquantity']
        tunit_price = json['tunit_price']
        trans_total = tquantity * tunit_price
        if med_id and person_id and tquantity and tunit_price:
            dao = MedicationTransactionDAO()
            med_trans_id = dao.insert(med_id, person_id, tquantity, tunit_price, trans_total)
            result = self.build_med_trans_attributes(med_trans_id, med_id, person_id, tquantity, tunit_price,
                                                       trans_total)
            return jsonify(MedicationTransaction=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request"), 400

    # Should never be used but still here
    def deleteMedicationTransaction(self, tid):
        dao = MedicationTransactionDAO()
        if not dao.getTransactionById(tid):
            return jsonify(Error = "Transaction not found."), 404
        else:
            dao.delete(tid)
            return jsonify(DeleteStatus = "OK"), 200

    def updateTransaction(self, tid, form):
        dao = MedicationTransactionDAO()
        if not dao.getTransactionById(tid):
            return jsonify(Error = "Transaction not found."), 404
        else:
            if len(form) != 4:
                return jsonify(Error="Malformed update request"), 400
            else:
                med_id = form['med_id']
                person_id = form['person_id']
                tquantity = form['tquantity']
                tunit_price = form['tunit_price']
                trans_total = tquantity * tunit_price
                if med_id and person_id and tquantity and tunit_price:
                    dao.update(tid, med_id,person_id,tquantity,tunit_price,trans_total)
                    result = self.build_med_trans_attributes(tid, med_id,person_id,tquantity,tunit_price,trans_total)
                    return jsonify(MedicationTransaction=result), 200
                else:
                    return jsonify(Error="Unexpected attributes in update request"), 400