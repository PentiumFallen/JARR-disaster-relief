from flask import jsonify
from backend.dao.medicalDeviceTransaction import MedicalDeviceTransactionDAO



class MedicalDeviceTransactionHandler:
    def build_md_trans_dict(self, row):
        result = {
            'med_dev_trans_id': row[0],
            'medical_dev_id': row[1],
            'person_id': row[2],
            'tquantity': row[3],
            'tunit_price': row[4],
            'trans_total': row[5]}
        return result


    def build_md_trans_attributes(self, med_dev_trans_id, medical_dev_id, person_id, tquantity, tunit_price, trans_total):
        result = {
            'med_dev_trans_id': med_dev_trans_id,
            'medical_dev_id': medical_dev_id,
            'person_id': person_id,
            'tquantity': tquantity,
            'tunit_price': tunit_price,
            'trans_total': trans_total}
        return result

    def getAllMedicalDeviceTransactions(self):
        dao = MedicalDeviceTransactionDAO()
        md_transaction_list = dao.getAllMedicalDeviceTransactions()
        result_list = []
        for row in md_transaction_list:
            result = self.build_md_trans_dict(row)
            result_list.append(result)
        return jsonify(MedicalDeviceTransactions=result_list)

    def getMedicalDeviceTransactionById(self, tid):
        dao = MedicalDeviceTransactionDAO()
        row = dao.getTransactionById(tid)
        if not row:
            return jsonify(Error = "Transaction Not Found"), 404
        else:
            MedicalDeviceTransaction = self.build_md_trans_dict(row)
            return jsonify(MedicalDeviceTransaction = MedicalDeviceTransaction)

    def insertMedicalDeviceTransaction(self, form):
        print("form: ", form)
        if len(form) != 4:
            return jsonify(Error = "Malformed post request"), 400
        else:
            medical_dev_id = form['medical_dev_id']
            person_id = form['person_id']
            tquantity = form['tquantity']
            tunit_price = form['tunit_price']
            trans_total = tquantity * tunit_price
            if medical_dev_id and person_id and tquantity and tunit_price:
                dao = MedicalDeviceTransactionDAO()
                med_dev_trans_id = dao.insert(medical_dev_id, person_id, tquantity, tunit_price, trans_total)
                result = self.build_md_trans_attributes(med_dev_trans_id, medical_dev_id, person_id, tquantity, tunit_price, trans_total)
                return jsonify(MedicalDeviceTransaction=result), 201
            else:
                return jsonify(Error="Unexpected attributes in post request"), 400

    def insertMedicalDeviceTransactionJson(self, json):
        medical_dev_id = json['medical_dev_id']
        person_id = json['person_id']
        tquantity = json['tquantity']
        tunit_price = json['tunit_price']
        trans_total = tquantity * tunit_price
        if medical_dev_id and person_id and tquantity and tunit_price:
            dao = MedicalDeviceTransactionDAO()
            med_dev_trans_id = dao.insert(medical_dev_id, person_id, tquantity, tunit_price, trans_total)
            result = self.build_md_trans_attributes(med_dev_trans_id, medical_dev_id, person_id, tquantity, tunit_price, trans_total)
            return jsonify(MedicalDeviceTransaction=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request"), 400

    # Should never be used but still here
    def deleteMedicalDeviceTransaction(self, tid):
        dao = MedicalDeviceTransactionDAO()
        if not dao.getTransactionById(tid):
            return jsonify(Error = "Transaction not found."), 404
        else:
            dao.delete(tid)
            return jsonify(DeleteStatus = "OK"), 200

    # def updateMedicalDeviceTransation(self, tid, form):
    #     dao = MedicalDeviceTransactionDAO()
    #     if not dao.getTransactionById(tid):
    #         return jsonify(Error = "Transaction not found."), 404
    #     else:
    #         if len(form) != 4:
    #             return jsonify(Error="Malformed update request"), 400
    #         else:
    #             medical_dev_id = form['medical_dev_id']
    #             person_id = form['person_id']
    #             tquantity = form['tquantity']
    #             tunit_price = form['tunit_price']
    #             trans_total = tquantity * tunit_price
    #             if medical_dev_id and person_id and tquantity and tunit_price:
    #                 dao.update(tid, medical_dev_id, person_id, tquantity, tunit_price, trans_total)
    #                 result = self.build_md_trans_attributes(tid, medical_dev_id, person_id, tquantity,tunit_price,trans_total)
    #                 return jsonify(MedicalDeviceTransaction=result), 200
    #             else:
    #                 return jsonify(Error="Unexpected attributes in update request"), 400