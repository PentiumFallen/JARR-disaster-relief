from flask import jsonify
from backend.utility import senate_district
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

    def build_address_attributes(self, address_id, address, city, zip_code):
        result = {
            'address_id': address_id,
            'address': address,
            'city': city,
            'district': senate_district[city.lower()],
            'zip_code': zip_code,
        }
        return result

    def get_address_by_id(self, address_id):
        dao = AddressDao()
        row = dao.getAddressById(address_id)
        if not row:
            return jsonify(Error="Person Not Found"), 404
        else:
            result = self.build_address_dict(row)
        return jsonify(Address=result)

    def insert_address(self, form):
        if len(form) != 3:
            return jsonify(Error="Malformed post request"), 400
        else:
            dao = AddressDao()
            address = form['address']
            city = form['city']
            zip_code = form['zip_code']

            if address and city and zip_code:
                address_id = dao.insert(address, city, zip_code)
                result = self.build_address_attributes(address_id, address, city, zip_code)
                return jsonify(Address=result), 201

            else:
                return jsonify(Error="Unexpected attributes in post request"), 400
