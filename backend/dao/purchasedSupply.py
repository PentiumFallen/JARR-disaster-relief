from backend.config.dbconfig import pg_config
import psycopg2


class PurchasedSupplyDAO:
    def __init__(self):

        connection_url = "dbname=%s user=%s password=%s host=%s" % (pg_config['dbname'],
                                                                    pg_config['user'],
                                                                    pg_config['passwd'],
                                                                    pg_config['host'])
        self.conn = psycopg2._connect(connection_url)

    def getAllPurchasedSupplies(self):
        cursor = self.conn.cursor()
        query = "select purchase_id, supply_id as post, person_id as buyer, category, subcategory, " \
                "pquantity as quantity, punit_price, date_purchased "\
                "from \"PurchasedSupplies\" natural inner join \"Supplies\" natural inner join \"Resources\" as R " \
                "natural inner join \"Categories\" as cat left join \"Subcategories\" as subcat " \
                "on subcat.subcategory_id = cat.subcategory_id " \
                "order by date_purchased desc;"
        cursor.execute(query)
        result = cursor.fetchall()
        return result

    def getTotalPurchases(self):
        cursor = self.conn.cursor()
        query = "select count(*) " \
                "from \"PurchasedSupplies\";"
        cursor.execute(query)
        result = int(cursor.fetchone())
        return result

    def getTotalPurchasesPerCategory(self):
        cursor = self.conn.cursor()
        query = "select category, subcategory, count(*) " \
                "from \"PurchasedSupplies\" natural inner join \"Supplies\" natural inner join \"Resources\" as R " \
                "natural inner join \"Categories\" as cat left join \"Subcategories\" as subcat " \
                "on subcat.subcategory_id = cat.subcategory_id " \
                "group by category, subcategory " \
                "order by category, subcategory;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getTotalSuppliesPurchasedPerCategory(self):
        cursor = self.conn.cursor()
        query = "select category, subcategory, sum(pquantity) as total_supplies " \
                "from \"PurchasedSupplies\" natural inner join \"Supplies\" natural inner join \"Resources\" " \
                "natural inner join \"Categories\" as cat left join \"Subcategories\" as subcat " \
                "on subcat.subcategory_id = cat.subcategory_id " \
                "group by category, subcategory " \
                "order by category, subcategory;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getPurchaseStatisticsPerCategory(self):
        cursor = self.conn.cursor()
        query = "select category, subcategory, count(*) as total_purchases, sum(pquantity) as total_supplies, " \
                "max(punit_price) as highest_price, avg(punit_price) as average_price, " \
                "min(punit_price) as lowest_price " \
                "from \"PurchasedSupplies\" natural inner join \"Supplies\" natural inner join \"Resources\" " \
                "natural inner join \"Categories\" as cat left join \"Subcategories\" as subcat " \
                "on subcat.subcategory_id = cat.subcategory_id " \
                "group by category, subcategory " \
                "order by category, subcategory;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getPurchasedSupplyById(self, purchase_id):
        cursor = self.conn.cursor()
        query = "select purchase_id, R.name, category, subcategory, pquantity as purchased_amount, punit_price, " \
                "concat(A.first_name,' ',A.last_name) as supplier, concat(B.first_name,' ',B.last_name) as buyer, " \
                "date_purchased " \
                "from \"PurchasedSupplies\" as PS natural inner join \"Supplies\" natural inner join \"Resources\" as R " \
                "natural inner join \"Persons\" as A natural inner join \"Persons\" as B " \
                "natural inner join \"Categories\" as cat left join \"Subcategories\" as subcat " \
                "on subcat.subcategory_id = cat.subcategory_id " \
                "where A.person_id = R.person_id " \
                "and B.person_id = PS.person_id " \
                "and purchase_id = %s;"

        query2 = "with sup as (select person_id as sperson_id, first_name as sfirst_name, last_name as slast_name from \"Persons\"), " \
                 "buy as (select person_id as bperson_id, first_name as bfirst_name, last_name as blast_name from \"Persons\") " \
                 "select purchase_id, R.name, category, subcategory, pquantity as purchased_amount, punit_price, " \
                 "concat(sfirst_name, ' ', slast_name) as supplier, concat(bfirst_name, ' ', blast_name) as buyer, " \
                 "date_purchased " \
                 "from buy inner join \"PurchasedSupplies\" as PS on buy.bperson_id = PS.person_id natural inner join \"Supplies\" " \
                 "natural inner join \"Resources\" as R inner join sup on R.person_id = sup.sperson_id natural inner join " \
                 "\"Categories\" as C left join \"Subcategories\" as S on C.subcategory_id = S.subcategory_id " \
                 "where purchase_id = %s;"
        cursor.execute(query2, (purchase_id,))
        result = cursor.fetchone()
        return result

    def getPurchasedSuppliesByBuyerId(self, person_id):
        cursor = self.conn.cursor()
        query = "select purchase_id, supply_id, category, subcategory, pquantity, punit_price, date_purchased " \
                "from \"PurchasedSupplies\" as PS natural inner join \"Supplies\" natural inner join \"Resources\" " \
                "natural inner join \"Categories\" as cat left join \"Subcategories\" as subcat " \
                "on subcat.subcategory_id = cat.subcategory_id " \
                "where PS.person_id = %s " \
                "order by date_purchased desc;"
        cursor.execute(query, (person_id,))
        result = cursor.fetchall()
        return result

    def getPurchasedSuppliesBySupplierId(self, person_id):
        cursor = self.conn.cursor()
        query = "select purchase_id, PS.person_id, category, subcategory, pquantity, punit_price, date_purchased " \
                "from \"PurchasedSupplies\" as PS natural inner join \"Supplies\" natural inner join \"Resources\" as R " \
                "natural inner join \"Categories\" as cat left join \"Subcategories\" as subcat " \
                "on subcat.subcategory_id = cat.subcategory_id " \
                "where R.person_id = %s " \
                "order by date_purchased desc;"
        cursor.execute(query, (person_id,))
        result = cursor.fetchall()
        return result

    def getPurchasedSuppliesBySupplyId(self, supply_id):
        cursor = self.conn.cursor()
        query = "select purchase_id, PS.person_id, category, subcategory, pquantity, punit_price, date_purchased " \
                "from \"PurchasedSupplies\" as PS natural inner join \"Supplies\" natural inner join \"Resources\" " \
                "natural inner join \"Categories\" as cat left join \"Subcategories\" as subcat " \
                "on subcat.subcategory_id = cat.subcategory_id " \
                "where supply_id = %s " \
                "order by date_purchased desc;"
        cursor.execute(query, (supply_id,))
        result = cursor.fetchall()
        return result

    def insert(self, supply_id, person_id, pquantity, punit_price):
        cursor = self.conn.cursor()

        query = "insert into \"PurchasedSupplies\"(supply_id, person_id, pquantity, punit_price) " \
                "values (%s, %s, %s, %s) " \
                "returning purchase_id;"
        cursor.execute(query, (supply_id, person_id, pquantity, punit_price))

        purchase_id = cursor.fetchone()[0]

        self.conn.commit()
        return purchase_id

    def delete(self, purchase_id):
        cursor = self.conn.cursor()
        query = "delete from \"PurchasedSupplies\" " \
                "where purchase_id = %s;"
        cursor.execute(query, (purchase_id,))
        self.conn.commit()
        return purchase_id

    def update(self, purchase_id, pquantity, punit_price):
        cursor = self.conn.cursor()
        query = "update \"PurchasedSupplies\" " \
                "set pquantity = %s, punit_price = %s " \
                "where purchase_id = %s;"
        cursor.execute(query, (pquantity, punit_price, purchase_id))
        self.conn.commit()
        return purchase_id
