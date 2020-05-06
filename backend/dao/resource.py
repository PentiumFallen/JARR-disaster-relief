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
        query = "select resource_id, person_id, name, category, subcategory, quantity, brand "\
                "from Resources natural inner join Categories left join Subcategories;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getTotalResource(self):
        cursor = self.conn.cursor()
        query = "select count(*) from Resources;"
        cursor.execute(query)
        result = int(cursor.fetchone())
        return result

    def getTotalResourcePerCategory(self):
        cursor = self.conn.cursor()
        query = "select category, subcategory, sum(quantity) as total_resources " \
                "from Resources natural inner join Categories left join Subcategories " \
                "group by category, subcategory " \
                "order by category, subcategory;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllAvailableResource(self):
        cursor = self.conn.cursor()
        query = "select category, subcategory, sum(quantity) as total_resources " \
                "from Resources natural inner join Categories left join Subcategories " \
                "where quantity > 0;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getResourceByPersonId(self, person_id):
        cursor = self.conn.cursor()
        query = "select resource_id, person_id, category, subcategory, quantity, name, brand " \
                "from Resources natural inner join Categories left join Subcategories " \
                "where person_id = %s;"
        cursor.execute(query, (person_id,))
        result = cursor.fetchall()
        return result
