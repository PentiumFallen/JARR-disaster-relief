from flask import jsonify

from backend.dao.account import AccountDAO
from backend.dao.purchasedSupply import PurchasedSupplyDAO
from backend.dao.supply import SupplyDAO
from backend.handler.account import AccountHandler
from backend.handler.supply import SupplyHandler


class PurchasedSupplyHandler:

    def build_all_purchased_supply_dict(self, row):
        result = {
            'purchase_id': row[0],
            'post': row[1],
            'buyer': row[2],
            'category': row[3],
            'subcategory': row[4],
            'quantity': row[5],
            'price_per_unit': row[6],
            'total_price': row[5]*row[6],
            'date_purchased': row[7],
        }
        return result

    def build_purchase_stat_dict(self, row, stat):
        if stat==1:
            result = {
                'category': row[0],
                'subcategory': row[1],
                'amountOfPurchases': row[2],
            }
            return result
        elif stat==2:
            result = {
                'category': row[0],
                'subcategory': row[1],
                'amountOfSupplies': row[2],
            }
            return result
        elif stat==3:
            result = {
                'category': row[0],
                'subcategory': row[1],
                'total_purchases': row[2],
                'total_supplies': row[3],
                'highest_price': row[4],
                'average_price': row[5],
                'lowest_price': row[6],
            }
            return result

    def build_purchase_info_dict(self, row, source):
        if source==1:
            result = {
                'purchase_id': row[0],
                'post_name': row[1],
                'category': row[2],
                'subcategory': row[3],
                'purchased_amount': row[4],
                'total_price': row[5]*row[4],
                'supplier': row[6],
                'buyer': row[7],
                'date_purchased': row[8],
            }
            return result
        elif source==2:
            result = {
                'purchase_id': row[0],
                'supply_id': row[1],
                'category': row[2],
                'subcategory': row[3],
                'purchased_amount': row[4],
                'total_price': row[5]*row[4],
                'date_purchased': row[6],
            }
            return result
        elif source==3:
            result = {
                'purchase_id': row[0],
                'buyer_id': row[1],
                'category': row[2],
                'subcategory': row[3],
                'purchased_amount': row[4],
                'total_price': row[5]*row[4],
                'date_purchased': row[6],
            }
            return result

    def build_purchased_supply_attributes(self, purchase_id, supply_id, person_id, pquantity, punit_price):
        result = {
            'purchase_id': purchase_id,
            'supply_id': supply_id,
            'person_id': person_id,
            'pquantity': pquantity,
            'punit_price': punit_price,
        }
        return result

    def getAllPurchasedSupplies(self):
        dao = PurchasedSupplyDAO()
        purchasedSupply_list = dao.getAllPurchasedSupplies()
        result_list = []
        for row in purchasedSupply_list:
            result = self.build_all_purchased_supply_dict(row)
            result_list.append(result)
        return jsonify(All_Purchased_Supplies=result_list)

    def getTotalPurchases(self):
        dao = PurchasedSupplyDAO()
        amount = dao.getTotalPurchases()
        return jsonify(Total_Purchases=amount)

    def getTotalPurchasesPerCategory(self):
        dao = PurchasedSupplyDAO()
        purchasedSupply_list = dao.getTotalPurchasesPerCategory()
        result_list = []
        for row in purchasedSupply_list:
            result = self.build_purchase_stat_dict(row,1)
            result_list.append(result)
        return jsonify(Purchases_Per_Category=result_list)

    def getTotalSuppliesPurchasedPerCategory(self):
        dao = PurchasedSupplyDAO()
        purchasedSupply_list = dao.getTotalSuppliesPurchasedPerCategory()
        result_list = []
        for row in purchasedSupply_list:
            result = self.build_purchase_stat_dict(row,2)
            result_list.append(result)
        return jsonify(Supplies_Purchased_Per_Category=result_list)

    def getPurchaseStatisticsPerCategory(self):
        dao = PurchasedSupplyDAO()
        purchasedSupply_list = dao.getPurchaseStatisticsPerCategory()
        result_list = []
        for row in purchasedSupply_list:
            result = self.build_purchase_stat_dict(row,3)
            result_list.append(result)
        return jsonify(Supplies_Purchased_Per_Category=result_list)

    def getPurchasedSupplyById(self, pid):
        dao = PurchasedSupplyDAO()
        row = dao.getPurchasedSupplyById(pid)
        result = self.build_purchase_info_dict(row,1)
        return jsonify(Purchase_Info=result)

    def getPurchasedSuppliesByBuyerId(self, bid):
        dao = PurchasedSupplyDAO()
        purchasedSupply_list = dao.getPurchasedSuppliesByBuyerId(bid)
        result_list = []
        for row in purchasedSupply_list:
            result = self.build_purchase_info_dict(row,2)
            result_list.append(result)
        return jsonify(Purchase_Info=result_list)

    def getPurchasedSuppliesBySupplierId(self, sid):
        dao = PurchasedSupplyDAO()
        purchasedSupply_list = dao.getPurchasedSuppliesBySupplierId(sid)
        result_list = []
        for row in purchasedSupply_list:
            result = self.build_purchase_info_dict(row,3)
            result_list.append(result)
        return jsonify(Purchase_Info=result_list)

    def getPurchasedSuppliesBySupplyId(self, sid):
        dao = PurchasedSupplyDAO()
        purchasedSupply_list = dao.getPurchasedSuppliesBySupplyId(sid)
        result_list = []
        for row in purchasedSupply_list:
            result = self.build_purchase_info_dict(row,3)
            result_list.append(result)
        return jsonify(Purchase_Info=result_list)

    def insert_purchasedSupply(self, form):
        if len(form) != 3:
            return jsonify(Error="Malformed post request"), 400
        else:
            dao = PurchasedSupplyDAO()
            supply_id = form['supply_id']
            person_id = form['person_id']
            pquantity = int(form['pquantity'])

            if person_id and supply_id and pquantity:
                supply = SupplyDAO().getSupplyById(supply_id)
                supply = SupplyHandler().build_supply_dict(supply)
                buyerAccountRow = AccountDAO().getAccountByPersonId(person_id)
                buyerAccount = AccountHandler().build_account_dict(buyerAccountRow)
                supplierAccountRow = AccountDAO().getAccountByPersonId(int(supply.get("person_id")))
                supplierAccount = AccountHandler().build_account_dict(supplierAccountRow)
                if supply.get("available") < pquantity:
                    return jsonify(Error="Insufficient stock"), 400
                elif buyerAccount.get("balance") < (pquantity*supply.get("sunit_price")):
                    return jsonify(Error="Insufficient funds"), 400
                else:
                    transactionTotal = pquantity*supply.get("sunit_price")
                    new_available = supply.get("available") - pquantity
                    newBuyerBalance = buyerAccount.get("balance") - transactionTotal
                    newSupplierBalance = supplierAccount.get("balance") + transactionTotal

                    purchasedSupply_id = dao.insert(supply_id, person_id, pquantity, supply.get("sunit_price"))
                    SupplyDAO().updateStock(int(supply.get("supply_id")), new_available)
                    AccountDAO().updateBalance(int(buyerAccount.get("account_id")), newBuyerBalance)
                    AccountDAO().updateBalance(int(supplierAccount.get("account_id")), newSupplierBalance)

                    result = self.build_purchased_supply_attributes(purchasedSupply_id, supply_id, person_id, pquantity, supply.get("sunit_price"))
                    return jsonify(PurchasedSupply=result), 201
            else:
                return jsonify(Error="Unexpected attributes in post request"), 400

    def insert_purchasedSupply_json(self, json):
        dao = PurchasedSupplyDAO()
        supply_id = json['supply_id']
        person_id = json['person_id']
        pquantity = int(json['pquantity'])

        if person_id and supply_id and pquantity:
            supply = SupplyDAO().getSupplyById(supply_id)
            supply = SupplyHandler().build_supply_dict(supply)
            buyerAccountRow = AccountDAO().getAccountByPersonId(person_id)
            buyerAccount = AccountHandler().build_account_dict(buyerAccountRow)
            supplierAccountRow = AccountDAO().getAccountByPersonId(int(supply.get("person_id")))
            supplierAccount = AccountHandler().build_account_dict(supplierAccountRow)
            if supply.get("available") < pquantity:
                return jsonify(Error="Insufficient stock"), 400
            elif buyerAccount.get("balance") < (pquantity * supply.get("sunit_price")):
                return jsonify(Error="Insufficient funds"), 400
            else:
                transactionTotal = pquantity * supply.get("sunit_price")
                new_available = supply.get("available") - pquantity
                newBuyerBalance = buyerAccount.get("balance") - transactionTotal
                newSupplierBalance = supplierAccount.get("balance") + transactionTotal

                purchasedSupply_id = dao.insert(supply_id, person_id, pquantity, supply.get("sunit_price"))
                SupplyDAO().updateStock(int(supply.get("supply_id")), new_available)
                AccountDAO().updateBalance(int(buyerAccount.get("account_id")), newBuyerBalance)
                AccountDAO().updateBalance(int(supplierAccount.get("account_id")), newSupplierBalance)

                result = self.build_purchased_supply_attributes(purchasedSupply_id, supply_id, person_id, pquantity,
                                                                supply.get("sunit_price"))
                return jsonify(PurchasedSupply=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request"), 400

    def delete_purchasedSupply(self, purchasedSupply_id):
        dao = PurchasedSupplyDAO()
        if not dao.getPurchasedSupplyById(purchasedSupply_id):
            return jsonify(Error="Post not found."), 404
        else:
            dao.delete(purchasedSupply_id)
        return jsonify(DeleteStatus="OK"), 200

    def update_purchasedSupply(self, purchasedSupply_id, unitprice, quantity):
        dao = PurchasedSupplyDAO()
        if not dao.getPurchasedSupplyById(purchasedSupply_id):
            return jsonify(Error="Post not found."), 404
        else:
                if int(quantity) <= 0:
                    return jsonify(Error="Cannot put non-positive value in quantity"), 400
                else:
                    dao.update(purchasedSupply_id, unitprice, quantity)
                    row = dao.getPurchasedSupplyById(purchasedSupply_id)
                    result = self.build_all_purchased_supply_dict(row)
                    return jsonify(Part=result), 200
