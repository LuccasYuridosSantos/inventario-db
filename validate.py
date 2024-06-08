VALID_ASSETS = [
        "notebook", "monitor1", "monitor2", "teclado", "mouse", "nobreak",
        "desktop", "headset", "celular", "acessorios"
    ]


def validate_asset(asset):
    if asset not in VALID_ASSETS:
        return create_response('Ativo inválido!', 400)
    return None

def validate_data(data, required_fields):
    if not data:
        return 'Nenhum dado enviado!', 400
    for field in required_fields:
        if not data.get(field):
            return f'{field} é obrigatório!', 400
    return None, None