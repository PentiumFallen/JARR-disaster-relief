from backend.config.dbconfig import pg_config
import psycopg2

class ToolDAO:
    def __init__(self):

        connection_url = "dbname=%s user=%s password=%s" % (pg_config['dbname'],
                                                            pg_config['user'],
                                                            pg_config['passwd'])
        self.conn = psycopg2._connect(connection_url)

    def getAllTool(self):
        cursor = self.conn.cursor()
        query = "select * from Tools;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllToolSupplies(self):
        cursor = self.conn.cursor()
        query = "select * from Tools where is_supply = TRUE;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllToolRequests(self):
        cursor = self.conn.cursor()
        query = "select * from Tools where is_supply = FALSE;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllAvailableToolSupplies(self):
        cursor = self.conn.cursor()
        query = "select * from Tools where is_supply = TRUE and curr_quantity > 0;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllUnfulfilledToolRequests(self):
        cursor = self.conn.cursor()
        query = "select * from Tools where is_supply = FALSE and curr_quantity > 0;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getToolById(self, tool_id):
        cursor = self.conn.cursor()
        query = "select * from Tools where tool_id = %s;"
        cursor.execute(query, (tool_id,))
        result = cursor.fetchone()
        return result

    def getToolByPersonId(self, person_id):
        cursor = self.conn.cursor()
        query = "select * from Tool swhere person_id = %s;"
        cursor.execute(query, (person_id,))
        result = cursor.fetchall()
        return result

    def getToolSuppliesByPersonId(self, person_id):
        cursor = self.conn.cursor()
        query = "select * from Tools where person_id = %s and is_supply = TRUE;"
        cursor.execute(query, (person_id,))
        result = cursor.fetchall()
        return result

    def getToolRequestsByPersonId(self, person_id):
        cursor = self.conn.cursor()
        query = "select * from Tools where person_id = %s and is_supply = FALSE;"
        cursor.execute(query, (person_id,))
        result = cursor.fetchall()
        return result

    def getToolByBrandAndName(self, brand, tool_name):
        cursor = self.conn.cursor()
        query = "select * from Tools where brand = %s and tool_name = %s;"
        cursor.execute(query, (brand, tool_name))
        result = cursor.fetchall()
        return result

    def getToolByBrand(self, brand):
        cursor = self.conn.cursor()
        query = "select * from Tools where brand = %s;"
        cursor.execute(query, (brand,))
        result = cursor.fetchall()
        return result

    def getToolByName(self, tool_name):
        cursor = self.conn.cursor()
        query = "select * from Tools where tool_name = %s;"
        cursor.execute(query, (tool_name,))
        result = cursor.fetchall()
        return result

    def getToolSuppliesByBrandAndNameAndMaxPrice(self, brand, tool_name, max_price):
        cursor = self.conn.cursor()
        query = "select * from Tools where brand = %s and unit_price <= %s and is_supply = TRUE and tool_name = %s;"
        cursor.execute(query, (brand, max_price, tool_name))
        result = cursor.fetchall()
        return result

    def getToolSuppliesByBrandAndName(self, brand, tool_name):
        cursor = self.conn.cursor()
        query = "select * from Tools where brand = %s and is_supply = TRUE and tool_name = %s;"
        cursor.execute(query, (brand, tool_name))
        result = cursor.fetchall()
        return result

    def getToolSuppliesByBrand(self, brand):
        cursor = self.conn.cursor()
        query = "select * from Tools where brand = %s and is_supply = TRUE;"
        cursor.execute(query, (brand,))
        result = cursor.fetchall()
        return result

    def getToolSuppliesByName(self, tool_name):
        cursor = self.conn.cursor()
        query = "select * from Tools where is_supply = TRUE and tool_name = %s;"
        cursor.execute(query, (tool_name,))
        result = cursor.fetchall()
        return result

    def getToolSuppliesByMaxPrice(self, max_price):
        cursor = self.conn.cursor()
        query = "select * from Tools where is_supply = TRUE and unit_price <= %s;"
        cursor.execute(query, (max_price,))
        result = cursor.fetchall()
        return result

    def getToolRequestsByBrandAndName(self, brand, tool_name):
        cursor = self.conn.cursor()
        query = "select * from Tools where brand = %s and tool_name = %s and is_supply = FALSE;"
        cursor.execute(query, (brand, tool_name))
        result = cursor.fetchall()
        return result

    def getToolRequestsByBrand(self, brand):
        cursor = self.conn.cursor()
        query = "select * from Tools where brand = %s and is_supply = FALSE;"
        cursor.execute(query, (brand,))
        result = cursor.fetchall()
        return result

    def getToolRequestsByName(self, tool_name):
        cursor = self.conn.cursor()
        query = "select * from Tools where tool_name = %s and is_supply = FALSE;"
        cursor.execute(query, (tool_name,))
        result = cursor.fetchall()
        return result

    def insert(self, person_id, brand, tool_name, description, quantity, unit_price, date_posted, curr_quantity,
               is_supply, address_id):
        cursor = self.conn.cursor()
        query = "insert into Tools(person_id, brand, tool_name, description, quantity, unit_price, date_posted, curr_quantity, " \
                "is_supply, address_id) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) returning supply_id;"
        cursor.execute(query, (person_id, brand, tool_name, description, quantity, unit_price, date_posted, curr_quantity,
                               is_supply, address_id))
        tool_id = cursor.fetchone()[0]
        self.conn.commit()
        return tool_id

    def delete(self, tool_id):
        cursor = self.conn.cursor()
        query = "update Tools set curr_quantity = 0 where tool_id = %s;"
        cursor.execute(query, (tool_id,))
        self.conn.commit()
        return tool_id

    def update(self, tool_id, brand, tool_name, description, unit_price, curr_quantity, address_id):
        cursor = self.conn.cursor()
        query = "update Tools set brand = %s, tool_name = %s, description = %s, unit_price = %s, curr_quantity = %s, " \
                "address_id = %s where tool_id = %s;"
        cursor.execute(query, (brand, tool_name, description, unit_price, curr_quantity, address_id, tool_id))
        self.conn.commit()
        return tool_id
