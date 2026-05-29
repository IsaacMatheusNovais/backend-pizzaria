# Sistema de Pedidos de Pizzaria

Este projeto é um backend desenvolvido em Python para gerenciar pedidos de uma pizzaria, com PostgreSQL como banco de dados.

## Tecnologias Utilizadas
- Python 3.x
- psycopg2 (para conexão com PostgreSQL)
- PostgreSQL (banco de dados relacional)

## Funcionalidades
- Cadastro de clientes
- Cadastro de produtos
- Criação de pedidos
- Associação de produtos a pedidos
- Consulta detalhada de pedidos

## Estrutura do Projeto
- `database.py`: Função de conexão com o banco de dados.
- `cliente.py`: Funções para criar, editar e deletar clientes.
- `produto.py`: Funções para gerenciar produtos.
- `pedido.py`: Funções para criar pedidos e associar produtos.
- `main.py`: Integração e execução das operações.

## Como Executar
1. Crie um ambiente virtual (opcional, mas recomendado): python -m venv venv

2. Ative o ambiente virtual:
- No Windows: `venv\Scripts\activate`
- No macOS/Linux: `source venv/bin/activate`

3. Instale as dependências: pip install -r requirements.txt

4. Configure o banco de dados no PostgreSQL (crie o banco e as tabelas se ainda não estiverem criadas).

5. Execute o script principal: python main.py

## Notas
- Certifique-se de que o PostgreSQL está rodando localmente na porta padrão (5432) ou ajuste a configuração no arquivo `database.py`.
- Caso precise de mais funcionalidades, basta adicionar novas funções e integrá-las no `main.py`.
