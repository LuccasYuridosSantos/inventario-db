from flask import Flask, request, jsonify
from pymongo import MongoClient
import os

app = Flask(__name__)

MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
client = MongoClient(MONGO_URI)
db = client['inventario_db']
collection = db['funcionarios']


def create_response(message, status):
    return jsonify({'message': message}), status


def validate_data(data, required_fields):
    if not data:
        return 'Nenhum dado enviado!', 400
    for field in required_fields:
        if not data.get(field):
            return f'{field} é obrigatório!', 400
    return None, None

def validate_asset(asset):
    valid_assets = [
        "notebook", "monitor1", "monitor2", "teclado", "mouse", "nobreak",
        "desktop", "headset", "celular", "acessorios"
    ]
    if asset not in valid_assets:
        return create_response('Ativo inválido!', 400)
    return None


@app.route('/api/funcionarios', methods=['POST'])
def add_funcionario():
    data = request.get_json()
    error, status = validate_data(data, ['cpf', 'nome'])
    if error:
        return create_response(error, status)

    cpf = data['cpf']
    if collection.find_one({'cpf': cpf}):
        return create_response('Funcionário com este CPF já existe!', 400)

    novo_funcionario = {
        "cpf": cpf,
        "nome": data['nome'],
        "notebook": {
            "modelo": data.get('notebook_modelo'),
            "tag": data.get('notebook_tag'),
            "versao": data.get('notebook_versao'),
            "caracteristicas": data.get('notebook_caracteristicas')
        },
        "monitor1": {"modelo": data.get('monitor1_modelo')},
        "monitor2": {"modelo": data.get('monitor2_modelo')},
        "teclado": {"modelo": data.get('teclado_modelo')},
        "mouse": {"modelo": data.get('mouse_modelo')},
        "nobreak": {"modelo": data.get('nobreak_modelo')},
        "desktop": {
            "modelo": data.get('desktop_modelo'),
            "tag": data.get('desktop_tag'),
            "versao": data.get('desktop_versao'),
            "caracteristicas": data.get('desktop_caracteristicas')
        },
        "headset": {"modelo": data.get('headset_modelo')},
        "celular": {
            "modelo": data.get('celular_modelo'),
            "numero": data.get('celular_numero')
        },
        "acessorios": data.get('acessorios')
    }
    collection.insert_one(novo_funcionario)
    return create_response('Funcionário adicionado com sucesso!', 201)


@app.route('/api/funcionarios', methods=['GET'])
def get_funcionarios():
    funcionarios = list(collection.find({}, {'_id': 0}))
    return jsonify(funcionarios)


@app.route('/api/funcionarios/<cpf>', methods=['GET'])
def get_funcionario(cpf):
    funcionario = collection.find_one({'cpf': cpf}, {'_id': 0})
    if funcionario:
        return jsonify(funcionario)
    return create_response('Funcionário não encontrado!', 404)


@app.route('/api/funcionarios/<cpf>', methods=['PUT'])
def update_funcionario(cpf):
    data = request.get_json()
    fields_to_update = {key: value for key, value in data.items() if key == 'nome'}
    if not fields_to_update:
        return create_response('Nenhum dado enviado para atualização!', 400)

    updated = collection.update_one({'cpf': cpf}, {'$set': fields_to_update})
    if updated.matched_count:
        return create_response('Funcionário atualizado com sucesso!', 200)
    return create_response('Funcionário não encontrado!', 404)


@app.route('/api/funcionarios/<cpf>/<asset>', methods=['PUT'])
def update_asset(cpf, asset):
    error = validate_asset(asset)
    if error:
        return error

    data = request.get_json()
    fields_to_update = {f"{asset}.{key}": value for key, value in data.items()}
    updated = collection.update_one({'cpf': cpf}, {'$set': fields_to_update})
    if updated.matched_count:
        return create_response(f'{asset} atualizado com sucesso!', 200)
    return create_response('Funcionário não encontrado!', 404)


@app.route('/api/funcionarios/<cpf>/<asset>', methods=['DELETE'])
def delete_asset(cpf, asset):
    error = validate_asset(asset)
    if error:
        return error

    fields_to_update = {f"{asset}.{field}": None for field in ['modelo', 'tag', 'versao', 'caracteristicas']}
    updated = collection.update_one({'cpf': cpf}, {'$set': fields_to_update})
    if updated.matched_count:
        return create_response(f'{asset} removido com sucesso!', 200)
    return create_response('Funcionário não encontrado!', 404)


@app.route('/api/funcionarios/<cpf>', methods=['DELETE'])
def delete_funcionario(cpf):
    funcionario = collection.find_one({'cpf': cpf})
    if funcionario:
        ativos = ['notebook', 'monitor1', 'monitor2', 'teclado', 'mouse', 'nobreak', 'desktop', 'headset', 'celular',
                  'acessorios']
        for ativo in ativos:
            if funcionario.get(ativo):
                if isinstance(funcionario[ativo], dict) and any(funcionario[ativo].values()):
                    return create_response('Funcionário possui ativos e não pode ser excluído!', 400)
                elif funcionario[ativo] is not None:
                    return create_response('Funcionário possui ativos e não pode ser excluído!', 400)
        collection.delete_one({'cpf': cpf})
        return create_response('Funcionário excluído com sucesso!', 200)
    return create_response('Funcionário não encontrado!', 404)


if __name__ == '__main__':
    app.run(debug=True)
