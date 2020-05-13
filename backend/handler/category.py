from flask import jsonify
from backend.dao.category import CategoryDao

class CategoryHandler:
    def build_full_category_dict(self, row):
        result = {
            'category_id': row[0],
            'category': row[1],
            'subcategory': row[2]
        }
        return result

    def build_category_dict(self, row):
        result = {
            'category': row[0]
        }
        return result

    def build_subcategory_dict(self, row):
        result = {
            'subcategory': row[0]
        }
        return result

    def build_category_attributes(self, category_id, category, subcategory):
        result = {
            'category_id': category_id,
            'category': category,
            'subcategory': subcategory
        }
        return result

    def get_all_full_categories(self):
        dao = CategoryDao()
        supply_list = dao.getAllCategoriesWithSubcategories()
        result_list = []
        for row in supply_list:
            result = self.build_full_category_dict(row)
            result_list.append(result)
        return jsonify(Categories=result_list)

    def get_all_categories(self):
        dao = CategoryDao()
        supply_list = dao.getAllCategories()
        result_list = []
        for row in supply_list:
            result = self.build_category_dict(row)
            result_list.append(result)
        return jsonify(Categories=result_list)

    def get_all_subcategories(self, category):
        dao = CategoryDao()
        supply_list = dao.getSubcategorybyCategory(category)
        result_list = []
        for row in supply_list:
            result = self.build_subcategory_dict(row)
            result_list.append(result)
        return jsonify(Subcategories=result_list)
