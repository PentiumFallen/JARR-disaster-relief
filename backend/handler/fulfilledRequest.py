from flask import jsonify

from backend.dao.account import AccountDAO
from backend.dao.person import PersonDAO
from backend.dao.fulfilledRequest import FulfilledRequestDAO
from backend.dao.request import RequestDAO



class FulfilledRequestHandler:

    def build_all_fulfilled_request_dict(self, row):
        result = {
            'fulfillment_id': row[0],
            'post': row[1],
            'seller': row[2],
            'category': row[3],
            'subcategory': row[4],
            'quantity': row[5],
            'price_per_unit': row[6],
            'total_price': row[5]*row[6],
            'date_fulfilled': row[7],
        }
        return result

    def build_fulfillment_stat_dict(self, row, stat):
        if stat==1:
            result = {
                'category': row[0],
                'subcategory': row[1],
                'amountOfFulfillments': row[2],
            }
            return result
        elif stat==2:
            result = {
                'category': row[0],
                'subcategory': row[1],
                'amountOfRequests': row[2],
            }
            return result
        elif stat==3:
            result = {
                'category': row[0],
                'subcategory': row[1],
                'total_fulfillments': row[2],
                'total_requests': row[3],
                'highest_price': row[4],
                'average_price': row[5],
                'lowest_price': row[6],
            }
            return result

    def build_fulfillment_info_dict(self, row, source):
        if source==1:
            result = {
                'fulfillment_id': row[0],
                'post_name': row[1],
                'category': row[2],
                'subcategory': row[3],
                'fulfilled_amount': row[4],
                'total_price': row[5]*row[4],
                'buyer': row[6],
                'seller': row[7],
                'date_fulfilled': row[8],
            }
            return result
        elif source==2:
            result = {
                'fulfillment_id': row[0],
                'request_id': row[1],
                'category': row[2],
                'subcategory': row[3],
                'fulfilled_amount': row[4],
                'total_price': row[5]*row[4],
                'date_fulfilled': row[6],
            }
            return result
        elif source==3:
            result = {
                'fulfillment_id': row[0],
                'seller_id': row[1],
                'category': row[2],
                'subcategory': row[3],
                'fulfilled_amount': row[4],
                'total_price': row[5]*row[4],
                'date_fulfilled': row[6],
            }
            return result

    def build_fulfilled_request_attributes(self, fulfillmentid, request_id, person_id, fquantity, funit_price):
        result = {
            'fulfillment_id': fulfillmentid,
            'request_id': request_id,
            'person_id': person_id,
            'fquantity': fquantity,
            'funit_price': funit_price,
        }
        return result

    def getAllFulfilledRequests(self):
        dao = FulfilledRequestDAO()
        fulfilledRequest_list = dao.getAllFulfilledRequests()
        result_list = []
        for row in fulfilledRequest_list:
            result = self.build_all_fulfilled_request_dict(row)
            result_list.append(result)
        return jsonify(All_Fulfilled_Requests=result_list)

    def getTotalFulfillments(self):
        dao = FulfilledRequestDAO()
        amount = dao.getTotalFulfillments()
        return jsonify(Total_Fulfillments=amount)

    def getTotalFulfillmentsPerCategory(self):
        dao = FulfilledRequestDAO()
        fulfilledRequest_list = dao.getTotalFulfillmentsPerCategory()
        result_list = []
        for row in fulfilledRequest_list:
            result = self.build_fulfillment_stat_dict(row,1)
            result_list.append(result)
        return jsonify(Fulfillments_Per_Category=result_list)

    def getTotalRequestsFulfulliedPerCategory(self):
        dao = FulfilledRequestDAO()
        fulfilledRequest_list = dao.getTotalRequestsFulfilledPerCategory()
        result_list = []
        for row in fulfilledRequest_list:
            result = self.build_fulfillment_stat_dict(row,2)
            result_list.append(result)
        return jsonify(Requests_Fulfullied_Per_Category=result_list)

    def getFulfillmentStatisticsPerCategory(self):
        dao = FulfilledRequestDAO()
        fulfilledRequest_list = dao.getFulfillmentStatisticsPerCategory()
        result_list = []
        for row in fulfilledRequest_list:
            result = self.build_fulfillment_stat_dict(row,3)
            result_list.append(result)
        return jsonify(Requests_Fulfullied_Per_Category=result_list)

    def getFulfilledRequestById(self, pid):
        dao = FulfilledRequestDAO()
        row = dao.getFulfilledRequestById(pid)
        result = self.build_fulfillment_info_dict(row,1)
        return jsonify(Fulfillment_Info=result)

    def getFulfilledRequestsByBuyerId(self, bid):
        dao = FulfilledRequestDAO()
        fulfilledRequest_list = dao.getFulfilledRequestsByBuyerId(bid)
        result_list = []
        for row in fulfilledRequest_list:
            result = self.build_fulfillment_info_dict(row,2)
            result_list.append(result)
        return jsonify(Fulfillment_Info=result_list)

    def getFulfilledRequestsBySellerId(self, sid):
        dao = FulfilledRequestDAO()
        fulfilledRequest_list = dao.getFulfilledRequestsBySellerId(sid)
        result_list = []
        for row in fulfilledRequest_list:
            result = self.build_fulfillment_info_dict(row,3)
            result_list.append(result)
        return jsonify(Fulfillment_Info=result_list)

    def getFulfilledRequestsByRequestId(self, sid):
        dao = FulfilledRequestDAO()
        fulfilledRequest_list = dao.getFulfilledRequestsByRequestId(sid)
        result_list = []
        for row in fulfilledRequest_list:
            result = self.build_fulfillment_info_dict(row,3)
            result_list.append(result)
        return jsonify(Fulfillment_Info=result_list)

    def insert_fulfilledRequest(self, form):
        if len(form) != 3:
            return jsonify(Error="Malformed post request"), 400
        else:
            dao = FulfilledRequestDAO()
            request_id = form['request_id']
            person_id = form['person_id']
            fquantity = form['fquantity']

            if person_id and request_id and fquantity:
                request = RequestDAO().getRequestById(request_id)
                sellerAccount = AccountDAO().getAccountByPersonId(person_id)
                buyerAccount = AccountDAO().getAccountByPersonId(request[3])
                if request[8] < fquantity:
                    return jsonify(Error="Resource overflow"), 400
                elif buyerAccount[5] < (fquantity*request[9]):
                    return jsonify(Error="Insufficient funds"), 400
                else:
                    transactionTotal = fquantity*request[9]
                    new_available = request[8] - fquantity
                    newSellerBalance = sellerAccount[5] + transactionTotal
                    newBuyerBalance = buyerAccount[5] - transactionTotal

                    fulfilledRequest_id = dao.insert(request_id, person_id, fquantity, request[9])
                    RequestDAO().updateStock(request[0], new_available)
                    AccountDAO().updateBalance(sellerAccount[0], newSellerBalance)
                    AccountDAO().updateBalance(buyerAccount[0], newBuyerBalance)

                    result = self.build_fulfilled_request_attributes(fulfilledRequest_id, request_id, person_id, fquantity, request[9])
                    return jsonify(FulfilledRequest=result), 201
            else:
                return jsonify(Error="Unexpected attributes in post request"), 400

    def insert_fulfilledRequest_json(self, json):
        dao = FulfilledRequestDAO()
        request_id = json['request_id']
        person_id = json['person_id']
        fquantity = json['fquantity']

        if person_id and request_id and fquantity:
            request = RequestDAO().getRequestById(request_id)
            sellerAccount = AccountDAO().getAccountByPersonId(person_id)
            buyerAccount = AccountDAO().getAccountByPersonId(request[3])
            if request[8] < fquantity:
                return jsonify(Error="Resource overflow"), 400
            elif buyerAccount[5] < (fquantity * request[9]):
                return jsonify(Error="Insufficient funds"), 400
            else:
                transactionTotal = fquantity * request[9]
                new_available = request[8] - fquantity
                newSellerBalance = sellerAccount[5] + transactionTotal
                newBuyerBalance = buyerAccount[5] - transactionTotal

                fulfilledRequest_id = dao.insert(request_id, person_id, fquantity, request[9])
                RequestDAO().updateStock(request[0], new_available)
                AccountDAO().updateBalance(sellerAccount[0], newSellerBalance)
                AccountDAO().updateBalance(buyerAccount[0], newBuyerBalance)

                result = self.build_fulfilled_request_attributes(fulfilledRequest_id, request_id, person_id, fquantity,
                                                                 request[9])
                return jsonify(FulfilledRequest=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request"), 400

    def delete_fulfilledRequest(self, fulfilledRequest_id):
        dao = FulfilledRequestDAO()
        if not dao.getFulfilledRequestById(fulfilledRequest_id):
            return jsonify(Error="Post not found."), 404
        else:
            dao.delete(fulfilledRequest_id)
        return jsonify(DeleteStatus="OK"), 200

    def update_fulfilledRequest(self, fulfilledRequest_id, unitprice, quantity):
        dao = FulfilledRequestDAO()
        if not dao.getFulfilledRequestById(fulfilledRequest_id):
            return jsonify(Error="Post not found."), 404
        else:
                if int(quantity) <= 0:
                    return jsonify(Error="Cannot put non-positive value in quantity"), 400
                else:
                    dao.update(fulfilledRequest_id, unitprice, quantity)
                    row = dao.getFulfilledRequestById(fulfilledRequest_id)
                    result = self.build_all_fulfilled_request_dict(row)
                    return jsonify(Part=result), 200
