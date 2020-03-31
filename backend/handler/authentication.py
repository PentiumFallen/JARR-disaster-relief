from flask import jsonify
from backend.dao import PersonDAO

class AuthenticationHandler:
    def build_account_dict(self, row):
        result = {
            'account_id': row[0],
            'email': row[1],
            'password': row[2],
            'is_admin': row[3],
        }
        return result

    def build_account_attributes(self, account_id, email, password, is_admin):
        result = {
            'account_id': account_id,
            'email': email,
            'password': password,
            'is_admin': is_admin,
        }
        return result

    def getAccountData(self, email, password):
        #dao = AuthenticationDAO()
        #result = dao.getAccountData(email, password)
        return jsonify(Account=['Get all data account works!'])
        """
        if not result:
            return jsonify(Error='Account not found.'), 404
        else:
            prof = self.build_account_(result)
            return jsonify(Account=prof), 200
        """

    def getAccountType(self, account_id):
        #dao = AuthenticationDAO()
        #result = dao.getAccountType(account_id)
        return jsonify(is_admin="YES"), 200

    def delete_account(self, account_id):
        # dao = AuthenticationDAO()
        # if not dao.getAllAuthenticationByEmail(account_id):
        #     return jsonify(Error = "Account not found."), 404
        # else:
        #     dao.deleteAccount(account_id)
        return jsonify(DeleteStatus="OK"), 200

    def accountLogin(self, form):
        #email = form.get('email')
        #password = form.get('password')
        
       # if password and email:
            #dao = AuthenticationDAO()
           #password = self.hash_password(password)
            #res = dao.accountLogin(email,password)
            #if len(res)==0:
                #return jsonify(Error = "No account found with that email or Password " ),404
            #else:
                #result_list = []
            #for row in res:
                #result = self.build_login(row)
                #result_list.append(result)            
                #return jsonify(Account = result_list)       
        #else:
            return jsonify(Error="Unexpected attributes in Login request"), 400

    def accountChangePassword(self, form):
        #email = form.get('email')
        #password = form.get('password')        
        #if password and email and (len(form)==2):
            #dao = AuthenticationDAO()
            #password = self.hash_password(password)
            #res = dao.accountChangePassword(email,password) 
            #return jsonify(Account = res)        
            
        #else:
            return jsonify(Error="Unexpected attributes in Login request"), 400

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
        