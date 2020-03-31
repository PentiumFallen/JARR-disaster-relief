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


    def get_all_authentication(self):
        # dao = AuthenticationDAO()
        # result_list = dao.getAllAuthentication()
        account = ['Get all accounts works!']
        # for row in result_list:
        #     result = self.build_person_dict(row)
        #     result_list.append(result)
        return jsonify(Account=account)
    
    def get_authentication_by_id(self, account_id):
        # dao = AuthenticationDAO()
        # row = dao.getAuthenticationById()
        # if not row:
        #     return jsonify(Error = "Account Not Found"), 404
        # else:
        #     account = self.build_account_dict(row)
        return jsonify(Account='Account by account_id')

    def get_authentication_by_person_id(self, person_id):
        # dao = AuthenticationDAO()
        # row = dao.getAuthenticationByPersonId(person_id)
        # if not row:
        #     return jsonify(Error = "Account Not Found"), 404
        # else:
        #     account = self.build_account_dict(row)
        return jsonify(Account='Account by person_id')

    def get_authentication_by_request_id(self, request_id):
        # dao = AuthenticationDAO()
        # row = dao.getAuthenticationByRequestId(request_id)
        # if not row:
        #     return jsonify(Error = "Account Not Found"), 404
        # else:
        #     account = self.build_person_dict(row)
        return jsonify(Person='Account by request_id')

    def get_authentication_by_supply_id(self, supply_id):
        # dao = AuthenticationDAO()
        # row = dao.getAuthenticationBySupplyId(supply_id)
        # if not row:
        #     return jsonify(Error = "Account Not Found"), 404
        # else:
        #     account = self.build_account_dict(row)
        return jsonify(Account='Account by supply_id')

    def insert_account(self, form):
        # if len(form) != 5:
        #     return jsonify(Error="Malformed post request"), 400
        # else:
        #     email = form['email']
        #     password = form['password']
        #     is_admin = form['is_admin']
        #     if email and password and is_admin:
        #         dao = AuthenticationDAO()
        #         aid = dao.insertAccount(email, password, is_admin)
        #         result = self.build_account_attributes(aid, email, password, is_admin)
        #         return jsonify(Account='Insert account (form)!')
        #     else:
        #         return jsonify(Error="Unexpected attributes in post request"), 400
        return jsonify(Account='Insert account (form)!')

    def insert_account_json(self, json):
        # email = json['email']
        # password = json['password']
        # is_admin = json['is_admin']
        # if email and password and is_admin:
        #     dao = AuthenticationDAO()
        #     aid = dao.insert(email, password, is_admin)
        #     result = self.build_account_attributes(aid, email, password, is_admin)
        #     return jsonify(Account="Insert account (json)!"), 201
        # else:
        #     return jsonify(Error="Unexpected attributes in post request"), 400
        return jsonify(Account="Insert account (json)!"), 201

    def delete_account(self, account_id):
        # dao = AuthenticationDAO()
        # if not dao.getAuthenticationById(account_id):
        #     return jsonify(Error = "Account not found."), 404
        # else:
        #     dao.delete(account_id)
        return jsonify(DeleteStatus="OK"), 200

    def update_account(self, account_id, form):
        # dao = AuthenticationDAO()
        # if not dao.getAuthenticationById(account_id):
        #     return jsonify(Error="Account not found."), 404
        # else:
        #     if len(form) != 5:
        #         return jsonify(Error="Malformed update request"), 400
        #     else:
        #         email = form['email']
        #         password = form['password']
        #         is_admin = form['is_admin']
        #         if email and password and is_admin and account_id:
        #             aid = dao.updateAccount(email, password, is_admin, account_id)
        #             result = self.build_account_attributes(self, email, password, is_admin,)
        #             return jsonify(Account='Update account (form)!')
        #         else:
        #             return jsonify(Error="Unexpected attributes in update request"), 400
        return jsonify(Account='Update account (form)!')


