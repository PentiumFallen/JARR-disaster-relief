from flask import jsonify
from backend.dao import PersonDAO

class PersonHandler:
    def build_person_dict(self, row):
        result = {
            'person_id': row[0],
            'first_name': row[1],
            'last_name': row[2],
            'address': row[3],
            'senate_district': row[4],
            'phone_number': row[5],
            'current_location': row[6]
        }
        return result

    def build_person_attributes(self, person_id, first_name, last_name, address, senate_district, phone_number, current_location):
        result = {
            'person_id': person_id,
            'first_name': first_name,
            'last_name': last_name,
            'address': address,
            'senate_district': senate_district,
            'phone_number': phone_number,
            'current_location': current_location
        }
        return result

    def get_all_persons(self):
        # dao = PersonDAO()
        # result_list = dao.getAllPersons()
        persons = ['Get all persons works!']
        # for row in result_list:
        #     result = self.build_person_dict(row)
        #     result_list.append(result)
        return jsonify(Persons=persons)

    def get_person_by_id(self, person_id):
        # dao = PersonDAO()
        # row = dao.getPersonById()
        # if not row:
        #     return jsonify(Error = "Person Not Found"), 404
        # else:
        #     person = self.build_person_dict(row)
        return jsonify(Person='Person by person_id')

    def get_person_by_request_id(self, request_id):
        # dao = PersonDAO()
        # row = dao.getPersonByRequestId(request_id)
        # if not row:
        #     return jsonify(Error = "Person Not Found"), 404
        # else:
        #     person = self.build_person_dict(row)
        return jsonify(Person='Person by request_id')

    def get_person_by_supply_id(self, supply_id):
        # dao = PersonDAO()
        # row = dao.getPersonBySupplyId(supply_id)
        # if not row:
        #     return jsonify(Error = "Person Not Found"), 404
        # else:
        #     person = self.build_person_dict(row)
        return jsonify(Person='Person by supply_id')

    def insert_person(self, form):
        # if len(form) != 5:
        #     return jsonify(Error="Malformed post request"), 400
        # else:
        #     first_name = form['first_name']
        #     last_name = form['last_name']
        #     address = form['address']
        #     senate_district = form['senate_district']
        #     phone_number = form['phone_number']
        #     current_location = form['current_location'] 
        #     if first_name and last_name and address and senate_district and phone_number and current_location:
        #         dao = PersonDAO()
        #         pid = dao.insertPerson(first_name, last_name, address, senate_district, phone_number, current_location)
        #         result = self.build_person_attributes(self, first_name, last_name, address, senate_district, phone_number, current_location,)
        #         return jsonify(Person='Insert person (form)!')
        #     else:
        #         return jsonify(Error="Unexpected attributes in post request"), 400
        return jsonify(Person='Insert person (form)!')

    def insert_person_json(self, json):
        # first_name = json['rcategory']
        # last_name = json['last_name']
        # address = json['address']
        # senate_district = json['senate_district']
        # phone_number = json['phone_number']
        # current_location = json['current_location']
        # if first_name and last_name and address and senate_district and phone_number and current_location:
        #     dao = PersonDAO()
        #     pid = dao.insert(first_name, last_name, address, senate_district, phone_number, current_location)
        #     result = self.build_part_attributes(pid, first_name, last_name, address, senate_district, phone_number, current_location)
        #     return jsonify(Person="Insert person (json)!"), 201
        # else:
        #     return jsonify(Error="Unexpected attributes in post request"), 400
        return jsonify(Person="Insert person (json)!"), 201

    def delete_person(self, person_id):
        # dao = PersonDAO()
        # if not dao.getPersonById(person_id):
        #     return jsonify(Error = "Person not found."), 404
        # else:
        #     dao.delete(person_id)
        return jsonify(DeleteStatus="OK"), 200

    def update_person(self, person_id, form):
        # dao = PersonDAO()
        # if not dao.getPersonById(person_id):
        #     return jsonify(Error="Person not found."), 404
        # else:
        #     if len(form) != 5:
        #         return jsonify(Error="Malformed update request"), 400
        #     else:
        #         first_name = form['first_name']
        #         last_name = form['last_name']
        #         address = form['address']
        #         senate_district = form['senate_district']
        #         phone_number = form['phone_number']
        #         current_location = form['current_location'] 
        #         if first_name and last_name and address and senate_district and phone_number and current_location and person_id:
        #             pid = dao.updatePerson(first_name, last_name, address, senate_district, phone_number, current_location, person_id)
        #             result = self.build_person_attributes(self, first_name, last_name, address, senate_district, phone_number, current_location,)
        #             return jsonify(Person='Update person (form)!')
        #         else:
        #             return jsonify(Error="Unexpected attributes in update request"), 400
        return jsonify(Person='Update person (form)!')

    def update_person_location(self, new_location, person_id):
        dao = PersonDAO()
        if not dao.getPersonById(person_id):
            return jsonify(Error="Person not found."), 404
        else:
            if new_location and person_id:
                # pid = dao.updatePersonLocation(new_location, person_id)
                return jsonify(Person='Update person location!')
            else:
                return jsonify(Error="Unexpected attributes in update request"), 400

