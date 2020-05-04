from flask import jsonify
from backend.dao.Address import AddressDao


class AddressHandler:
    def build_address_dict(self, row):
        result = {
            'address_id': row[0],
            'address': row[1],
            'city': row[2],
            'district': row[3],
            'zip_code': row[4],
        }
        return result

    def build_address_attributes(self, address_id, address, city, district, zip_code):
        result = {
            'address_id': address_id,
            'address': address,
            'city': city,
            'district': district,
            'zip_code': zip_code,
        }
        return result

    def get_address_by_id(self, address_id):
        dao = AddressDao()
        row = dao.getAddressById(address_id)
        if not row:
            return jsonify(Error="Person Not Found"), 404
        else:
            result = self.build_person_dict(row)
        return jsonify(Address=result)
