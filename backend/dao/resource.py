from backend.config.dbconfig import pg_config
import psycopg2


class ResourceDAO:
    def __init__(self):

        connection_url = "dbname=%s user=%s password=%s host=%s" % (pg_config['dbname'],
                                                                    pg_config['user'],
                                                                    pg_config['passwd'],
                                                                    pg_config['host'])
        self.conn = psycopg2._connect(connection_url)

    def getAllResources(self):
        cursor = self.conn.cursor()
        query = "select resource_id, person_id, name, category, subcategory, quantity "\
                "from \"Resources\" natural inner join (select category_id, " \
                "category, subcategory from \"Categories\" as C left join \"Subcategories\" as S on C.subcategory_id = " \
                "S.subcategory_id) as cat;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getResourceById(self, resource_id):
        cursor = self.conn.cursor()
        query = "select resource_id, person_id, name, category, subcategory, quantity "\
                "from \"Resources\" natural inner join (select category_id, " \
                "category, subcategory from \"Categories\" as C left join \"Subcategories\" as S on C.subcategory_id = " \
                "S.subcategory_id) as cat "\
                "where resource_id = %s;"
        cursor.execute(query, (resource_id,))
        result = cursor.fetchone()
        return result

    def getTotalResources(self):
        cursor = self.conn.cursor()
        query = "select count(*) from \"Resources\";"
        cursor.execute(query)
        result = int(cursor.fetchone())
        return result

    def getTotalResourcesPerCategory(self):
        cursor = self.conn.cursor()
        query = "select category, subcategory, sum(quantity) as total_resources " \
                "from \"Resources\" natural inner join (select category_id, " \
                "category, subcategory from \"Categories\" as C left join \"Subcategories\" as S on C.subcategory_id = " \
                "S.subcategory_id) as cat " \
                "group by category, subcategory " \
                "order by category, subcategory;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllAvailableResources(self):
        cursor = self.conn.cursor()
        query = "select resource_id, person_id, name, category, subcategory, quantity " \
                "from \"Resources\" natural inner join (select category_id, " \
                "category, subcategory from \"Categories\" as C left join \"Subcategories\" as S on C.subcategory_id = " \
                "S.subcategory_id) as cat " \
                "where quantity > 0;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getResourcesByPersonId(self, person_id):
        cursor = self.conn.cursor()
        query = "select resource_id, person_id, name, category, subcategory, quantity " \
                "from \"Resources\" natural inner join (select category_id, " \
                "category, subcategory from \"Categories\" as C left join \"Subcategories\" as S on C.subcategory_id = " \
                "S.subcategory_id) as cat " \
                "where person_id = %s;"
        cursor.execute(query, (person_id,))
        result = cursor.fetchall()
        return result

    def getResourceIdAndQuantityBySupplyId(self, supply_id):
        cursor = self.conn.cursor()
        query = "select resource_id, quantity " \
                "from \"Resources\" natural inner join \"Supplies\" " \
                "where supply_id = %s;"
        cursor.execute(query, (supply_id,))
        result = cursor.fetchone()
        return result

    def getResourceIdAndQuantityByRequestId(self, request_id):
        cursor = self.conn.cursor()
        query = "select resource_id, quantity " \
                "from \"Resources\" natural inner join \"Requests\" " \
                "where request_id = %s;"
        cursor.execute(query, (request_id,))
        result = cursor.fetchone()
        return result

    def insert(self, person_id, name, quantity, category_id):
        cursor = self.conn.cursor()
        query = "insert into \"Resources\"(person_id, name, quantity, category_id)" \
                "values(%s, %s, %s, %s) returning resource_id"
        cursor.execute(query, (person_id, name, quantity, category_id))
        resource_id = cursor.fetchone()[0]
        self.conn.commit()
        return resource_id

    def updateResource(self, resource_id, quantity):
        cursor = self.conn.cursor()
        query = "update \"Resources\" " \
                "set quantity = %s " \
                "where resource_id = %s;"
        cursor.execute(query, (quantity, resource_id))
        self.conn.commit()
        return resource_id
