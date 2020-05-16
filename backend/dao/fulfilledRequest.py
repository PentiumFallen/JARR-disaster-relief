from backend.config.dbconfig import pg_config
import psycopg2


class FulfilledRequestDAO:
    def __init__(self):

        connection_url = "dbname=%s user=%s password=%s host=%s" % (pg_config['dbname'],
                                                                    pg_config['user'],
                                                                    pg_config['passwd'],
                                                                    pg_config['host'])
        self.conn = psycopg2._connect(connection_url)

    def getAllFulfilledRequests(self):
        cursor = self.conn.cursor()
        query = "select fulfillment_id, request_id as post, person_id as seller, category, subcategory, " \
                    "fquantity as quantity, funit_price, date_fulfilled "\
                "from \"FulfilledRequests\" natural inner join \"Requests\" natural inner join \"Resources\" " \
                    "natural inner join \"Categories\" as cat left join \"Subcategories\" as subcat " \
                "on subcat.subcategory_id = cat.subcategory_id " \
                "order by date_fulfilled desc;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getTotalFulfillments(self):
        cursor = self.conn.cursor()
        query = "select count(*) " \
                "from \"FulfilledRequests\";"
        cursor.execute(query)
        result = int(cursor.fetchone())
        return result

    def getTotalFulfillmentsPerCategory(self):
        cursor = self.conn.cursor()
        query = "select category, subcategory, count(*) " \
                "from \"FulfilledRequests\" natural inner join \"Requests\" natural inner join \"Resources\" " \
                    "natural inner join \"Categories\" as cat left join \"Subcategories\" as subcat " \
                "on subcat.subcategory_id = cat.subcategory_id " \
                "group by category, subcategory " \
                "order by category, subcategory;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getTotalRequestsFulfilledPerCategory(self):
        cursor = self.conn.cursor()
        query = "select category, subcategory, sum(fquantity) as total_requests " \
                "from \"FulfilledRequests\" natural inner join \"Requests\" natural inner join \"Resources\" " \
                    "natural inner join \"Categories\" as cat left join \"Subcategories\" as subcat " \
                "on subcat.subcategory_id = cat.subcategory_id " \
                "group by category, subcategory " \
                "order by category, subcategory;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getFulfillmentStatisticsPerCategory(self):
        cursor = self.conn.cursor()
        query = "select category, subcategory, count(*) as total_fulfillments, sum(fquantity) as total_requests, " \
                    "max(funit_price) as highest_price, avg(funit_price) as average_price, " \
                    "min(funit_price) as lowest_price " \
                "from \"FulfilledRequests\" natural inner join \"Requests\" natural inner join \"Resources\" " \
                    "natural inner join \"Categories\" as cat left join \"Subcategories\" as subcat " \
                "on subcat.subcategory_id = cat.subcategory_id " \
                "group by category, subcategory " \
                "order by category, subcategory;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getFulfilledRequestById(self, fulfillment_id):
        cursor = self.conn.cursor()
        query = "select fulfillment_id, name, category, subcategory, fquantity as fulfilled_amount, funit_price " \
                    "concat(A.first_name,' ',A.last_name) as buyer, concat(B.first_name,' ',B.last_name) as seller, " \
                    "date_fulfilled " \
                "from \"FulfilledRequests\" as FR natural inner join \"Requests\" natural inner join \"Resources\" as R " \
                    "natural inner join \"Persons\" as A natural inner join \"Persons\" as B " \
                    "natural inner join \"Categories\" left join \"Subcategories\" " \
                "on A.person_id <> B.person_id " \
                "where A.person_id = R.person_id " \
                "and B.person_id = FR.person_id " \
                "and fulfillment_id = %s;"
        query2 = "with req as (select person_id as sperson_id, first_name as sfirst_name, last_name as slast_name from \"Persons\"), " \
                 "sell as (select person_id as bperson_id, first_name as bfirst_name, last_name as blast_name from \"Persons\") " \
                 "select fulfillment_id, R.name, category, subcategory, fquantity as purchased_amount, funit_price, " \
                 "concat(sfirst_name, ' ', slast_name) as requester, concat(bfirst_name, ' ', blast_name) as seller, " \
                 "date_purchased " \
                 "from sell inner join \"PurchasedSupplies\" as PS on sell.bperson_id = PS.person_id natural inner join \"Supplies\" " \
                 "natural inner join \"Resources\" as R inner join req on R.person_id = req.sperson_id natural inner join " \
                 "\"Categories\" as C left join \"Subcategories\" as S on C.subcategory_id = S.subcategory_id " \
                 "where purchase_id = %s;"
        cursor.execute(query2, (fulfillment_id,))
        result = cursor.fetchone()
        return result

    def getFulfilledRequestsBySellerId(self, person_id):
        cursor = self.conn.cursor()
        query = "select fulfillment_id, request_id, category, subcategory, fquantity, funit_price, date_fulfilled " \
                "from \"FulfilledRequests\" as FR natural inner join \"Requests\" natural inner join \"Resources\" " \
                    "natural inner join \"Categories\" as cat left join \"Subcategories\" as subcat " \
                "on subcat.subcategory_id = cat.subcategory_id " \
                "where FR.person_id = %s " \
                "order by date_fulfilled desc;"
        cursor.execute(query, (person_id,))
        result = cursor.fetchall()
        return result

    def getFulfilledRequestsByBuyerId(self, person_id):
        cursor = self.conn.cursor()
        query = "select fulfillment_id, FR.person_id, category, subcategory, fquantity, funit_price, date_fulfilled " \
                "from \"FulfilledRequests\" as FR natural inner join \"Requests\" natural inner join \"Resources\" as R " \
                    "natural inner join \"Categories\" as cat left join \"Subcategories\" as subcat " \
                "on subcat.subcategory_id = cat.subcategory_id " \
                "where R.person_id = %s " \
                "order by date_fulfilled desc;"
        cursor.execute(query, (person_id,))
        result = cursor.fetchall()
        return result

    def getFulfilledRequestsByRequestId(self, request_id):
        cursor = self.conn.cursor()
        query = "select fulfillment_id, FR.person_id, category, subcategory, fquantity, funit_price, date_fulfilled " \
                "from \"FulfilledRequests\" as FR natural inner join \"Requests\" natural inner join \"Resources\" " \
                    "natural inner join \"Categories\" as cat left join \"Subcategories\" as subcat " \
                "on subcat.subcategory_id = cat.subcategory_id " \
                "where request_id = %s " \
                "order by date_fulfilled desc;"
        cursor.execute(query, (request_id,))
        result = cursor.fetchall()
        return result

    def insert(self, request_id, person_id, fquantity, funit_price):
        cursor = self.conn.cursor()

        query = "insert into \"FulfilledRequests\"(request_id, person_id, fquantity, funit_price) " \
                "values (%s, %s, %s, %s) " \
                "returning fulfillment_id;"
        cursor.execute(query, (request_id, person_id, fquantity, funit_price))

        fulfillment_id = cursor.fetchone()[0]

        self.conn.commit()
        return fulfillment_id

    def delete(self, fulfillment_id):
        cursor = self.conn.cursor()
        query = "delete from \"FulfilledRequests\" " \
                "where fulfillment_id = %s;"
        cursor.execute(query, (fulfillment_id,))
        self.conn.commit()
        return fulfillment_id

    def update(self, fulfillment_id, fquantity, funit_price):
        cursor = self.conn.cursor()
        query = "update \"FulfilledRequests\" " \
                "set fquantity = %s, funit_price = %s " \
                "where fulfillment_id = %s;"
        cursor.execute(query, (fquantity, funit_price, fulfillment_id))
        self.conn.commit()
        return fulfillment_id
