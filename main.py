"""
===================================================
IMPORT DAS FUNÇÕES
===================================================
"""

from cliente import criar_cliente
from pedido import criar_pedido
from pedido import adicionar_produto_ao_pedido
from produto import criar_produto

"""
===================================================
NOVO CLIENTE
===================================================
"""
novo_cliente = criar_cliente(
    nome="Tainá Novais",
    telefone="13 99799-1548",
    endereco="Rua joão marqui, 65, Indaiatuba - SP")

print(novo_cliente)

"""
===================================================
NOVO PRODUTO
===================================================
"""

novo_produto = criar_produto(
    nome="Pizza de Calabresa",
    preco=35.00)

print(novo_produto)

"""
===================================================
NOVO PEDIDO
===================================================
"""

novo_pedido = criar_pedido(
    novo_cliente['data']['id_cliente']
)

print(novo_pedido)


id_pedido = novo_pedido["data"]["id_pedido"]
id_produto = novo_produto["data"]["id_produto"]


adicionar_produto_ao_pedido(
    id_pedido=id_pedido,
    id_produto=id_produto,
    quantidade=2
)