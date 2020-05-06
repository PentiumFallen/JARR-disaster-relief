from flask import jsonify
from backend.dao.account import AccountDAO

class AccountHandler:
    def build_account_dict(self, row):
        result = {
            'account_id': row[0],
            'email': row[1],
            'password': row[2],
            'registered_date': row[3],
            'is_admin': row[4],
            'person_id': row[5],
            'balance': row[6],
            'bank_account_number': row[7],
            'routing_number': row[8],
        }
        return result

    def build_account_attributes(self, account_id, email, password, registered_date, is_admin, person_id, 
                                 balance, bank_account_number, routing_number):
        result = {
            'account_id': account_id,
            'email': email,
            'password': password,
            'registered_date': registered_date,
            'is_admin': is_admin,
            'person_id': person_id,
            'balance': balance,
            'bank_account_number': bank_account_number,
            'routing_number': routing_number,
        }
        return result

    def get_account_data(self, email, password):
        dao = AccountDAO()
        result = dao.getAccountData()
        if not result:
            return jsonify(Error='Account not found.'), 404
        else:
            res = self.build_account_dict(result)
            return jsonify(Account=res), 200

    
    def get_admin_account(self, is_admin):
        dao = AccountDAO()
        result = dao.getAdminAccount()
        if not result:
            return jsonify(Error='Admins accounts not found.'), 404
        else:
            res = self.build_account_dict(result)
            return jsonify(Account=res), 200

    def get_account_type(self, account_id):
        dao = AccountDAO()
        result = dao.getAccountType()
        return jsonify(is_admin=result), 200

    def delete_account(self, account_id):
        dao = AccountDAO()
        if not dao.getAllAuthenticationByEmail:
            return jsonify(Error = "Account not found."), 404
        else:
            dao.deleteAccount(account_id)
        return jsonify(DeleteStatus="OK"), 200

    def accountLogin(self, form):
        email = form.get('email')
        password = form.get('password')
        
        if password and email:
            dao = AccountDAO()
            password = self.hash_password(password)
            res = dao.accountLogin(email,password)
            if len(res)==0:
                return jsonify(Error = "No account found with that email or Password"),404
            else:
                result_list = []
            for row in res:
                result = self.build_login(row)
                result_list.append(result)            
                return jsonify(Account = result_list)       
        else:
            return jsonify(Error="Unexpected attributes in Login request"), 400

    def accountChangePassword(self, form):
        email = form.get('email')
        password = form.get('password')        
        if password and email and (len(form)==2):
            dao = AccountDAO()
            password = self.accountChangePassword(password)
            res = dao.accountChangePassword(email,password) 
            return jsonify(Account = res)        
        else:
            return jsonify(Error="Unexpected attributes in changing password request"), 400

    def insertAccount(self, form):
        if len(form) != 5:
            return jsonify(Error="Malformed post request"), 400
        else:
            email = form['email']
            password = form['password']
            registered_date = form['registered_id']
            is_admin = form['is_admin']
            person_id = form['person_id']
            balance = form['balance']
            bank_account = form['bank_account']
            routing_number = form['routing_number']

            if email and password and registered_date and is_admin and person_id and balance and bank_account and routing_number:
                dao = AccountDAO()
                pid = dao.insertAccount(email, password, registered_date, is_admin, person_id, balance, bank_account, routing_number)
                result = build_account_attributes(pid, email, password, registered_date, is_admin, person_id, balance, bank_account, routing_number)
                result = 'Account created!'
                return jsonify(Account=result), 201
            else:
                return jsonify(Error="Unexpected attributes in post account"), 400

    def insertAccount_json(self, json):
        email = json['email']
        password = json['password']
        registered_date = json['registered_date']
        is_admin = json['is_admin'] 
        person_id = json['person_id']
        balance = json['balance']
        bank_account = json['bank_account']
        routing_number = json['routing_number']

        if email and password and registered_date and is_admin and person_id and balance and bank_account and routing_number:
            dao = AccountDAO()
            pid = dao.insertAccount(email, password, registered_date, is_admin, person_id, balance, bank_account, routing_number)
            result = self.build_account_attributes(pid, email, password, registered_date, is_admin, person_id, balance, bank_account, routing_number)
            return jsonify(Account=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post account"), 400