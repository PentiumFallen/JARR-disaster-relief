from backend.config.dbconfig import pg_config
import psycopg2


class CategoryDao:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s" % (pg_config['dbname'],
                                                            pg_config['user'],
                                                            pg_config['passwd'])
        self.conn = psycopg2._connect(connection_url)


    def getAllCategories(self):
        cursor = self.conn.cursor()
        query = "select distinct category from Categories;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllCategoriesWithSubcategories(self):
        cursor = self.conn.cursor()
        query = "select category_id, category, subcategory from Categories as C left join Subcategories as S on " \
                "C.subcategory_id = S.subcategory_id;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getSubcategorybyCategory(self, category):
        cursor = self.conn.cursor()
        query = "select subcategory from Categories as C left join Subcategories as S on " \
                "C.subcategory_id = S.subcategory_id" \
                "where category = %s;"
        cursor.execute(query, (category,))
        result = []
        for row in cursor:
            result.append(row)
        return result
