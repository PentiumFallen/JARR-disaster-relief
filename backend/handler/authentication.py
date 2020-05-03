from flask import jsonify
from backend.dao.authentication import AuthenticationDAO

class AuthenticationHandler:
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

    def getAccountData(self, email, password):
        dao = AuthenticationDAO()
        result = dao.getAccountData
        return jsonify(Account=result)
        if not result:
            return jsonify(Error='Account not found.'), 404
        else:
            res = self.build_account_(result)
            return jsonify(Account=res), 200

    def getAccountType(self, account_id):
        dao = AuthenticationDAO()
        result = dao.getAccountType
        return jsonify(is_admin=result), 200

    def delete_account(self, account_id):
        dao = AuthenticationDAO()
        if not dao.getAllAuthenticationByEmail:
            return jsonify(Error = "Account not found."), 404
        else:
            dao.deleteAccount(account_id)
        return jsonify(DeleteStatus="OK"), 200

    def accountLogin(self, form):
        email = form.get('email')
        password = form.get('password')
        
        if password and email:
            dao = AuthenticationDAO()
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
            dao = AuthenticationDAO()
            password = self.hash_password(password)
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
            is_admin = form['is_admin']
            if email and password and is_admin:
                # dao = AuthenticationDAO()
                # pid = dao.insertAccount(email, password, is_admin)
                # result = build_account_attributes(pid, email, password, is_admin)
                result = 'Insert works!'
                return jsonify(Request=result), 201
            else:
                return jsonify(Error="Unexpected attributes in post account"), 400

    def insertAccount_json(self, json):
        email = json['email']
        password = json['password']
        is_admin = json['is_admin']
        if email and password and is_admin:
            # dao = AuthenticationDAO()
            # pid = dao.insertAccount(email, password, is_admin)
            # result = self.build_account_attributes(pid, email, password, is_admin)
            return jsonify(Request="Insert account json works!"), 201
        else:
            return jsonify(Error="Unexpected attributes in post account"), 400
        