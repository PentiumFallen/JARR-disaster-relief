from backend.config.dbconfig import pg_config
import psycopg2

class HeavyEquiptmentDAO:
    def __init__(self):

        connection_url = "dbname=%s user=%s password=%s" % (pg_config['dbname'],
                                                            pg_config['user'],
                                                            pg_config['passwd'])
        self.conn = psycopg2._connect(connection_url)

    def getAllHeavyEquipment(self):
        cursor = self.conn.cursor()
        query = "select * from HeavyEquipment;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllHeavyEquipmentSupplies(self):
        cursor = self.conn.cursor()
        query = "select * from HeavyEquipment where is_supply = TRUE;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllHeavyEquipmentRequests(self):
        cursor = self.conn.cursor()
        query = "select * from HeavyEquipment where is_supply = FALSE;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllAvailableHeavyEquipmentSupplies(self):
        cursor = self.conn.cursor()
        query = "select * from HeavyEquipment where is_supply = TRUE and curr_quantity > 0;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllUnfulfilledHeavyEquipmentRequests(self):
        cursor = self.conn.cursor()
        query = "select * from HeavyEquipment where is_supply = FALSE and curr_quantity > 0;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getHeavyEquipmentById(self, heavy_equip_id):
        cursor = self.conn.cursor()
        query = "select * from HeavyEquipment where heavy_equip_id = %s;"
        cursor.execute(query, (heavy_equip_id,))
        result = cursor.fetchone()
        return result

    def getHeavyEquipmentByPersonId(self, person_id):
        cursor = self.conn.cursor()
        query = "select * from HeavyEquipment where person_id = %s;"
        cursor.execute(query, (person_id,))
        result = cursor.fetchall()
        return result

    def getHeavyEquipmentSuppliesByPersonId(self, person_id):
        cursor = self.conn.cursor()
        query = "select * from HeavyEquipment where person_id = %s and is_supply = TRUE;"
        cursor.execute(query, (person_id,))
        result = cursor.fetchall()
        return result

    def getHeavyEquipmentRequestsByPersonId(self, person_id):
        cursor = self.conn.cursor()
        query = "select * from HeavyEquipment where person_id = %s and is_supply = FALSE;"
        cursor.execute(query, (person_id,))
        result = cursor.fetchall()
        return result

    def getHeavyEquipmentByBrandAndName(self, brand, equipment_name):
        cursor = self.conn.cursor()
        query = "select * from HeavyEquipment where brand = %s and equipment_name = %s;"
        cursor.execute(query, (brand, equipment_name))
        result = cursor.fetchall()
        return result

    def getHeavyEquipmentByBrand(self, brand):
        cursor = self.conn.cursor()
        query = "select * from HeavyEquipment where brand = %s;"
        cursor.execute(query, (brand,))
        result = cursor.fetchall()
        return result

    def getHeavyEquipmentByName(self, equipment_name):
        cursor = self.conn.cursor()
        query = "select * from HeavyEquipment where equipment_name = %s;"
        cursor.execute(query, (equipment_name,))
        result = cursor.fetchall()
        return result

    def getHeavyEquipmentSuppliesByBrandAndNameAndMaxPrice(self, brand, equipment_name, max_price):
        cursor = self.conn.cursor()
        query = "select * from HeavyEquipment where brand = %s and unit_price <= %s and is_supply = TRUE and equipment_name = %s;"
        cursor.execute(query, (brand, max_price, equipment_name))
        result = cursor.fetchall()
        return result

    def getHeavyEquipmentSuppliesByBrandAndName(self, brand, equipment_name):
        cursor = self.conn.cursor()
        query = "select * from HeavyEquipment where brand = %s and is_supply = TRUE and equipment_name = %s;"
        cursor.execute(query, (brand, equipment_name))
        result = cursor.fetchall()
        return result

    def getHeavyEquipmentSuppliesByBrand(self, brand):
        cursor = self.conn.cursor()
        query = "select * from HeavyEquipment where brand = %s and is_supply = TRUE;"
        cursor.execute(query, (brand,))
        result = cursor.fetchall()
        return result

    def getHeavyEquipmentSuppliesByName(self, equipment_name):
        cursor = self.conn.cursor()
        query = "select * from HeavyEquipment where is_supply = TRUE and equipment_name = %s;"
        cursor.execute(query, (equipment_name,))
        result = cursor.fetchall()
        return result

    def getHeavyEquipmentSuppliesByMaxPrice(self, max_price):
        cursor = self.conn.cursor()
        query = "select * from HeavyEquipment where is_supply = TRUE and unit_price <= %s;"
        cursor.execute(query, (max_price,))
        result = cursor.fetchall()
        return result

    def getHeavyEquipmentRequestsByBrandAndName(self, brand, equipment_name):
        cursor = self.conn.cursor()
        query = "select * from HeavyEquipment where brand = %s and equipment_name = %s and is_supply = FALSE;"
        cursor.execute(query, (brand, equipment_name))
        result = cursor.fetchall()
        return result

    def getHeavyEquipmentRequestsByBrand(self, brand):
        cursor = self.conn.cursor()
        query = "select * from HeavyEquipment where brand = %s and is_supply = FALSE;"
        cursor.execute(query, (brand,))
        result = cursor.fetchall()
        return result

    def getHeavyEquipmentRequestsByName(self, equipment_name):
        cursor = self.conn.cursor()
        query = "select * from HeavyEquipment where equipment_name = %s and is_supply = FALSE;"
        cursor.execute(query, (equipment_name,))
        result = cursor.fetchall()
        return result

    def insert(self, person_id, brand, equipment_name, description, quantity, unit_price, date_posted, curr_quantity,
               is_supply, address_id):
        cursor = self.conn.cursor()
        query = "insert into HeavyEquipment(person_id, brand, description, quantity, unit_price, date_posted, curr_quantity, " \
                "is_supply, equipment_name, address_id) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) returning supply_id;"
        cursor.execute(query, (person_id, brand, description, quantity, unit_price, date_posted, curr_quantity,
                               is_supply, equipment_name, address_id))
        heavy_equip_id = cursor.fetchone()[0]
        self.conn.commit()
        return heavy_equip_id

    def delete(self, heavy_equip_id):
        cursor = self.conn.cursor()
        query = "update HeavyEquipment set curr_quantity = 0 where heavy_equip_id = %s;"
        cursor.execute(query, (heavy_equip_id,))
        self.conn.commit()
        return heavy_equip_id

    def update(self, heavy_equip_id, brand, equipment_name, description, unit_price, curr_quantity, address_id):
        cursor = self.conn.cursor()
        query = "update HeavyEquipment set brand = %s, equipment_name = %s, description = %s, unit_price = %s, curr_quantity = %s, " \
                "address_id = %s where heavy_equip_id = %s;"
        cursor.execute(query, (brand, equipment_name, description, unit_price, curr_quantity, address_id, heavy_equip_id))
        self.conn.commit()
        return heavy_equip_id
