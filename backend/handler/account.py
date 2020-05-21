from flask import jsonify

from backend.dao.account import AccountDAO
from backend.utility import senate_district


# Joined to person and address
class AccountHandler:
    def build_account_dict(self, row):
        result = {
            'account_id': row[0],
            'email': row[1],
            'password': row[2],
            'registered_date': row[3],
            'is_admin': row[4],
            'balance': row[5],
            'person_id': row[6],
            'bank_account_number': row[7],
            'routing_number': row[8],
            'first_name': row[9],
            'last_name' : row[10],
            'address': row[11],
            'city': row[12],
            'district': row[13],
            'zip_code': row[14]
        }
        return result

    def build_account_attributes(self, account_id, email, password, is_admin, person_id,
                                 balance, bank_account_number, routing_number, first_name,
                                 last_name, address, city, zip_code):
        result = {
            'account_id': account_id,
            'email': email,
            'password': password,
            'is_admin': is_admin,
            'person_id': person_id,
            'balance': balance,
            'bank_account_number': bank_account_number,
            'routing_number': routing_number,
            'first_name' : first_name,
            'last_name' : last_name,
            'address': address,
            'city': city,
            'district': senate_district[city.lower()],
            'zip_code': zip_code
        }
        return result

    def build_login(self, row):
        result = {
            'email': row[0],
            'password': row[1]
        }
        return result

    def get_all_account(self):
        dao = AccountDAO()
        account_list = dao.getAllAccount()
        result_list = []
        for row in account_list:
            result = self.build_account_dict(row)
            result_list.append(result)
        return jsonify(Accounts_list=result_list), 200

    def get_account_by_person_id(self, person_id):
        dao = AccountDAO()
        result = dao.getAccountByPersonId(person_id)
        if not result:
            return jsonify(Error='Account not found.'), 404
        else:
            res = self.build_account_dict(result)
            return jsonify(Account=res), 200

    def get_admin_accounts(self):
        dao = AccountDAO()
        admin_list = dao.getAdminAccounts()
        result_list = []
        if not admin_list:
            return jsonify(Error='Admins accounts not found.'), 404
        else:
            for row in admin_list:
                result = self.build_account_dict(row)
                result_list.append(result)
            return jsonify(Admins_accounts=result_list), 200

    def get_account_type(self, account_id):
        dao = AccountDAO()
        result = dao.getAccountType(account_id)
        return jsonify(Account_type=result), 200

    def delete_account(self, account_id):
        dao = AccountDAO()
        if not dao.getAccountById(account_id):
            return jsonify(Error="Account not found."), 404
        else:
            dao.deleteAccount(account_id)
        return jsonify(DeleteStatus="OK"), 200

    def accountLogin(self, form):
        email = form.get('email')
        password = form.get('password')

        if password and email:
            dao = AccountDAO()
            res = dao.accountLogin(email, password)
            if len(res) == 0:
                return jsonify(Error="No account found with that email or Password"), 404
            else:
                result_list = []
            for row in res:
                result = self.build_login(row)
                result_list.append(result)
                return jsonify(Account=result_list)
        else:
            return jsonify(Error="Unexpected attributes in Login request"), 400

    def accountChangePassword(self, form):
        email = form.get('email')
        password = form.get('password')
        if password and email and (len(form) == 2):
            dao = AccountDAO()
            password = self.accountChangePassword(password)
            res = dao.accountChangePassword(email, password)
            return jsonify(Account=res)
        else:
            return jsonify(Error="Unexpected attributes in changing password request"), 400

    def insertAccount(self, form):
        if len(form) != 7:
            return jsonify(Error="Malformed post request"), 400
        else:
            email = form['email']
            password = form['password']
            is_admin = form['is_admin']
            person_id = form['person_id']
            balance = form['balance']
            bank_account = form['bank_account']
            routing_number = form['routing_number']
            first_name = form['first_name']
            last_name = form['last_name']
            address = form['address']
            city = form['city']
            zip_code = form['zip_code']


            if email and password and is_admin and person_id and balance and bank_account and routing_number \
                and first_name and last_name and address and city and zip_code:
                dao = AccountDAO().insertAccount(person_id, email, password, is_admin, bank_account,routing_number)
                aid = dao.insertAccount(email, password, is_admin, person_id, bank_account, routing_number)
                result = self.build_account_attributes(aid, first_name, last_name, address, city, zip_code)
                return jsonify(Account=result), 201
            else:
                return jsonify(Error="Unexpected attributes in post account"), 400

    def insertAccount_json(self, json):
        email = json['email']
        password = json['password']
        is_admin = json['is_admin']
        person_id = json['person_id']
        balance = json['balance']
        bank_account = json['bank_account']
        routing_number = json['routing_number']
        first_name = json['first_name']
        last_name = json['last_name']
        address = json['address']
        city = json['city']
        zip_code = json['zip_code']

        if email and password and is_admin and person_id and balance and bank_account and routing_number \
                and first_name and last_name and address and city and zip_code:
            dao = AccountDAO().insertAccount(person_id, email, password, is_admin, bank_account, routing_number)
            aid = dao.insertAccount(email, password, is_admin, person_id, bank_account, routing_number)
    
            result = self.build_account_attributes(aid, first_name, last_name, address, city, zip_code)
            return jsonify(Account=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post account"), 400

    def update_balance(self, account_id, balance):
        dao = AccountDAO()
        if not dao.getAccountById(account_id):
            return jsonify(Error="Post not found."), 404
        else:
            dao.updateBalance(account_id, balance)
            row = dao.getAccountById(account_id)
            result = self.build_account_dict(row)
            return jsonify(Account_Balance_Update=result), 200
