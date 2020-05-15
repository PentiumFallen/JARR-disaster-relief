from flask import jsonify
from backend.dao.person import PersonDAO


class PersonHandler:
    def build_person_dict(self, row):
        result = {
            'person_id': row[0],
            'first_name': row[1],
            'last_name': row[2],
            'address_id': row[3],
        }
        return result

    def build_person_attributes(self, person_id, first_name, last_name, address_id):
        result = {
            'person_id': person_id,
            'first_name': first_name,
            'last_name': last_name,
            'address_id': address_id,
        }
        return result

    def get_all_persons(self):
        dao = PersonDAO()
        person_list = dao.getAllPersons()
        result_list = []
        for row in person_list:
            result = self.build_person_dict(row)
            result_list.append(result)
        return jsonify(Persons=result_list)

    def get_person_by_id(self, person_id):
        dao = PersonDAO()
        row = dao.getPersonById(person_id)
        if not row:
            return jsonify(Error="Person Not Found"), 404
        else:
            person = self.build_person_dict(row)
        return jsonify(Person=person)

    def get_person_by_request_id(self, request_id):
        dao = PersonDAO()
        row = dao.getPersonByRequestId(request_id)
        if not row:
            return jsonify(Error="Person Not Found"), 404
        else:
            person = self.build_person_dict(row)
        return jsonify(Person=person)

    def get_person_by_supply_id(self, supply_id):
        dao = PersonDAO()
        row = dao.getPersonBySupplyId(supply_id)
        if not row:
            return jsonify(Error="Person Not Found"), 404
        else:
            person = self.build_person_dict(row)
        return jsonify(Person=person)

    def insert_person(self, form):
        if len(form) != 4:
            return jsonify(Error="Malformed post request"), 400
        else:
            first_name = form['first_name']
            last_name = form['last_name']
            phone_number = form['phone_number']
            address_id = form['address_id']
            if first_name and last_name and address_id and phone_number:
                dao = PersonDAO()
                dao.insertPerson(first_name, last_name, address_id)
                result = self.build_person_attributes(self, first_name, last_name, address_id)
                return jsonify(Person=result)
            else:
                return jsonify(Error="Unexpected attributes in post request"), 400

    def insert_person_json(self, json):
        first_name = json['first_name']
        last_name = json['last_name']
        phone_number = json['phone_number']
        address_id = json['address_id']
        if first_name and last_name and address_id and phone_number:
            dao = PersonDAO()
            pid = dao.insertPerson(first_name, last_name, address_id)
            result = self.build_person_attributes(pid, first_name, last_name, address_id)
            return jsonify(Person=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request"), 400

    def delete_person(self, person_id):
        dao = PersonDAO()
        if not dao.getPersonById(person_id):
            return jsonify(Error="Person not found."), 404
        else:
            dao.deletePerson(person_id)
        return jsonify(DeleteStatus="OK"), 200

    def update_person(self, person_id, form):
        dao = PersonDAO()
        if not dao.getPersonById(person_id):
            return jsonify(Error="Person not found."), 404
        else:
            if len(form) != 4:
                return jsonify(Error="Malformed update request"), 400
            else:
                first_name = form['first_name']
                last_name = form['last_name']
                phone_number = form['phone_number']
                address_id = form['address_id']
                if first_name and last_name and phone_number and person_id:
                    pid = dao.updatePerson(first_name, last_name, phone_number, person_id)
                    result = self.build_person_attributes(pid, first_name, last_name, address_id)
                    return jsonify(Person=result)
                else:
                    return jsonify(Error="Unexpected attributes in update request"), 400
