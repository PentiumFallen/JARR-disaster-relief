from flask import jsonify
from backend.dao.resource import ResourceDAO


class ResourceHandler:

    def build_resource_dict(self, row):
        #ToDo: Check what Python does with null values in columns!
        if not row[3]:
            result = {
                'resource_id': row[0],
                'category': row[1],
                'person_id': row[2],
                'name': row[4],
                'quantity': row[5],
                'brand': row[6],
            }
        else:
            result = {
                'resource_id': row[0],
                'category': row[1],
                'subcategory': row[2],
                'person_id': row[3],
                'name': row[4],
                'quantity': row[5],
                'brand': row[6],
            }
            return result

    def build_resource_attributes(self, resource_id, category_id, person_id, name, quantity, brand):
        result = {
            'resource_id': resource_id,
            'category_id': category_id,
            'person_id': person_id,
            'name': name,
            'quantity': quantity,
            'brand': brand,
        }
        return result

    def build_resource_count(self, row):
        result = {
            'category': row[0],
            'amount': row[1]
        }
        return result

    def get_all_resource(self):
        dao = ResourceDAO()
        resource_list = dao.getAllResource()
        result_list = []
        for row in resource_list:
            result = self.build_resource_dict(row)
            result_list.append(result)
        return jsonify(Resources=result_list)

    def get_available_resource(self):
        dao = ResourceDAO()
        resource_list = dao.getAllAvailableResource()
        result_list = []
        for row in resource_list:
            result = self.build_resource_dict(row)
            result_list.append(result)
        return jsonify(Needed_Resources=result_list)

    def get_resource_by_person_id(self):
        dao = ResourceDAO()
        count_list = dao.getResourceByPersonId()
        result_list = []
        for row in count_list:
            result = self.build_resource_count(row)
            result_list.append(result)
        return jsonify(Resources=result_list)

    def get_resource_by_id(self, resource_id):
        dao = ResourceDAO()
        row = dao.getResourceById(resource_id)
        if not row:
            return jsonify(Error="Post Not Found"), 404
        else:
            result = self.build_resource_dict(row)
        return jsonify(Resources_Posts=result)

    def get_total_resource_per_category(self):
        dao = ResourceDAO()
        count_list = dao.getTotalResourcePerCategory()
        result_list = []
        for row in count_list:
            result = self.build_supply_count(row)
            result_list.append(result)
        return jsonify(Available_Resource_Count=result_list)

    def get_total_resource(self):
        dao = ResourceDAO()
        amount = dao.getTotalResource()
        return jsonify(Total_Resources=amount)