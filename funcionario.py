class EmployeeBuilder:
    def __init__(self):
        self.funcionario = {}

    def with_cpf(self, cpf):
        self.funcionario["cpf"] = cpf
        return self

    def with_nome(self, nome):
        self.funcionario["nome"] = nome
        return self

    def with_notebook(self, modelo, tag, versao, caracteristicas):
        notebook = {
            "modelo": modelo,
            "tag": tag,
            "versao": versao,
            "caracteristicas": caracteristicas
        }
        self.funcionario["notebook"] = notebook
        return self

    def with_monitor1(self, monitor1):
        self.funcionario["monitor1"] = {"modelo": monitor1}
        return self

    def with_monitor2(self, monitor2):
        self.funcionario["monitor2"] = {"modelo": monitor2}
        return self

    def with_teclado(self, teclado):
        self.funcionario["teclado"] = {"modelo": teclado}
        return self

    def with_mouse(self, mouse):
        self.funcionario["mouse"] = {"modelo": mouse}
        return self

    def with_nobreak(self, nobreak):
        self.funcionario["nobreak"] = {"modelo": nobreak}
        return self

    def with_desktop(self, modelo, tag, versao, caracteristicas):
        desktop = {
            "modelo": modelo,
            "tag": tag,
            "versao": versao,
            "caracteristicas": caracteristicas
        }
        self.funcionario["desktop"] = desktop
        return self

    def with_headset(self, headset):
        self.funcionario["headset"] = {"modelo": headset}
        return self

    def with_celular(self, modelo, numero):
        celular = {
            "modelo": modelo,
            "numero": numero
        }
        self.funcionario["celular"] = celular
        return self

    def with_acessorios(self, acessorios):
        self.funcionario["acessorios"] = acessorios
        return self

    def build(self):
        return self.funcionario


class EmployeeService:
    def __init__(self, collection, builder):
        self.collection = collection
        self.builder = builder

    def create_employee(self, data):
        return (self.builder.with_cpf(data['cpf'])
                .with_nome(data['nome'])
                .with_notebook(data.get('notebook_modelo'), data.get('notebook_tag'),
                               data.get('notebook_versao'), data.get('notebook_caracteristicas'))
                .with_monitor1(data.get('monitor1_modelo'))
                .with_monitor2(data.get('monitor2_modelo'))
                .with_teclado(data.get('teclado_modelo'))
                .with_mouse(data.get('mouse_modelo'))
                .with_nobreak(data.get('nobreak_modelo'))
                .with_desktop(data.get('desktop_modelo'), data.get('desktop_tag'), data.get('desktop_versao'),
                              data.get('desktop_caracteristicas'))
                .with_headset(data.get('headset_modelo'))
                .with_celular(data.get('celular_modelo'), data.get('celular_numero'))
                .with_acessorios(data.get('acessorios'))
                .build())