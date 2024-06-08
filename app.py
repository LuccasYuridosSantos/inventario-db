from http import HTTPStatus

from flask import jsonify, request, Flask

from constants import EMPLOYEE_EXISTS, EMPLOYEE_ADDED, EMPLOYEE_NOT_FOUND, NO_UPDATE_DATA, EMPLOYEE_UPDATED, \
    ASSET_REMOVED, EMPLOYEE_HAS_ASSETS, EMPLOYEE_DELETED
from funcionario import EmployeeBuilder, EmployeeService
from mongo_connection import mongo_connection
from validate import validate_data, validate_asset, VALID_ASSETS

app = Flask(__name__)

collection = mongo_connection()
builder = EmployeeBuilder()
service = EmployeeService(collection, builder)

def create_response(message, status):
    return jsonify({'message': message}), status


@app.post('/api/funcionarios')
def insert_employee():
    data = request.get_json()
    error, status = validate_data(data, ['cpf', 'nome'])

    if error:
        return create_response(error, status)

    cpf = data['cpf']
    if collection.find_one({'cpf': cpf}):
        return create_response(EMPLOYEE_EXISTS, HTTPStatus.BAD_REQUEST)

    new_employee = service.create_employee(data)
    collection.insert_one(new_employee)
    return create_response(EMPLOYEE_ADDED, HTTPStatus.CREATED)


@app.get('/api/funcionarios')
def find_all():
    employee = list(collection.find({}, {'_id': 0}))
    return jsonify(employee)


@app.get('/api/funcionarios/<cpf>')
def find_employ_by_cpf(cpf):
    employee = collection.find_one({'cpf': cpf}, {'_id': 0})
    if employee:
        return jsonify(employee)
    return create_response(EMPLOYEE_NOT_FOUND, HTTPStatus.NOT_FOUND)


@app.get('/api/funcionarios/<cpf>')
def update_employee(cpf):
    data = request.get_json()
    fields_to_update = {key: value for key, value in data.items() if key == 'nome'}
    if not fields_to_update:
        return create_response(NO_UPDATE_DATA, HTTPStatus.BAD_REQUEST)

    updated = collection.update_one({'cpf': cpf}, {'$set': fields_to_update})
    if updated.matched_count:
        return create_response(EMPLOYEE_UPDATED, HTTPStatus.OK)
    return create_response(EMPLOYEE_NOT_FOUND, HTTPStatus.NOT_FOUND)


@app.put('/api/funcionarios/<cpf>/<asset>')
def update_asset(cpf, asset):
    error = validate_asset(asset)
    if error:
        return error

    data = request.get_json()
    fields_to_update = {f"{asset}.{key}": value for key, value in data.items()}
    updated = collection.update_one({'cpf': cpf}, {'$set': fields_to_update})
    if updated.matched_count:
        return create_response(status=HTTPStatus.OK, message=None)
    return create_response(EMPLOYEE_NOT_FOUND, HTTPStatus.NOT_FOUND)


@app.delete('/api/funcionarios/<cpf>/<asset>')
def delete_asset(cpf, asset):
    error = validate_asset(asset)

    if error:
        return error

    fields_to_update = {f"{asset}.{field}": None for field in ['modelo', 'tag', 'versao', 'caracteristicas']}
    updated = collection.update_one({'cpf': cpf}, {'$set': fields_to_update})
    if updated.matched_count:
        return create_response(ASSET_REMOVED.format(asset), HTTPStatus.OK)
    return create_response(EMPLOYEE_NOT_FOUND, HTTPStatus.NOT_FOUND)


@app.delete('/api/funcionarios/<cpf>')
def delete_employee(cpf):
    employee = collection.find_one({'cpf': cpf})
    if employee:
        for asset in VALID_ASSETS:
            if employee.get(asset):
                if isinstance(employee[asset], dict) and any(employee[asset].values()):
                    return create_response(EMPLOYEE_HAS_ASSETS, HTTPStatus.BAD_REQUEST)
                elif employee[asset] is not None:
                    return create_response(EMPLOYEE_HAS_ASSETS, HTTPStatus.BAD_REQUEST)
        collection.delete_one({'cpf': cpf})
        return create_response(EMPLOYEE_DELETED, HTTPStatus.OK)
    return create_response(EMPLOYEE_NOT_FOUND, HTTPStatus.NOT_FOUND)


if __name__ == '__main__':
    app.run(debug=True)
