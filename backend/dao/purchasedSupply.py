from backend.config.dbconfig import pg_config
import psycopg2


class PurchasedSupplyDAO:
    def __init__(self):

        connection_url = "dbname=%s user=%s password=%s" % (pg_config['dbname'],
                                                            pg_config['user'],
                                                            pg_config['passwd'])
        self.conn = psycopg2._connect(connection_url)

    def getAllPurchasedSupplies(self):
        cursor = self.conn.cursor()
        query = "select purchase_id, supply_id as post, person_id as buyer, category, subcategory, " \
                    "pquantity as quantity, date_purchased "\
                "from PurchasedSupplies natural inner join Supplies natural inner join Resources " \
                    "natural inner join Categories left join Subcategories " \
                "order by date_purchased desc;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getTotalPurchases(self):
        cursor = self.conn.cursor()
        query = "select count(*) " \
                "from PurchasedSupplies;"
        cursor.execute(query)
        result = int(cursor.fetchone())
        return result

    def getTotalPurchasesPerCategory(self):
        cursor = self.conn.cursor()
        query = "select category, subcategory, count(*) " \
                "from PurchasedSupplies natural inner join Supplies natural inner join Resources " \
                    "natural inner join Categories left join Subcategories " \
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
                "from PurchasedSupplies natural inner join Supplies natural inner join Resources " \
                    "natural inner join Categories left join Subcategories " \
                "group by category, subcategory " \
                "order by category, subcategory;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getPurchaseStatisticsPerCategory(self):
        cursor = self.conn.cursor()
        query = "select category, count(*) as total_purchases, sum(pquantity) as total_supplies, " \
                    "max(punit_price) as highest_price, avg(punit_price) as average_price, " \
                    "min(punit_price) as lowest_price " \
                "from PurchasedSupplies natural inner join Supplies natural inner join Resources " \
                    "natural inner join Categories left join Subcategories " \
                "group by category, subcategory " \
                "order by category, subcategory;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getPurchasedSupplyById(self, purchase_id):
        cursor = self.conn.cursor()
        query = "select purchase_id, name, category, subcategory, pquantity as purchased_amount, " \
                    "A.first_name + ' ' + A.last_name as supplier, B.first_name + ' ' + B.last_name as buyer, " \
                    "date_purchased, supplies.address_id " \
                "from PurchasedSupplies natural inner join Supplies natural inner join Resources " \
                    "natural inner join Person as A natural inner join Person as B " \
                "on A.person_id <> B.person_id " \
                "where A.person_id = resources.person_id " \
                "and B.person_id = PurchasedSupplies.person_id " \
                "and purchase_id = %s;"
        cursor.execute(query, (purchase_id,))
        result = cursor.fetchone()
        return result

    def getPurchasedSuppliesByBuyerId(self, person_id):
        cursor = self.conn.cursor()
        query = "select purchase_id, supply_id, category, subcategory, pquantity, date_purchased " \
                "from PurchasedSupplies natural inner join Supplies natural inner join Resources " \
                    "natural inner join Categories left join Subcategories " \
                "where PurchasedSupplies.person_id = %s " \
                "order by date_purchased desc;"
        cursor.execute(query, (person_id,))
        result = cursor.fetchall()
        return result

    def getPurchasedSuppliesBySupplierId(self, person_id):
        cursor = self.conn.cursor()
        query = "select purchase_id, PurchasedSupplies.person_id, category, subcategory, pquantity, date_purchased " \
                "from PurchasedSupplies natural inner join Supplies natural inner join Resources " \
                    "natural inner join Categories left join Subcategories " \
                "where Resources.person_id = %s " \
                "order by date_purchased desc;"
        cursor.execute(query, (person_id,))
        result = cursor.fetchall()
        return result

    def getPurchasedSuppliesBySupplyId(self, supply_id):
        cursor = self.conn.cursor()
        query = "select purchase_id, PurchasedSupplies.person_id, category, subcategory, pquantity, date_purchased " \
                "from PurchasedSupplies natural inner join Supplies natural inner join Resources " \
                    "natural inner join Categories left join Subcategories " \
                "where supply_id = %s " \
                "order by date_purchased desc;"
        cursor.execute(query, (supply_id,))
        result = cursor.fetchall()
        return result

    def insert(self, supply_id, person_id, pquantity, punit_price):
        cursor = self.conn.cursor()

        query = "insert into PurchasedSupplies(supply_id, person_id, pquantity, punit_price) " \
                "values (%s, %s, %s, %s) " \
                "returning purchase_id;"
        cursor.execute(query, (supply_id, person_id, pquantity, punit_price))

        supply_id = cursor.fetchone()[0]

        self.conn.commit()
        return supply_id

    def delete(self, purchase_id):
        cursor = self.conn.cursor()
        query = "delete from PurchasedSupplies " \
                "where purchase_id = %s;"
        cursor.execute(query, (purchase_id,))
        self.conn.commit()
        return purchase_id

    def update(self, supply_id, person_id, pquantity, punit_price):
        cursor = self.conn.cursor()
        query = "update PurchasedSupplies " \
                "set supply_id = %s, person_id = %s, pquantity = %s, punit_price = %s " \
                "where purchase_id = %s;"
        cursor.execute(query, (supply_id, person_id, pquantity, punit_price))
        self.conn.commit()
        return supply_id
