from backend.config.dbconfig import pg_config
from backend.dao.address import AddressDao
from backend.dao.resource import ResourceDAO
import psycopg2


class SupplyDAO:
    def __init__(self):

        connection_url = "dbname=%s user=%s password=%s host=%s" % (pg_config['dbname'],
                                                                    pg_config['user'],
                                                                    pg_config['passwd'],
                                                                    pg_config['host'])
        self.conn = psycopg2._connect(connection_url)

    def getAllSupplies(self):
        cursor = self.conn.cursor()
        query = "select supply_id, category, subcategory, person_id, name, quantity, brand, sdescription, available, "\
                "sunit_price, date_offered, address, city, district, zip_code from \"Supplies\" natural inner join \"Resources\" natural inner join " \
                "(select category_id,category, subcategory from \"Categories\" as C left join \"Subcategories\" as S on " \
                "C.subcategory_id = S.subcategory_id) as Cat natural inner join \"Addresses\";"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getTotalSupplies(self):
        cursor = self.conn.cursor()
        query = "select count(*) from \"Supplies\";"
        cursor.execute(query)
        result = int(cursor.fetchone()[0])
        return result

    def getTotalSuppliesPerCategory(self):
        cursor = self.conn.cursor()
        query = "select category, count(*) from \"Supplies\" natural inner join \"Resources\" natural inner join \"Categories\" " \
                "group by category order by category;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getTotalAvailableSupplies(self):
        cursor = self.conn.cursor()
        query = "select count(*) from \"Supplies\" where available > 0;"
        cursor.execute(query)
        result = int(cursor.fetchone()[0])
        return result

    def getTotalAvailableSuppliesPerCategory(self):
        cursor = self.conn.cursor()
        query = "select category, count(*) from \"Supplies\" natural inner join \"Resources\" natural inner join \"Categories\" " \
                " where available > 0 group by category order by category;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllAvailableSupplies(self):
        cursor = self.conn.cursor()
        query = "select supply_id, category, subcategory, person_id, name, quantity, brand, sdescription, available, "\
                "sunit_price, date_offered, address, city, district, zip_code from \"Supplies\" natural inner join \"Resources\" natural inner join (select category_id, " \
                "category, subcategory from \"Categories\" as C left join \"Subcategories\" as S on C.subcategory_id = " \
                "S.subcategory_id) as Cat natural inner join \"Addresses\" where available > 0;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getSupplyById(self, supply_id):
        cursor = self.conn.cursor()
        query = "select supply_id, category, subcategory, person_id, name, quantity, brand, sdescription, available, "\
                "sunit_price, date_offered, address, city, district, zip_code from \"Supplies\" natural inner join \"Resources\" natural inner join (select category_id, " \
                "category, subcategory from \"Categories\" as C left join \"Subcategories\" as S on C.subcategory_id = " \
                "S.subcategory_id) as Cat natural inner join \"Addresses\" where supply_id = %s;"
        cursor.execute(query, (supply_id,))
        result = cursor.fetchone()
        return result

    def getSuppliesByPersonId(self, person_id):
        cursor = self.conn.cursor()
        query = "select supply_id, category, subcategory, person_id, name, quantity, brand, sdescription, available, "\
                "sunit_price, date_offered, address, city, district, zip_code from \"Supplies\" natural inner join \"Resources\" natural inner join (select category_id, " \
                "category, subcategory from \"Categories\" as C left join \"Subcategories\" as S on C.subcategory_id = " \
                "S.subcategory_id) as Cat natural inner join \"Addresses\" where person_id = %s order by name;"
        cursor.execute(query, (person_id,))
        result = cursor.fetchall()
        return result

    def getAvailableSuppliesByPersonId(self, person_id):
        cursor = self.conn.cursor()
        query = "select supply_id, category, subcategory, person_id, name, quantity, brand, sdescription, available, "\
                "sunit_price, date_offered, address, city, district, zip_code from \"Supplies\" natural inner join \"Resources\" natural inner join (select category_id, " \
                "category, subcategory from \"Categories\" as C left join \"Subcategories\" as S on C.subcategory_id = " \
                "S.subcategory_id) as Cat natural inner join \"Addresses\" where person_id = %s and available > 0 order by name;"
        cursor.execute(query, (person_id,))
        result = cursor.fetchall()
        return result

    def getSuppliesByBrandAndCategoryAndSubcategoryAndMaxPrice(self, brand, category, subcategory, max_price):
        cursor = self.conn.cursor()
        query = "select supply_id, category, subcategory, person_id, name, quantity, brand, sdescription, available, "\
                "sunit_price, date_offered, address, city, district, zip_code from \"Supplies\" natural inner join \"Resources\" natural inner join (select category_id, " \
                "category, subcategory from \"Categories\" as C left join \"Subcategories\" as S on C.subcategory_id = " \
                "S.subcategory_id) as Cat natural inner join \"Addresses\" where brand = %s and category = %s and subcategory = %s sunit_price < %s order by name;"
        cursor.execute(query, (brand, category, subcategory, max_price))
        result = cursor.fetchall()
        return result

    def getSuppliesByBrandAndCategoryAndSubcategory(self, brand, category, subcategory):
        cursor = self.conn.cursor()
        query = "select supply_id, category, subcategory, person_id, name, quantity, brand, sdescription, available, "\
                "sunit_price, date_offered, address, city, district, zip_code from \"Supplies\" natural inner join \"Resources\" natural inner join (select category_id, " \
                "category, subcategory from \"Categories\" as C left join \"Subcategories\" as S on C.subcategory_id = " \
                "S.subcategory_id) as Cat natural inner join \"Addresses\" where brand = %s and category = %s and subcategory = %s order by name;"
        cursor.execute(query, (brand, category, subcategory))
        result = cursor.fetchall()
        return result

    def getSuppliesByBrandAndCategoryAndMaxPrice(self, brand, category, max_price):
        cursor = self.conn.cursor()
        query = "select supply_id, category, subcategory, person_id, name, quantity, brand, sdescription, available, "\
                "sunit_price, date_offered, address, city, district, zip_code from \"Supplies\" natural inner join \"Resources\" natural inner join (select category_id, " \
                "category, subcategory from \"Categories\" as C left join \"Subcategories\" as S on C.subcategory_id = " \
                "S.subcategory_id) as Cat natural inner join \"Addresses\" where brand = %s and category = %s and sunit_price < %s order by name;"
        cursor.execute(query, (brand, category, max_price))
        result = cursor.fetchall()
        return result

    def getSuppliesByBrandAndCategory(self, brand, category):
        cursor = self.conn.cursor()
        query = "select supply_id, category, subcategory, person_id, name, quantity, brand, sdescription, available, "\
                "sunit_price, date_offered, address, city, district, zip_code from \"Supplies\" natural inner join \"Resources\" natural inner join (select category_id, " \
                "category, subcategory from \"Categories\" as C left join \"Subcategories\" as S on C.subcategory_id = " \
                "S.subcategory_id) as Cat natural inner join \"Addresses\" where brand = %s and category = %s;"
        cursor.execute(query, (brand, category))
        result = cursor.fetchall()
        return result

    def getSuppliesByBrand(self, brand):
        cursor = self.conn.cursor()
        query = "select supply_id, category, subcategory, person_id, name, quantity, brand, sdescription, available, "\
                "sunit_price, date_offered, address, city, district, zip_code from \"Supplies\" natural inner join \"Resources\" natural inner join (select category_id, " \
                "category, subcategory from \"Categories\" as C left join \"Subcategories\" as S on C.subcategory_id = " \
                "S.subcategory_id) as Cat natural inner join \"Addresses\" where brand = %s order by name;"
        cursor.execute(query, (brand,))
        result = cursor.fetchall()
        return result

    def getSuppliesByName(self, name):
        cursor = self.conn.cursor()
        query = "select supply_id, category, subcategory, person_id, name, quantity, brand, sdescription, available, "\
                "sunit_price, date_offered, address, city, district, zip_code from \"Supplies\" natural inner join \"Resources\" natural inner join (select category_id, " \
                "category, subcategory from \"Categories\" as C left join \"Subcategories\" as S on C.subcategory_id = " \
                "S.subcategory_id) as Cat natural inner join \"Addresses\" where name like %s or name like %s or name like %s or name like %s;"
        cursor.execute(query, ('%'+name+'%', name, '%'+name, name+'%'))
        result = cursor.fetchall()
        return result

    def getSuppliesByCategory(self, category):
        cursor = self.conn.cursor()
        query = "select supply_id, category, subcategory, person_id, name, quantity, brand, sdescription, available, "\
                "sunit_price, date_offered, address, city, district, zip_code from \"Supplies\" natural inner join \"Resources\" natural inner join (select category_id, " \
                "category, subcategory from \"Categories\" as C left join \"Subcategories\" as S on C.subcategory_id = " \
                "S.subcategory_id) as Cat natural inner join \"Addresses\" where category = %s order by name;"
        cursor.execute(query, (category,))
        result = cursor.fetchall()
        return result

    def getSuppliesByMaxPrice(self, max_price):
        cursor = self.conn.cursor()
        query = "select supply_id, category, subcategory, person_id, name, quantity, brand, sdescription, available, "\
                "sunit_price, date_offered, address, city, district, zip_code from \"Supplies\" natural inner join \"Resources\" natural inner join (select category_id, " \
                "category, subcategory from \"Categories\" as C left join \"Subcategories\" as S on C.subcategory_id = " \
                "S.subcategory_id) as Cat natural inner join \"Addresses\" where sunit_price < %s order by name;"
        cursor.execute(query, (max_price,))
        result = cursor.fetchall()
        return result

    def getAvailableSuppliesByBrandAndCategoryAndSubcategoryAndMaxPrice(self, brand, category, subcategory, max_price):
        cursor = self.conn.cursor()
        query = "select supply_id, category, subcategory, person_id, name, quantity, brand, sdescription, available, "\
                "sunit_price, date_offered, address, city, district, zip_code from \"Supplies\" natural inner join \"Resources\" natural inner join (select category_id, " \
                "category, subcategory from \"Categories\" as C left join \"Subcategories\" as S on C.subcategory_id = " \
                "S.subcategory_id) as Cat natural inner join \"Addresses\" where brand = %s and category = %s and " \
                "subcategory = %s sunit_price < %s and available > 0 order by name;"
        cursor.execute(query, (brand, category, subcategory, max_price))
        result = cursor.fetchall()
        return result

    def getAvailableSuppliesByBrandAndCategoryAndSubcategory(self, brand, category, subcategory):
        cursor = self.conn.cursor()
        query = "select supply_id, category, subcategory, person_id, name, quantity, brand, sdescription, available, "\
                "sunit_price, date_offered, address, city, district, zip_code from \"Supplies\" natural inner join \"Resources\" natural inner join (select category_id, " \
                "category, subcategory from \"Categories\" as C left join \"Subcategories\" as S on C.subcategory_id = " \
                "S.subcategory_id) as Cat natural inner join \"Addresses\" where brand = %s and category = %s and subcategory = %s and available > 0 order by name;"
        cursor.execute(query, (brand, category, subcategory))
        result = cursor.fetchall()
        return result

    def getAvailableSuppliesByBrandAndCategoryAndMaxPrice(self, brand, category, max_price):
        cursor = self.conn.cursor()
        query = "select supply_id, category, subcategory, person_id, name, quantity, brand, sdescription, available, "\
                "sunit_price, date_offered, address, city, district, zip_code from \"Supplies\" natural inner join \"Resources\" natural inner join (select category_id, " \
                "category, subcategory from \"Categories\" as C left join \"Subcategories\" as S on C.subcategory_id = " \
                "S.subcategory_id) as Cat natural inner join \"Addresses\" where brand = %s and category = %s and sunit_price < %s and available > 0 order by name;"
        cursor.execute(query, (brand, category, max_price))
        result = cursor.fetchall()
        return result

    def getAvailableSuppliesByBrandAndCategory(self, brand, category):
        cursor = self.conn.cursor()
        query = "select supply_id, category, subcategory, person_id, name, quantity, brand, sdescription, available, "\
                "sunit_price, date_offered, address, city, district, zip_code from \"Supplies\" natural inner join \"Resources\" natural inner join (select category_id, " \
                "category, subcategory from \"Categories\" as C left join \"Subcategories\" as S on C.subcategory_id = " \
                "S.subcategory_id) as Cat natural inner join \"Addresses\" where brand = %s and category = %s and available > 0 order by name;"
        cursor.execute(query, (brand, category))
        result = cursor.fetchall()
        return result

    def getAvailableSuppliesByBrand(self, brand):
        cursor = self.conn.cursor()
        query = "select supply_id, category, subcategory, person_id, name, quantity, brand, sdescription, available, "\
                "sunit_price, date_offered, address, city, district, zip_code from \"Supplies\" natural inner join \"Resources\" natural inner join (select category_id, " \
                "category, subcategory from \"Categories\" as C left join \"Subcategories\" as S on C.subcategory_id = " \
                "S.subcategory_id) as Cat natural inner join \"Addresses\" where brand = %s and available > 0 order by name;"
        cursor.execute(query, (brand,))
        result = cursor.fetchall()
        return result

    def getAvailableSuppliesByName(self, name):
        cursor = self.conn.cursor()
        query = "select supply_id, category, subcategory, person_id, name, quantity, brand, sdescription, available, "\
                "sunit_price, date_offered, address, city, district, zip_code from \"Supplies\" natural inner join \"Resources\" natural inner join (select category_id, " \
                "category, subcategory from \"Categories\" as C left join \"Subcategories\" as S on C.subcategory_id = " \
                "S.subcategory_id) as Cat natural inner join \"Addresses\" where name = %s and available > 0;"
        cursor.execute(query, (name,))
        result = cursor.fetchall()
        return result

    def getAvailableSuppliesByCategory(self, category):
        cursor = self.conn.cursor()
        query = "select supply_id, category, subcategory, person_id, name, quantity, brand, sdescription, available, "\
                "sunit_price, date_offered, address, city, district, zip_code from \"Supplies\" natural inner join \"Resources\" natural inner join (select category_id, " \
                "category, subcategory from \"Categories\" as C left join \"Subcategories\" as S on C.subcategory_id = " \
                "S.subcategory_id) as Cat natural inner join \"Addresses\" where category = %s and available > 0 order by name;"
        cursor.execute(query, (category,))
        result = cursor.fetchall()
        return result

    def getAvailableSuppliesByMaxPrice(self, max_price):
        cursor = self.conn.cursor()
        query = "select supply_id, category, subcategory, person_id, name, quantity, brand, sdescription, available, "\
                "sunit_price, date_offered, address, city, district, zip_code from \"Supplies\" natural inner join \"Resources\" natural inner join (select category_id, " \
                "category, subcategory from \"Categories\" as C left join \"Subcategories\" as S on C.subcategory_id = " \
                "S.subcategory_id) as Cat natural inner join \"Addresses\" where sunit_price < %s and available > 0 order by name;"
        cursor.execute(query, (max_price,))
        result = cursor.fetchall()
        return result

    def insert(self, resource_id, brand, description, available, unit_price, address, city, zip_code):
        cursor = self.conn.cursor()
        address_id = AddressDao().getAddressIdFromAddressAndCityAndZipCode(address, city, zip_code)
        if not address_id:
            address_id = AddressDao().insert(address, city, zip_code)
        query = "insert into \"Supplies\"(resource_id, brand, sdescription, available, sunit_price, " \
                "address_id) values (%s, %s, %s, %s, %s, %s) returning supply_id;"
        cursor.execute(query, (resource_id, brand, description, available, unit_price, address_id))
        supply_id = cursor.fetchone()[0]
        self.conn.commit()
        return supply_id

    def delete(self, supply_id):
        cursor = self.conn.cursor()
        query = "update \"Supplies\" set available = 0 where supply_id = %s;"
        cursor.execute(query, (supply_id,))
        self.conn.commit()
        return supply_id

    def update(self, supply_id, brand, description, available, unit_price, address, city, zip_code):
        cursor = self.conn.cursor()
        address_id = AddressDao().getAddressIdFromAddressAndCityAndZipCode(address, city, zip_code)
        if not address_id:
            address_id = AddressDao().insert(address, city, zip_code)
        query = "update \"Supplies\" set brand = %s, sdescription = %s, sunit_price = %s, address_id = %s where " \
                "supply_id = %s;"
        cursor.execute(query, (brand, description, unit_price, address_id, supply_id))
        self.conn.commit()
        self.updateStock(supply_id, available)
        return supply_id

    def updateStock(self, supply_id, available):
        supply = self.getSupplyById(supply_id)
        curr_supply_stock = supply[8]
        stock_difference = int(available) - curr_supply_stock
        if stock_difference != 0:
            resource = ResourceDAO().getResourceIdAndQuantityBySupplyId(supply_id)
            new_resource_quantity = resource[1] + stock_difference
            ResourceDAO().updateResource(resource[0], new_resource_quantity)
            cursor = self.conn.cursor()
            query = "update \"Supplies\" " \
                    "set available = %s " \
                    "where supply_id = %s;"
            cursor.execute(query, (available, supply_id))
            self.conn.commit()
            return supply_id
