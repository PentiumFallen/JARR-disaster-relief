from backend.config.dbconfig import pg_config
import psycopg2


class ResourceDAO:
    def __init__(self):

        connection_url = "dbname=%s user=%s password=%s" % (pg_config['dbname'],
                                                            pg_config['user'],
                                                            pg_config['passwd'])
        self.conn = psycopg2._connect(connection_url)

    def getAllResource(self):
        cursor = self.conn.cursor()
        query = "select resource_id, person_id, name, quantity, brand "\
                "from Resources natural inner join " \
                "(select category_id,category, subcategory from Categories as C left join Subcategories as S on " \
                "C.subcategory_id = S.subcategory_id);"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getResourceById(self, resource_id):
        cursor = self.conn.cursor()
        query = "select resource_id, person_id, name, quantity, brand "\
                "from Resources natural inner join " \
                "(select category_id,category, subcategory from Categories as C left join Subcategories as S on " \
                "C.subcategory_id = S.subcategory_id) where resource_id = %s;"
        cursor.execute(query, (resource_id,))
        result = cursor.fetchone()
        return result

    def getResourceByName(self, name):
        cursor = self.conn.cursor()
        query = "select resource_id, person_id, name, quantity, brand "\
                "from Resources natural inner join " \
                "(select category_id,category, subcategory from Categories as C left join Subcategories as S on " \
                "C.subcategory_id = S.subcategory_id) where name = %s;"
        cursor.execute(query, (name,))
        result = cursor.fetchone()
        return result

    def getResourceByBrand(self, brand):
        cursor = self.conn.cursor()
        query = "select resource_id, person_id, name, quantity, brand "\
                "from Resources natural inner join " \
                "(select category_id,category, subcategory from Categories as C left join Subcategories as S on " \
                "C.subcategory_id = S.subcategory_id) where brand = %s;"
        cursor.execute(query, (brand,))
        result = cursor.fetchone()
        return result

    def getResourceByNamePerCategory(self, name):
        cursor = self.conn.cursor()
        query = "select category from Resources natural inner join Categories " \
                " where name = %s group by category order by category;"
        cursor.execute(query, (name,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getResourceByPersonId(self, person_id):
        cursor = self.conn.cursor()
        query = "select select resource_id, person_id, name, quantity, brand "\
                "from Resources natural inner join (select category_id, " \
                "category, subcategory from Categories as C left join Subcategories as S on C.subcategory_id = " \
                "S.subcategory_id) where person_id = %s;"
        cursor.execute(query, (person_id,))
        result = cursor.fetchall()
        return result


    def getResourceByCategory(self, category):
        cursor = self.conn.cursor()
        query = "select select resource_id, person_id, name, quantity, brand "\
                "from Resources natural inner join (select category_id, " \
                "category, subcategory from Categories as C left join Subcategories as S on C.subcategory_id = " \
                "S.subcategory_id) where category = %s;"
        cursor.execute(query, (category,))
        result = cursor.fetchall()
        return result

    def getResourceByNameAndCategory(self, name, category):
        cursor = self.conn.cursor()
        query = "select select resource_id, person_id, name, quantity, brand "\
                "from Resources natural inner join (select category_id, " \
                "category, subcategory from Categories as C left join Subcategories as S on C.subcategory_id = " \
                "S.subcategory_id) where name = %s and category = %s;"
        cursor.execute(query, (name, category))
        result = cursor.fetchall()
        return result

    def getAllNeededResource(self, quantity):
        cursor = self.conn.cursor()
        query = "select select resource_id, person_id, name, quantity, brand "\
                "from Resources natural inner join (select category_id, " \
                "category, subcategory from Categories as C left join Subcategories as S on C.subcategory_id = " \
                "S.subcategory_id) where quantity = 0;"
        cursor.execute(query, (quantity,))
        result = cursor.fetchall()
        return result