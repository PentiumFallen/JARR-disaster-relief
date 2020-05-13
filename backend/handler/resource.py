from flask import jsonify
from backend.dao.resource import ResourceDAO


class ResourceHandler:

    def build_resource_dict(self, row):
        result = {
            'resource_id': row[0],
            'category': row[1],
            'subcategory': row[2],
            'person_id': row[3],
            'name': row[4],
            'quantity': row[5]
        }
        return result

    def build_resource_attributes(self, resource_id, category_id, person_id, name, quantity):
        result = {
            'resource_id': resource_id,
            'category_id': category_id,
            'person_id': person_id,
            'name': name,
            'quantity': quantity
        }
        return result

    def build_resource_count(self, row):
        result = {
            'category': row[0],
            'amount': row[1]
        }
        return result

    def get_all_resources(self):
        dao = ResourceDAO()
        resource_list = dao.getAllResources()
        result_list = []
        for row in resource_list:
            result = self.build_resource_dict(row)
            result_list.append(result)
        return jsonify(Resources=result_list)

    def get_available_resource(self):
        dao = ResourceDAO()
        resource_list = dao.getAllAvailableResources()
        result_list = []
        for row in resource_list:
            result = self.build_resource_dict(row)
            result_list.append(result)
        return jsonify(Needed_Resources=result_list)

    def get_resources_by_person_id(self, person_id):
        dao = ResourceDAO()
        count_list = dao.getResourcesByPersonId(person_id)
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
        count_list = dao.getTotalResourcesPerCategory()
        result_list = []
        for row in count_list:
            result = self.build_resource_count(row)
            result_list.append(result)
        return jsonify(Available_Resource_Count=result_list)

    def get_total_resource(self):
        dao = ResourceDAO()
        amount = dao.getTotalResources()
        return jsonify(Total_Resources=amount)

    def update_resource(self, resource_id, quantity):
        dao = ResourceDAO()
        if not dao.updateResource(resource_id):
            return jsonify(Error="Post not found."), 404
        else:
                if int(quantity) <= 0:
                    return jsonify(Error="Cannot put non-positive value in quantity"), 400
                else:
                    dao.updateResource(resource_id, quantity)
                    row = dao.getResourceById(resource_id)
                    result = self.build_resource_dict(row)
                    return jsonify(Update_Resource=result), 200
