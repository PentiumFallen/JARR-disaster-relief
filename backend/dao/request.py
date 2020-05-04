from backend.config.dbconfig import pg_config
import psycopg2


class RequestDAO:
    def __init__(self):

        connection_url = "dbname=%s user=%s password=%s" % (pg_config['dbname'],
                                                            pg_config['user'],
                                                            pg_config['passwd'])
        self.conn = psycopg2._connect(connection_url)

    def getAllRequests(self):
        cursor = self.conn.cursor()
        query = "select request_id, category, subcategory, person_id, name, quantity, rdescription, needed, "\
                "max_unit_price, date_requested, address_id from Requests natural inner join Resources natural inner join " \
                "(select category_id,category, subcategory from Categories as C left join Subcategories as S on " \
                "C.subcategory_id = S.subcategory_id) as Cat;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getTotalRequests(self):
        cursor = self.conn.cursor()
        query = "select count(*) from Requests;"
        cursor.execute(query)
        result = int(cursor.fetchone()[0])
        return result

    def getTotalRequestsPerCategory(self):
        cursor = self.conn.cursor()
        query = "select category, count(*) from Requests natural inner join Resources natural inner join Categories " \
                "group by category order by category;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getTotalNeededRequests(self):
        cursor = self.conn.cursor()
        query = "select count(*) from Requests where needed > 0;"
        cursor.execute(query)
        result = int(cursor.fetchone()[0])
        return result

    def getTotalNeededRequestsPerCategory(self):
        cursor = self.conn.cursor()
        query = "select category, count(*) from Requests natural inner join Resources natural inner join Categories " \
                " where needed > 0 group by category order by category;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllNeededRequests(self):
        cursor = self.conn.cursor()
        query = "select request_id, category, subcategory, person_id, name, quantity, rdescription, needed, "\
                "max_unit_price, date_requested, address_id from Requests natural inner join Resources natural inner join (select category_id, " \
                "category, subcategory from Categories as C left join Subcategories as S on C.subcategory_id = " \
                "S.subcategory_id) as Cat where needed > 0;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getRequestById(self, request_id):
        cursor = self.conn.cursor()
        query = "select request_id, category, subcategory, person_id, name, quantity, rdescription, needed, "\
                "max_unit_price, date_requested, address_id from Requests natural inner join Resources natural inner join (select category_id, " \
                "category, subcategory from Categories as C left join Subcategories as S on C.subcategory_id = " \
                "S.subcategory_id) as Cat where request_id = %s;"
        cursor.execute(query, (request_id,))
        result = cursor.fetchone()
        return result

    def getRequestsByPersonId(self, person_id):
        cursor = self.conn.cursor()
        query = "select request_id, category, subcategory, person_id, name, quantity, rdescription, needed, "\
                "max_unit_price, date_requested, address_id from Requests natural inner join Resources natural inner join (select category_id, " \
                "category, subcategory from Categories as C left join Subcategories as S on C.subcategory_id = " \
                "S.subcategory_id) as Cat where person_id = %s;"
        cursor.execute(query, (person_id,))
        result = cursor.fetchall()
        return result

    def getRequestsByMaxPriceAndCategory(self, max_price, category):
        cursor = self.conn.cursor()
        query = "select request_id, category, subcategory, person_id, name, quantity, rdescription, needed, "\
                "max_unit_price, date_requested, address_id from Requests natural inner join Resources natural inner join (select category_id, " \
                "category, subcategory from Categories as C left join Subcategories as S on C.subcategory_id = " \
                "S.subcategory_id) as Cat where max_unit_price = %s and category = %s;"
        cursor.execute(query, (max_price, category))
        result = cursor.fetchall()
        return result

    def getRequestsByMaxPrice(self, brand):
        cursor = self.conn.cursor()
        query = "select request_id, category, subcategory, person_id, name, quantity, rdescription, needed, "\
                "max_unit_price, date_requested, address_id from Requests natural inner join Resources natural inner join (select category_id, " \
                "category, subcategory from Categories as C left join Subcategories as S on C.subcategory_id = " \
                "S.subcategory_id) as Cat where max_unit_price = %s;"
        cursor.execute(query, (brand,))
        result = cursor.fetchall()
        return result

    def getRequestsByCategory(self, category):
        cursor = self.conn.cursor()
        query = "select request_id, category, subcategory, person_id, name, quantity, rdescription, needed, "\
                "max_unit_price, date_requested, address_id from Requests natural inner join Resources natural inner join (select category_id, " \
                "category, subcategory from Categories as C left join Subcategories as S on C.subcategory_id = " \
                "S.subcategory_id) as Cat where category = %s;"
        cursor.execute(query, (category,))
        result = cursor.fetchall()
        return result

    def getNeededRequestsByMaxPriceAndCategory(self, max_price, category):
        cursor = self.conn.cursor()
        query = "select request_id, category, subcategory, person_id, name, quantity, rdescription, needed, " \
                "max_unit_price, date_requested, address_id from Requests natural inner join Resources natural inner join (select category_id, " \
                "category, subcategory from Categories as C left join Subcategories as S on C.subcategory_id = " \
                "S.subcategory_id) as Cat where max_unit_price = %s and category = %s and needed > 0;"
        cursor.execute(query, (max_price, category))
        result = cursor.fetchall()
        return result

    def getNeededRequestsByMaxPrice(self, brand):
        cursor = self.conn.cursor()
        query = "select request_id, category, subcategory, person_id, name, quantity, rdescription, needed, " \
                "max_unit_price, date_requested, address_id from Requests natural inner join Resources natural inner join (select category_id, " \
                "category, subcategory from Categories as C left join Subcategories as S on C.subcategory_id = " \
                "S.subcategory_id) as Cat where max_unit_price = %s and needed > 0;"
        cursor.execute(query, (brand,))
        result = cursor.fetchall()
        return result

    def getNeededRequestsByCategory(self, category):
        cursor = self.conn.cursor()
        query = "select request_id, category, subcategory, person_id, name, quantity, rdescription, needed, " \
                "max_unit_price, date_requested, address_id from Requests natural inner join Resources natural inner join (select category_id, " \
                "category, subcategory from Categories as C left join Subcategories as S on C.subcategory_id = " \
                "S.subcategory_id) as Cat where category = %s and needed > 0;"
        cursor.execute(query, (category,))
        result = cursor.fetchall()
        return result

    def insert(self, resource_id, person_id, description, needed, unit_price, address_id):
        cursor = self.conn.cursor()

        query = "insert into Requests(resource_id, person_id, description, needed, max_unit_price, " \
                "address_id) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) returning request_id;"
        cursor.execute(query, (resource_id, person_id, description, needed, unit_price, address_id))

        request_id = cursor.fetchone()[0]

        self.conn.commit()
        return request_id

    def delete(self, request_id):
        cursor = self.conn.cursor()
        query = "update Requests set needed = 0 where request_id = %s;"
        cursor.execute(query, (request_id,))
        self.conn.commit()
        return request_id

    def update(self, request_id, description, needed, unit_price, address_id):
        cursor = self.conn.cursor()
        query = "update Requests set description = %s, needed = %s, unit_price = %s, address_id = %s where " \
                "request_id = %s;"
        cursor.execute(query, (request_id, description, needed, unit_price, address_id))
        self.conn.commit()
        return request_id
