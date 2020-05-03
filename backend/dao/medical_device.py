from backend.config.dbconfig import pg_config
import psycopg2

class MedicalDeviceDAO:
    def __init__(self):

        connection_url = "dbname=%s user=%s password=%s" % (pg_config['dbname'],
                                                            pg_config['user'],
                                                            pg_config['passwd'])
        self.conn = psycopg2._connect(connection_url)

    def getAllMedicalDevice(self):
        cursor = self.conn.cursor()
        query = "select * from MedicalDevices;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllMedicalDeviceSupplies(self):
        cursor = self.conn.cursor()
        query = "select * from MedicalDevices where is_supply = TRUE;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllMedicalDeviceRequests(self):
        cursor = self.conn.cursor()
        query = "select * from MedicalDevices where is_supply = FALSE;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllAvailableMedicalDeviceSupplies(self):
        cursor = self.conn.cursor()
        query = "select * from MedicalDevices where is_supply = TRUE and curr_quantity > 0;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllUnfulfilledMedicalDeviceRequests(self):
        cursor = self.conn.cursor()
        query = "select * from MedicalDevices where is_supply = FALSE and curr_quantity > 0;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getMedicalDeviceById(self, meddical_dev_id):
        cursor = self.conn.cursor()
        query = "select * from MedicalDevices where meddical_dev_id = %s;"
        cursor.execute(query, (meddical_dev_id,))
        result = cursor.fetchone()
        return result

    def getMedicalDeviceByPersonId(self, person_id):
        cursor = self.conn.cursor()
        query = "select * from MedicalDevices where person_id = %s;"
        cursor.execute(query, (person_id,))
        result = cursor.fetchall()
        return result

    def getMedicalDeviceSuppliesByPersonId(self, person_id):
        cursor = self.conn.cursor()
        query = "select * from MedicalDevices where person_id = %s and is_supply = TRUE;"
        cursor.execute(query, (person_id,))
        result = cursor.fetchall()
        return result

    def getMedicalDeviceRequestsByPersonId(self, person_id):
        cursor = self.conn.cursor()
        query = "select * from MedicalDevices where person_id = %s and is_supply = FALSE;"
        cursor.execute(query, (person_id,))
        result = cursor.fetchall()
        return result

    def getMedicalDeviceByBrandAndUsage(self, brand, usage):
        cursor = self.conn.cursor()
        query = "select * from MedicalDevices where brand = %s and usage = %s;"
        cursor.execute(query, (brand, usage))
        result = cursor.fetchall()
        return result

    def getMedicalDeviceByBrand(self, brand):
        cursor = self.conn.cursor()
        query = "select * from MedicalDevices where brand = %s;"
        cursor.execute(query, (brand,))
        result = cursor.fetchall()
        return result

    def getMedicalDeviceByUsage(self, usage):
        cursor = self.conn.cursor()
        query = "select distinct med_id, person_id, brand, description, quantity, unit_price, date_offered, " \
                "curr_quantity, is_supply, address_id from MedicalDevices where usage = %s;"
        cursor.execute(query, (usage,))
        result = cursor.fetchall()
        return result

    def getMedicalDeviceSuppliesByBrandAndUsageAndMaxPrice(self, brand, usage, max_price):
        cursor = self.conn.cursor()
        query = "select distinct med_id, person_id, brand, description, quantity, unit_price, date_offered, " \
                "curr_quantity, is_supply, address_id from MedicalDevices where "\
                "brand = %s and unit_price <= %s and usage = %s is_supply = TRUE;"
        cursor.execute(query, (brand, max_price, usage))
        result = cursor.fetchall()
        return result

    def getMedicalDeviceSuppliesByBrandAndUsage(self, brand, usage):
        cursor = self.conn.cursor()
        query = "select distinct med_id, person_id, brand, description, quantity, unit_price, date_offered, " \
                "curr_quantity, is_supply, address_id from MedicalDevices where "\
                "brand = %s and usage = %s and is_supply = TRUE;"
        cursor.execute(query, (brand, usage))
        result = cursor.fetchall()
        return result

    def getMedicalDeviceSuppliesByBrand(self, brand):
        cursor = self.conn.cursor()
        query = "select * from MedicalDevices where brand = %s and is_supply = TRUE;"
        cursor.execute(query, (brand,))
        result = cursor.fetchall()
        return result

    def getMedicalDeviceSuppliesByUsage(self, usage):
        cursor = self.conn.cursor()
        query = "select distinct med_id, person_id, brand, description, quantity, unit_price, date_offered, " \
                "curr_quantity, is_supply, address_id from MedicalDevices where "\
                "usage = %s and is_supply = TRUE;"
        cursor.execute(query, (usage,))
        result = cursor.fetchall()
        return result

    def getMedicalDeviceSuppliesByMaxPrice(self, max_price):
        cursor = self.conn.cursor()
        query = "select * from MedicalDevices where is_supply = TRUE and unit_price <= %s;"
        cursor.execute(query, (max_price,))
        result = cursor.fetchall()
        return result

    def getMedicalDeviceRequestsByBrandAndUsage(self, brand, usage):
        cursor = self.conn.cursor()
        query = "select distinct med_id, person_id, brand, description, quantity, unit_price, date_offered, " \
                "curr_quantity, is_supply, address_id from MedicalDevices where "\
                "brand = %s and usage = %s and is_supply = FALSE;"
        cursor.execute(query, (brand, usage))
        result = cursor.fetchall()
        return result

    def getMedicalDeviceRequestsByBrand(self, brand):
        cursor = self.conn.cursor()
        query = "select * from MedicalDevices where brand = %s and is_supply = FALSE;"
        cursor.execute(query, (brand,))
        result = cursor.fetchall()
        return result

    def getMedicalDeviceRequestsByUsage(self, usage):
        cursor = self.conn.cursor()
        query = "select distinct med_id, person_id, brand, description, quantity, unit_price, date_offered, " \
                "curr_quantity, is_supply, address_id from MedicalDevices where "\
                "usage = %s and is_supply = FALSE;"
        cursor.execute(query, (usage,))
        result = cursor.fetchall()
        return result

    def insert(self, person_id, brand, description, quantity, unit_price, date_posted, curr_quantity,
               is_supply, address_id):
        cursor = self.conn.cursor()

        query = "insert into MedicalDevices(person_id, brand, description, quantity, unit_price, date_posted, " \
                "curr_quantity, usage, is_supply, address_id) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) " \
                "returning supply_id;"
        cursor.execute(query, (person_id, brand, description, quantity, unit_price, date_posted, curr_quantity,
                               is_supply, address_id))

        meddical_dev_id = cursor.fetchone()[0]

        self.conn.commit()
        return meddical_dev_id

    def delete(self, meddical_dev_id):
        cursor = self.conn.cursor()
        query = "update MedicalDevices set curr_quantity = 0 where meddical_dev_id = %s;"
        cursor.execute(query, (meddical_dev_id,))
        self.conn.commit()
        return meddical_dev_id

    def update(self, meddical_dev_id, brand, description, unit_price, curr_quantity, address_id, usage):
        cursor = self.conn.cursor()
        query = "update MedicalDevices set brand = %s, description = %s, unit_price = %s, curr_quantity = %s, " \
                "usage = %s, address_id = %s where meddical_dev_id = %s;"
        cursor.execute(query, (brand, description, unit_price, curr_quantity, usage, address_id, meddical_dev_id))
        self.conn.commit()
        return meddical_dev_id