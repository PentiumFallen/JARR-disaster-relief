from backend.config.dbconfig import pg_config
from backend.dao.address import AddressDao
from backend.dao.resource import ResourceDAO
from backend.utility import senate_district
import psycopg2


class RequestDAO:
    def __init__(self):

        connection_url = "dbname=%s user=%s password=%s host=%s" % (pg_config['dbname'],
                                                                    pg_config['user'],
                                                                    pg_config['passwd'],
                                                                    pg_config['host'])
        self.conn = psycopg2._connect(connection_url)

    def getAllRequests(self):
        cursor = self.conn.cursor()
        query = "select request_id, category, subcategory, person_id, name, quantity, rdescription, needed, "\
                "max_unit_price, date_requested, address, city, district, zip_code from \"Requests\" natural inner join \"Resources\" natural inner join " \
                "(select category_id,category, subcategory from \"Categories\" as C left join \"Subcategories\" as S on " \
                "C.subcategory_id = S.subcategory_id) as Cat natural inner join \"Addresses\";"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getTotalRequests(self):
        cursor = self.conn.cursor()
        query = "select count(*) from \"Requests\";"
        cursor.execute(query)
        result = int(cursor.fetchone()[0])
        return result

    def getTotalRequestsPerCategory(self):
        cursor = self.conn.cursor()
        query = "select category, count(*) from \"Requests\" natural inner join \"Resources\" natural inner join \"Categories\" " \
                "group by category order by category;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getTotalNeededRequests(self):
        cursor = self.conn.cursor()
        query = "select count(*) from \"Requests\" where needed > 0;"
        cursor.execute(query)
        result = int(cursor.fetchone()[0])
        return result

    def getTotalNeededRequestsPerCategory(self):
        cursor = self.conn.cursor()
        query = "select category, count(*) from \"Requests\" natural inner join \"Resources\" natural inner join \"Categories\" " \
                " where needed > 0 group by category order by category;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllNeededRequests(self):
        cursor = self.conn.cursor()
        query = "select request_id, category, subcategory, person_id, name, quantity, rdescription, needed, "\
                "max_unit_price, date_requested, address, city, district, zip_code from \"Requests\" natural inner join \"Resources\" natural inner join (select category_id, " \
                "category, subcategory from \"Categories\" as C left join \"Subcategories\" as S on C.subcategory_id = " \
                "S.subcategory_id) as Cat natural inner join \"Addresses\" where needed > 0;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getRequestById(self, request_id):
        cursor = self.conn.cursor()
        query = "select request_id, category, subcategory, person_id, name, quantity, rdescription, needed, "\
                "max_unit_price, date_requested, address, city, district, zip_code from \"Requests\" natural inner join \"Resources\" natural inner join (select category_id, " \
                "category, subcategory from \"Categories\" as C left join \"Subcategories\" as S on C.subcategory_id = " \
                "S.subcategory_id) as Cat natural inner join \"Addresses\" where request_id = %s;"
        cursor.execute(query, (request_id,))
        result = cursor.fetchone()
        return result

    def getRequestsByPersonId(self, person_id):
        cursor = self.conn.cursor()
        query = "select request_id, category, subcategory, person_id, name, quantity, rdescription, needed, "\
                "max_unit_price, date_requested, address, city, district, zip_code from \"Requests\" natural inner join \"Resources\" natural inner join (select category_id, " \
                "category, subcategory from \"Categories\" as C left join \"Subcategories\" as S on C.subcategory_id = " \
                "S.subcategory_id) as Cat natural inner join \"Addresses\" where person_id = %s order by name;"
        cursor.execute(query, (person_id,))
        result = cursor.fetchall()
        return result

    def getNeededRequestsByPersonId(self, person_id):
        cursor = self.conn.cursor()
        query = "select request_id, category, subcategory, person_id, name, quantity, rdescription, needed, "\
                "max_unit_price, date_requested, address, city, district, zip_code from \"Requests\" natural inner join \"Resources\" natural inner join (select category_id, " \
                "category, subcategory from \"Categories\" as C left join \"Subcategories\" as S on C.subcategory_id = " \
                "S.subcategory_id) as Cat natural inner join \"Addresses\" where person_id = %s and needed > 0 order by name;"
        cursor.execute(query, (person_id,))
        result = cursor.fetchall()
        return result

    def getRequestsByMaxPriceAndCategory(self, max_price, category):
        cursor = self.conn.cursor()
        query = "select request_id, category, subcategory, person_id, name, quantity, rdescription, needed, "\
                "max_unit_price, date_requested, address, city, district, zip_code from \"Requests\" natural inner join \"Resources\" natural inner join (select category_id, " \
                "category, subcategory from \"Categories\" as C left join \"Subcategories\" as S on C.subcategory_id = " \
                "S.subcategory_id) as Cat natural inner join \"Addresses\" where max_unit_price = %s and category = %s order by name;"
        cursor.execute(query, (max_price, category))
        result = cursor.fetchall()
        return result

    def getRequestsByMaxPrice(self, brand):
        cursor = self.conn.cursor()
        query = "select request_id, category, subcategory, person_id, name, quantity, rdescription, needed, "\
                "max_unit_price, date_requested, address, city, district, zip_code from \"Requests\" natural inner join \"Resources\" natural inner join (select category_id, " \
                "category, subcategory from \"Categories\" as C left join \"Subcategories\" as S on C.subcategory_id = " \
                "S.subcategory_id) as Cat natural inner join \"Addresses\" where max_unit_price = %s order by name;"
        cursor.execute(query, (brand,))
        result = cursor.fetchall()
        return result

    def getRequestsByCategory(self, category):
        cursor = self.conn.cursor()
        query = "select request_id, category, subcategory, person_id, name, quantity, rdescription, needed, "\
                "max_unit_price, date_requested, address, city, district, zip_code from \"Requests\" natural inner join \"Resources\" natural inner join (select category_id, " \
                "category, subcategory from \"Categories\" as C left join \"Subcategories\" as S on C.subcategory_id = " \
                "S.subcategory_id) as Cat natural inner join \"Addresses\" where category = %s order by name;"
        cursor.execute(query, (category,))
        result = cursor.fetchall()
        return result

    def getRequestsByName(self, name):
        cursor = self.conn.cursor()
        query = "select request_id, category, subcategory, person_id, name, quantity, rdescription, needed, "\
                "max_unit_price, date_requested, address, city, district, zip_code from \"Requests\" natural inner join \"Resources\" natural inner join (select category_id, " \
                "category, subcategory from \"Categories\" as C left join \"Subcategories\" as S on C.subcategory_id = " \
                "S.subcategory_id) as Cat natural inner join \"Addresses\" where name = %s;"
        cursor.execute(query, (name,))
        result = cursor.fetchall()
        return result

    def getNeededRequestsByMaxPriceAndCategory(self, max_price, category):
        cursor = self.conn.cursor()
        query = "select request_id, category, subcategory, person_id, name, quantity, rdescription, needed, " \
                "max_unit_price, date_requested, address, city, district, zip_code from \"Requests\" natural inner join \"Resources\" natural inner join (select category_id, " \
                "category, subcategory from \"Categories\" as C left join \"Subcategories\" as S on C.subcategory_id = " \
                "S.subcategory_id) as Cat natural inner join \"Addresses\" where max_unit_price = %s and category = %s and needed > 0 order by name;"
        cursor.execute(query, (max_price, category))
        result = cursor.fetchall()
        return result

    def getNeededRequestsByMaxPrice(self, brand):
        cursor = self.conn.cursor()
        query = "select request_id, category, subcategory, person_id, name, quantity, rdescription, needed, " \
                "max_unit_price, date_requested, address, city, district, zip_code from \"Requests\" natural inner join \"Resources\" natural inner join (select category_id, " \
                "category, subcategory from \"Categories\" as C left join \"Subcategories\" as S on C.subcategory_id = " \
                "S.subcategory_id) as Cat natural inner join \"Addresses\" where max_unit_price = %s and needed > 0 order by name;"
        cursor.execute(query, (brand,))
        result = cursor.fetchall()
        return result

    def getNeededRequestsByCategory(self, category):
        cursor = self.conn.cursor()
        query = "select request_id, category, subcategory, person_id, name, quantity, rdescription, needed, " \
                "max_unit_price, date_requested, address, city, district, zip_code from \"Requests\" natural inner join \"Resources\" natural inner join (select category_id, " \
                "category, subcategory from \"Categories\" as C left join \"Subcategories\" as S on C.subcategory_id = " \
                "S.subcategory_id) as Cat natural inner join \"Addresses\" where category = %s and needed > 0 order by name;"
        cursor.execute(query, (category,))
        result = cursor.fetchall()
        return result

    def getNeededRequestsByName(self, name):
        cursor = self.conn.cursor()
        query = "select request_id, category, subcategory, person_id, name, quantity, rdescription, needed, " \
                "max_unit_price, date_requested, address, city, district, zip_code from \"Requests\" natural inner join \"Resources\" natural inner join (select category_id, " \
                "category, subcategory from \"Categories\" as C left join \"Subcategories\" as S on C.subcategory_id = " \
                "S.subcategory_id) as Cat natural inner join \"Addresses\" where name = %s and needed > 0;"
        cursor.execute(query, (name,))
        result = cursor.fetchall()
        return result

    def insert(self, resource_id, person_id, description, needed, unit_price, address, city, zip_code):
        cursor = self.conn.cursor()
        address_id = AddressDao().getAddressIdFromAddressAndCityAndZipCode(address, city, zip_code)
        if not address_id:
            address_id = AddressDao().insert(address, city, zip_code)
        query = "insert into \"Requests\"(resource_id, person_id, rdescription, needed, max_unit_price, " \
                "address_id) values (%s, %s, %s, %s, %s, %s) returning request_id;"
        cursor.execute(query, (resource_id, person_id, description, needed, unit_price, address_id))

        request_id = cursor.fetchone()[0]

        self.conn.commit()
        return request_id

    def delete(self, request_id):
        cursor = self.conn.cursor()
        query = "update \"Requests\" set needed = 0 where request_id = %s;"
        cursor.execute(query, (request_id,))
        self.conn.commit()
        return request_id

    def update(self, request_id, description, needed, unit_price, address, city, zip_code):
        cursor = self.conn.cursor()
        address_id = AddressDao().getAddressIdFromAddressAndCityAndZipCode(address, city, zip_code)
        if not address_id:
            address_id = AddressDao().insert(address, city, zip_code)
        query = "update \"Requests\" set rdescription = %s, max_unit_price = %s, address_id = %s" \
                "where request_id = %s;"
        cursor.execute(query, (description, unit_price, address_id, request_id))
        self.conn.commit()
        self.updateStock(request_id, needed)
        return request_id

    def updateStock(self, request_id, needed):
        request = self.getRequestById(request_id)
        curr_request_need = request[7]
        need_difference = int(needed) - curr_request_need
        if need_difference != 0:
            resource = ResourceDAO().getResourceIdAndQuantityBySupplyId(request_id)
            new_resource_quantity = resource[1] + need_difference
            ResourceDAO().updateResource(resource[0], new_resource_quantity)
            cursor = self.conn.cursor()
            query = "update \"Requests\" " \
                    "set needed = %s " \
                    "where request_id = %s;"
            cursor.execute(query, (needed, request_id))
            self.conn.commit()
            return request_id
