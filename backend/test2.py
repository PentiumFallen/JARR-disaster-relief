def getSuppliesByBrandAndCategoryAndSubcategoryAndMaxPrice(self, brand, category, subcategory, max_price):
    cursor = self.conn.cursor()
    query = "select supply_id, category, subcategory, person_id, name, quantity, brand, sdescription, available, " \
            "sunit_price, date_offered, address_id from Supplies natural inner join Resources natural inner join (select category_id, " \
            "category, subcategory from Categories as C left join Subcategories as S on C.subcategory_id = " \
            "S.subcategory_id) where brand = %s and category = %s and subcategory = %s sunit_price < %s;"
    cursor.execute(query, (brand, category, subcategory, max_price))
    result = cursor.fetchall()
    return result


def getSuppliesByBrandAndCategoryAndSubcategory(self, brand, category, subcategory):
    cursor = self.conn.cursor()
    query = "select supply_id, category, subcategory, person_id, name, quantity, brand, sdescription, available, " \
            "sunit_price, date_offered, address_id from Supplies natural inner join Resources natural inner join (select category_id, " \
            "category, subcategory from Categories as C left join Subcategories as S on C.subcategory_id = " \
            "S.subcategory_id) where brand = %s and category = %s and subcategory = %s;"
    cursor.execute(query, (brand, category, subcategory))
    result = cursor.fetchall()
    return result


def getSuppliesByBrandAndCategoryAndMaxPrice(self, brand, category, max_price):
    cursor = self.conn.cursor()
    query = "select supply_id, category, subcategory, person_id, name, quantity, brand, sdescription, available, " \
            "sunit_price, date_offered, address_id from Supplies natural inner join Resources natural inner join (select category_id, " \
            "category, subcategory from Categories as C left join Subcategories as S on C.subcategory_id = " \
            "S.subcategory_id) where brand = %s and category = %s and sunit_price < %s;"
    cursor.execute(query, (brand, category, max_price))
    result = cursor.fetchall()
    return result


def getSuppliesByBrandAndCategory(self, brand, category):
    cursor = self.conn.cursor()
    query = "select supply_id, category, subcategory, person_id, name, quantity, brand, sdescription, available, " \
            "sunit_price, date_offered, address_id from Supplies natural inner join Resources natural inner join (select category_id, " \
            "category, subcategory from Categories as C left join Subcategories as S on C.subcategory_id = " \
            "S.subcategory_id) where brand = %s and category = %s;"
    cursor.execute(query, (brand, category))
    result = cursor.fetchall()
    return result


def getSuppliesByBrand(self, brand):
    cursor = self.conn.cursor()
    query = "select supply_id, category, subcategory, person_id, name, quantity, brand, sdescription, available, " \
            "sunit_price, date_offered, address_id from Supplies natural inner join Resources natural inner join (select category_id, " \
            "category, subcategory from Categories as C left join Subcategories as S on C.subcategory_id = " \
            "S.subcategory_id) where brand = %s;"
    cursor.execute(query, (brand,))
    result = cursor.fetchall()
    return result


def getSuppliesByCategory(self, category):
    cursor = self.conn.cursor()
    query = "select supply_id, category, subcategory, person_id, name, quantity, brand, sdescription, available, " \
            "sunit_price, date_offered, address_id from Supplies natural inner join Resources natural inner join (select category_id, " \
            "category, subcategory from Categories as C left join Subcategories as S on C.subcategory_id = " \
            "S.subcategory_id) where category = %s;"
    cursor.execute(query, (category,))
    result = cursor.fetchall()
    return result


def getSuppliesByMaxPrice(self, max_price):
    cursor = self.conn.cursor()
    query = "select supply_id, category, subcategory, person_id, name, quantity, brand, sdescription, available, " \
            "sunit_price, date_offered, address_id from Supplies natural inner join Resources natural inner join (select category_id, " \
            "category, subcategory from Categories as C left join Subcategories as S on C.subcategory_id = " \
            "S.subcategory_id) where sunit_price < %s;"
    cursor.execute(query, (max_price,))
    result = cursor.fetchall()
    return result