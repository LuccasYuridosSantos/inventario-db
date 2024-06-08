# API de Inventário de Ativos de TI

Esta API permite realizar as principais operações de CRUD (Create, Read, Update, Delete) para gerenciar um inventário de ativos de TI de funcionários, salvando os dados em um banco de dados MongoDB.

## Instalação

Clone o repositório:

```bash
git clone <https://github.com/LuccasYuridosSantos/inventario-db.git>
```

Crie um ambiente virtual e instale as dependências:

```bash
python -m venv venv
source venv/bin/activate   # No Windows use: venv\Scripts\activate
pip install -r requirements.txt
```

Configure a variável de ambiente MONGO_URI com a URI do seu MongoDB:

```bash
export MONGO_URI='mongodb://localhost:27017/'
```

Execute a aplicação:

```bash
python app.py
```

### Endpoints

#### Adicionar Funcionário
Adiciona um novo funcionário com os ativos opcionais.
- **URL:** `/api/funcionarios`
- **Método:** `POST`
- **Dados JSON:**
  ```json
  {
      "cpf": "12345678903",
      "nome": "João Silva",
      "notebook_modelo": "Dell XPS 13",
      "notebook_tag": "TAG654",
      "notebook_versao": "2022",
      "notebook_caracteristicas": "Core i7, 16GB RAM, 512GB SSD",
      "monitor1_modelo": "Dell 24'",
      "monitor2_modelo": "HP 24'",
      "teclado_modelo": "Razer BlackWidow",
      "mouse_modelo": "Razer DeathAdder",
      "nobreak_modelo": "CyberPower 1500VA",
      "desktop_modelo": "HP EliteDesk",
      "desktop_tag": "TAG321",
      "desktop_versao": "2022",
      "desktop_caracteristicas": "Core i7, 32GB RAM, 1TB SSD",
      "headset_modelo": "HyperX Cloud II",
      "celular_modelo": "iPhone 13",
      "celular_numero": "987654321",
      "acessorios": "Adaptador USB-C"
  }
  ```
- **Resposta:**
  ```json
  {
      "message": "Funcionário adicionado com sucesso!"
  }
  ```

#### Listar Funcionários
Retorna uma lista de todos os funcionários.
- **URL:** `/api/funcionarios`
- **Método:** `GET`
- **Resposta:**
  ```json
  [
      {
          "cpf": "12345678903",
          "nome": "João Silva",
          "notebook": {...},
          ...
      }
  ]
  ```

#### Obter Funcionário
Retorna as informações de um funcionário específico.
- **URL:** `/api/funcionarios/<cpf>`
- **Método:** `GET`
- **Resposta:**
  ```json
  {
      "cpf": "12345678903",
      "nome": "João Silva",
      "notebook": {...},
      ...
  }
  ```

#### Atualizar Funcionário
Atualiza o nome de um funcionário.
- **URL:** `/api/funcionarios/<cpf>`
- **Método:** `PUT`
- **Dados JSON:**
  ```json
  {
      "nome": "João Pedro Silva"
  }
  ```
- **Resposta:**
  ```json
  {
      "message": "Funcionário atualizado com sucesso!"
  }
  ```

#### Atualizar Ativo
Atualiza as informações de um ativo específico de um funcionário.
- **URL:** `/api/funcionarios/<cpf>/<asset>`
- **Método:** `PUT`
- **Dados JSON:**
  ```json
  {
      "modelo": "Novo Modelo",
      "tag": "Nova Tag",
      "versao": "Nova Versão",
      "caracteristicas": "Novas Características"
  }
  ```
- **Resposta:**
  ```json
  {
      "message": "Ativo atualizado com sucesso!"
  }
  ```

#### Remover Ativo
Remove as informações de um ativo específico de um funcionário.
- **URL:** `/api/funcionarios/<cpf>/<asset>`
- **Método:** `DELETE`
- **Resposta:**
  ```json
  {
      "message": "Ativo removido com sucesso!"
  }
  ```

#### Remover Funcionário
Remove um funcionário, se ele não possuir ativos.
- **URL:** `/api/funcionarios/<cpf>`
- **Método:** `DELETE`
- **Resposta:**
  ```json
  {
      "message": "Funcionário excluído com sucesso!"
  }
  ```