# Projeto Flask API - Gerenciamento de Produtos e Vendas

Este projeto é uma API RESTful desenvolvida em Python utilizando o microframework **Flask**. O objetivo principal é fornecer um sistema para gerenciamento de produtos e importação de vendas via arquivos CSV, com autenticação segura.

## 🏗️ Arquitetura e Fundamentos

O projeto segue uma arquitetura modular, separando responsabilidades para facilitar a manutenção e escalabilidade.

### Tecnologias Principais
- **Flask**: Framework web leve para construção da API.
- **MongoDB (PyMongo)**: Banco de dados NoSQL para armazenamento flexível de produtos e vendas.
- **Pydantic**: Biblioteca para validação de dados e definição de esquemas (Models), garantindo que os dados recebidos e enviados estejam corretos.
- **PyJWT**: Utilizado para implementação de autenticação via Json Web Tokens (JWT).

### Estrutura do Projeto
A estrutura de diretórios foi organizada da seguinte forma:

```text
projeto/
├── app/
│   ├── __init__.py      # Factory da aplicação e conexão com banco de dados
│   ├── decorators.py    # Decorators personalizados (ex: autenticação)
│   ├── models/          # Modelos de dados Pydantic
│   └── routes/          # Definição das rotas (Endpoints)
├── config.py            # Configurações de ambiente
├── run.py               # Ponto de entrada da aplicação
└── .env                 # Variáveis de ambiente (Segredos)
```

### Padrões de Projeto (Design Patterns)
1.  **Application Factory**: Definido em `app/__init__.py`, permite criar múltiplas instâncias da aplicação com diferentes configurações (útil para testes).
2.  **Blueprints**: O Flask Blueprint (`main_bp`) é usado para organizar as rotas, mantendo o `app` principal limpo.
3.  **Data Transfer Objects (DTOs)**: Os modelos do Pydantic (`app/models`) atuam como DTOs, validando a entrada (`LoginPayLoad`, `Product`) e formatando a saída (`ProdctDBModel`).

---

## 🚀 Funcionalidades

### 1. Autenticação (JWT)
O sistema possui um endpoint de login que valida credenciais (hardcoded para demonstração: `admin`/`123`).
- **Endpoint**: `POST /login/`
- **Fluxo**: O usuário envia credenciais -> API valida -> Retorna um **Token JWT** com validade de 30 minutos.
- **Segurança**: Rotas protegidas utilizam o decorator `@token_required` que intercepta a requisição e valida o token no header `Authorization`.

### 2. Gerenciamento de Produtos (CRUD)
Operações completas para criar, ler, atualizar e remover produtos.
- **Modelagem**: Os produtos possuem campos como `name`, `price`, `description` e `stock`. O `ObjectId` do MongoDB é tratado e convertido para string nas respostas.
- **Endpoints**:
    - `GET /products/`: Lista todos os produtos (Requer Token).
    - `GET /products/<id>`: Detalhes de um produto específico (Requer Token).
    - `POST /products`: Cria um novo produto (Requer Token).
    - `PUT /products/<id>`: Atualiza um produto (Requer Token).
    - `DELETE /products/<id>`: Remove um produto (Requer Token).

### 3. Importação de Vendas em Lote
Funcionalidade para upload de arquivos CSV contendo registros de vendas.
- **Validação**: Cada linha do CSV é validada individualmente usando Pydantic.
- **Processamento**:
    - Se a linha for válida, é adicionada a uma lista de inserção.
    - Se inválida, o erro é registrado e retornado no relatório final, sem interromper o processo para as linhas válidas.
- **Endpoint**: `POST /sales/upload` (Requer Token).

---

## ⚙️ Como Executar

1.  **Instale as dependências**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Configure o ambiente**:
    Certifique-se de ter um arquivo `.env` na raiz com:
    ```env
    MONGO_URI=sua_string_de_conexao_mongodb
    SECRET_KEY=sua_chave_secreta
    ```

3.  **Inicie o servidor**:
    ```bash
    python run.py
    ```
