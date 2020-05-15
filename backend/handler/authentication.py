from flask import jsonify
from backend.dao.account import AccountDAO
from backend.dao.person import PersonDAO
from backend.dao.address import AddressDao


class Auth:
    def signup(self, form):
        if len(form) != 10:
            return jsonify(Error="Malformed post request"), 400
        else:
            # account
            email = form['email']
            #ToDo: Hash password
            password = form['password']
            is_admin = form['is_admin']
            bank_account = form['bank_account']
            routing_number = form['routing_number']
            # person
            first_name = form['first_name']
            last_name = form['last_name']
            # address
            address = form['address']
            city = form['city']
            zip_code = form['zip_code']

            if email and password and is_admin and bank_account and routing_number and first_name and last_name and address and city and zip_code:
                address_id = AddressDao().insert(address, city, zip_code)
                person_id = PersonDAO().insertPerson(first_name, last_name, address_id)
                AccountDAO().insertAccount(person_id, email, password, is_admin, bank_account, routing_number)
                return jsonify(Account="Account created!")
            else:
                return jsonify(Error="Unexpected arguments in post request"), 400
