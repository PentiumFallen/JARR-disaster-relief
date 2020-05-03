from backend.config.dbconfig import pg_config
import psycopg2

class MedicationDAO:
    def __init__(self):

        connection_url = "dbname=%s user=%s password=%s" % (pg_config['dbname'],
                                                            pg_config['user'],
                                                            pg_config['passwd'])
        self.conn = psycopg2._connect(connection_url)

    def getAllMedication(self):
        cursor = self.conn.cursor()
        query = "select * from Medications;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllMedicationSupplies(self):
        cursor = self.conn.cursor()
        query = "select * from Medications where is_supply = TRUE;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllMedicationRequests(self):
        cursor = self.conn.cursor()
        query = "select * from Medications where is_supply = FALSE;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllAvailableMedicationSupplies(self):
        cursor = self.conn.cursor()
        query = "select * from Medications where is_supply = TRUE and curr_quantity > 0;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllUnfulfilledMedicationRequests(self):
        cursor = self.conn.cursor()
        query = "select * from Medications where is_supply = FALSE and curr_quantity > 0;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getMedicationById(self, medication_id):
        cursor = self.conn.cursor()
        query = "select * from Medications where medication_id = %s;"
        cursor.execute(query, (medication_id,))
        result = cursor.fetchone()
        return result

    def getMedicationIngredientById(self, ing_id):
        cursor = self.conn.cursor()
        query = "select * from MedicationIngredients where ing_id = %s;"
        cursor.execute(query, (ing_id,))
        result = cursor.fetchone()
        return result

    def getMedicationIngredientsById(self, medication_id):
        cursor = self.conn.cursor()
        query = "select * from MedicationIngredients where medication_id = %s;"
        cursor.execute(query, (medication_id,))
        result = cursor.fetchone()
        return result

    def getMedicationByPersonId(self, person_id):
        cursor = self.conn.cursor()
        query = "select * from Medications where person_id = %s;"
        cursor.execute(query, (person_id,))
        result = cursor.fetchall()
        return result

    def getMedicationSuppliesByPersonId(self, person_id):
        cursor = self.conn.cursor()
        query = "select * from Medications where person_id = %s and is_supply = TRUE;"
        cursor.execute(query, (person_id,))
        result = cursor.fetchall()
        return result

    def getMedicationRequestsByPersonId(self, person_id):
        cursor = self.conn.cursor()
        query = "select * from Medications where person_id = %s and is_supply = FALSE;"
        cursor.execute(query, (person_id,))
        result = cursor.fetchall()
        return result

    def getMedicationByBrandAndUsage(self, brand, usage):
        cursor = self.conn.cursor()
        query = "select * from Medications natural inner join MedicationIngredient where brand = %s and usage = %s;"
        cursor.execute(query, (brand, usage))
        result = cursor.fetchall()
        return result

    def getMedicationByBrand(self, brand):
        cursor = self.conn.cursor()
        query = "select * from Medications where brand = %s;"
        cursor.execute(query, (brand,))
        result = cursor.fetchall()
        return result

    def getMedicationByUsage(self, usage):
        cursor = self.conn.cursor()
        query = "select distinct med_id, person_id, brand, description, quantity, unit_price, date_offered, " \
                "curr_quantity, is_supply, address_id from Medications natural inner join MedicationIngredients where "\
                "usage = %s;"
        cursor.execute(query, (usage,))
        result = cursor.fetchall()
        return result

    def getMedicationSuppliesByBrandAndUsageAndMaxPrice(self, brand, usage, max_price):
        cursor = self.conn.cursor()
        query = "select distinct med_id, person_id, brand, description, quantity, unit_price, date_offered, " \
                "curr_quantity, is_supply, address_id from Medications natural inner join MedicationIngredients where "\
                "brand = %s and unit_price <= %s and usage = %s is_supply = TRUE;"
        cursor.execute(query, (brand, max_price, usage))
        result = cursor.fetchall()
        return result

    def getMedicationSuppliesByBrandAndIngredientAndMaxPrice(self, brand, ingredient, max_price):
        cursor = self.conn.cursor()
        query = "select distinct med_id, person_id, brand, description, quantity, unit_price, date_offered, " \
                "curr_quantity, is_supply, address_id from Medications natural inner join MedicationIngredients where "\
                "brand = %s and unit_price <= %s and ing_name = %s is_supply = TRUE;"
        cursor.execute(query, (brand, max_price, ingredient))
        result = cursor.fetchall()
        return result

    def getMedicationSuppliesByBrandAndUsage(self, brand, usage):
        cursor = self.conn.cursor()
        query = "select distinct med_id, person_id, brand, description, quantity, unit_price, date_offered, " \
                "curr_quantity, is_supply, address_id from Medications natural inner join MedicationIngredients where "\
                "brand = %s and usage = %s and is_supply = TRUE;"
        cursor.execute(query, (brand, usage))
        result = cursor.fetchall()
        return result

    def getMedicationSuppliesByBrandAndIngredient(self, brand, ingredient):
        cursor = self.conn.cursor()
        query = "select distinct med_id, person_id, brand, description, quantity, unit_price, date_offered, " \
                "curr_quantity, is_supply, address_id from Medications natural inner join MedicationIngredients where "\
                "brand = %s and ing_name = %s and is_supply = TRUE;"
        cursor.execute(query, (brand, ingredient))
        result = cursor.fetchall()
        return result

    def getMedicationSuppliesByBrand(self, brand):
        cursor = self.conn.cursor()
        query = "select * from Medications where brand = %s and is_supply = TRUE;"
        cursor.execute(query, (brand,))
        result = cursor.fetchall()
        return result

    def getMedicationSuppliesByUsage(self, usage):
        cursor = self.conn.cursor()
        query = "select distinct med_id, person_id, brand, description, quantity, unit_price, date_offered, " \
                "curr_quantity, is_supply, address_id from Medications natural inner join MedicationIngredients where "\
                "usage = %s and is_supply = TRUE;"
        cursor.execute(query, (usage,))
        result = cursor.fetchall()
        return result

    def getMedicationSuppliesByIngredient(self, ingredient):
        cursor = self.conn.cursor()
        query = "select distinct med_id, person_id, brand, description, quantity, unit_price, date_offered, " \
                "curr_quantity, is_supply, address_id from Medications natural inner join MedicationIngredients where "\
                "ing_name = %s and is_supply = TRUE;"
        cursor.execute(query, (ingredient,))
        result = cursor.fetchall()
        return result

    def getMedicationSuppliesByMaxPrice(self, max_price):
        cursor = self.conn.cursor()
        query = "select * from Medications where is_supply = TRUE and unit_price <= %s;"
        cursor.execute(query, (max_price,))
        result = cursor.fetchall()
        return result

    def getMedicationRequestsByBrandAndUsage(self, brand, usage):
        cursor = self.conn.cursor()
        query = "select distinct med_id, person_id, brand, description, quantity, unit_price, date_offered, " \
                "curr_quantity, is_supply, address_id from Medications natural inner join MedicationIngredients where "\
                "brand = %s and usage = %s and is_supply = FALSE;"
        cursor.execute(query, (brand, usage))
        result = cursor.fetchall()
        return result

    def getMedicationRequestsByBrandAndIngredient(self, brand, ingredient):
        cursor = self.conn.cursor()
        query = "select distinct med_id, person_id, brand, description, quantity, unit_price, date_offered, " \
                "curr_quantity, is_supply, address_id from Medications natural inner join MedicationIngredients where "\
                "brand = %s and ing_name = %s and is_supply = FALSE;"
        cursor.execute(query, (brand, ingredient))
        result = cursor.fetchall()
        return result

    def getMedicationRequestsByBrand(self, brand):
        cursor = self.conn.cursor()
        query = "select * from Medications where brand = %s and is_supply = FALSE;"
        cursor.execute(query, (brand,))
        result = cursor.fetchall()
        return result

    def getMedicationRequestsByUsage(self, usage):
        cursor = self.conn.cursor()
        query = "select distinct med_id, person_id, brand, description, quantity, unit_price, date_offered, " \
                "curr_quantity, is_supply, address_id from Medications natural inner join MedicationIngredients where "\
                "usage = %s and is_supply = FALSE;"
        cursor.execute(query, (usage,))
        result = cursor.fetchall()
        return result

    def getMedicationRequestsByIngredient(self, ingredient):
        cursor = self.conn.cursor()
        query = "select distinct med_id, person_id, brand, description, quantity, unit_price, date_offered, " \
                "curr_quantity, is_supply, address_id from Medications natural inner join MedicationIngredients where " \
                "ing_name = %s and is_supply = FALSE;"
        cursor.execute(query, (ingredient,))
        result = cursor.fetchall()
        return result

    def insert(self, person_id, brand, description, quantity, unit_price, date_posted, curr_quantity,
               is_supply, address_id):
        cursor = self.conn.cursor()

        query = "insert into Medications(person_id, brand, description, quantity, unit_price, date_posted, " \
                "curr_quantity, is_supply, address_id) values (%s, %s, %s, %s, %s, %s, %s, %s, %s) " \
                "returning supply_id;"
        cursor.execute(query, (person_id, brand, description, quantity, unit_price, date_posted, curr_quantity,
                               is_supply, address_id))

        medication_id = cursor.fetchone()[0]

        self.conn.commit()
        return medication_id


    def insertIngredient(self, medication_id, ing_name, usage):
        cursor = self.conn.cursor()

        query = "insert into MedicationIngredients(med_id, ing_name, usage) values (%s, %s, %s) returning ing_id;"
        cursor.execute(query, (medication_id, ing_name, usage))
        ing_name = cursor.fetchone()[0]

        self.conn.commit()
        return ing_name

    def delete(self, medication_id):
        cursor = self.conn.cursor()
        query = "update Medications set curr_quantity = 0 where medication_id = %s;"
        cursor.execute(query, (medication_id,))
        self.conn.commit()
        return medication_id

    def deleteIngredient(self, ing_id):
        cursor = self.conn.cursor()
        query = "delete from MedicationIngredients where ing_id = %s;"
        cursor.execute(query, (ing_id,))
        self.conn.commit()
        return ing_id

    def update(self, medication_id, brand, description, unit_price, curr_quantity, type_id, address_id):
        cursor = self.conn.cursor()
        query = "update Medications set brand = %s, description = %s, unit_price = %s, curr_quantity = %s, " \
                "type_id = %s, address_id = %s where medication_id = %s;"
        cursor.execute(query, (brand, description, unit_price, curr_quantity, type_id, address_id, medication_id))
        self.conn.commit()
        return medication_id
