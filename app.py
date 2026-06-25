from flask import Flask, request
from cliente import criar_cliente, obter_cliente, listar_clientes, atualizar_cliente, excluir_cliente
from produto import criar_produto, listar_produto, editar_produto, deletar_produto, obter_produto
from pedido import criar_pedido,adicionar_produto_ao_pedido, busca_pedido, remover_produto_do_pedido, editar_quantidade_produto_pedido

#cria aplicação Flask
app = Flask(__name__)

#Ignorar a tabela ASCII e permitir caracteres acentuados.
app.json.ensure_ascii = False

#Rota para a página inicial
@app.route('/')
def home():
    return "API da pizzaria está funcionando!", 200

#rota para listar clientes
@app.route('/clientes')
def listar_clientes_route():
    return listar_clientes(), 200

#rota para obter um cliente por ID
@app.route('/clientes/<int:id_cliente>')
def cliente_por_id_route(id_cliente):

    resultado = obter_cliente(id_cliente)

    if not resultado["success"]:
        return resultado, 404

    return resultado, 200

#rota para criar um cliente
@app.route('/clientes', methods=['POST'])
def cadastrar_cliente():

    dados = request.get_json()

    if not dados:
        return {
            "success": False,
            "message": "JSON inválido ou ausente"
        }, 400

    campos_obrigatorios = [
        "nome",
        "telefone",
        "endereco"
    ]

    for campo in campos_obrigatorios:
        if campo not in dados:
            return {
                "success": False,
                "message": f"Campo obrigatório ausente: {campo}"
            }, 400

    resultado = criar_cliente(
        nome=dados["nome"],
        telefone=dados["telefone"],
        endereco=dados["endereco"]
    )

    return resultado, 201

#Rota para editar cliente
@app.route('/clientes/<int:id_cliente>', methods=['PUT'])
def editar_cliente_route(id_cliente):

    dados = request.get_json()

    if not dados:
        return {
            "success": False,
            "message": "JSON inválido ou ausente"
        }, 400

    campos_obrigatorios = [
        "nome",
        "telefone",
        "endereco"
    ]

    for campo in campos_obrigatorios:
        if campo not in dados:
            return {
                "success": False,
                "message": f"Campo obrigatório ausente: {campo}"
            }, 400

    resultado = atualizar_cliente(
        id_cliente=id_cliente,
        nome=dados["nome"],
        telefone=dados["telefone"],
        endereco=dados["endereco"]
    )

    if not resultado["success"]:
        return resultado, 404

    return resultado, 200

#Rota para excluir cliente
@app.route('/clientes/<int:id_cliente>', methods=['DELETE'])
def excluir_cliente_route(id_cliente):
    resultado = excluir_cliente(id_cliente)

    if not resultado["success"]:
        return resultado, 404
    return resultado, 200

#Rota para criar produto
@app.route('/produtos', methods=['POST'])
def criar_produto_route():

    dados = request.get_json()
    if not dados:
        return {
            "success": False,
            "message": "JSON inválido ou ausente"
        }, 400

    campos_obrigatorios = [
        "nome",
        "preco"
    ]

    for campo in campos_obrigatorios:
        if campo not in dados:
            return {
                "success": False,
                "message": f"Campo obrigatório ausente: {campo}"
            }, 400

    resultado = criar_produto(
        nome=dados["nome"],
        preco=dados["preco"]
    )

    if not resultado["success"]:
        return resultado, 400

    return resultado, 201

#rota para listar produtos
@app.route('/produtos')
def listar_produtos_route():
    return listar_produto(), 200

#rota para obter um produto por ID
@app.route('/produtos/<int:id_produto>', methods=['GET'])
def produto_por_id_route(id_produto):
    resultado = obter_produto(id_produto)

    if not resultado["success"]:
        return resultado, 404
    return resultado, 200

#Rota para editar produto
@app.route('/produtos/<int:id_produto>', methods=['PUT'])
def editar_produto_route(id_produto):
    dados = request.get_json()

    if not dados:
        return {
            "sucess": False,
            "message": "JSON inválido ou ausente"
        }, 400
    
    campos_obrigatorios = [
        "novo_nome",
        "novo_preco"
    ]
    for campo in campos_obrigatorios:
        if campo not in dados:
            return {
                "success": False,
                "message": f"Campo obrigatório ausente: {campo}"
            }, 400
        
    resultado = editar_produto(
        id_produto=id_produto,
        novo_nome=dados["novo_nome"],
        novo_preco=dados["novo_preco"]
    )
    if not resultado["success"]:
        return resultado, 404
    return resultado, 200

#Rota para deletar produto
@app.route('/produtos/<int:id_produto>', methods=['DELETE'])
def deletar_produto_route(id_produto):
    resultado = deletar_produto(id_produto)

    if not resultado["success"]:
        return resultado, 404
    return resultado, 200

#Rota para criar pedido
@app.route('/pedidos', methods=['POST'])
def criar_pedido_route():
    dados = request.get_json()

    if not dados:
        return {
            "success": False,
            "message": "JSON inválido ou ausente"
        }, 400

    if "id_cliente" not in dados:
        return {
            "success": False,
            "message": "Campo obrigatório ausente: id_cliente"
        }, 400
    
    resultado = criar_pedido(id_cliente=dados["id_cliente"])
    
    if not resultado["success"]:
        return resultado, 404
    
    return resultado, 201


#rota para adicionar produto ao pedido
@app.route('/pedidos/<int:id_pedido>/produtos/<int:id_produto>', methods=['POST'])
def adicionar_produto_ao_pedido_route(id_pedido, id_produto):
    dados = request.get_json()

    if not dados:
        return {
            "success": False,
            "message": "JSON inválido ou ausente"
        }, 400

    if "quantidade" not in dados:
        return {
            "success": False,
            "message": "Campo obrigatório ausente: quantidade"
        }, 400
    
    if dados["quantidade"]<= 0:
        return {
            "success": False,
            "message": "A quantidade deve ser maior que zero"
        }, 400
    
    resultado = adicionar_produto_ao_pedido(
        id_pedido=id_pedido, 
        id_produto=id_produto, 
        quantidade=dados["quantidade"])
    
    if not resultado["success"]:
        return resultado, 404
    return resultado, 201

#rota para buscar pedido por id do pedido
@app.route('/pedidos/<int:id_pedido>', methods=['GET'])
def busca_pedidos_route(id_pedido):   

    resultado = busca_pedido(id_pedido)
    if not resultado["success"]:
        return resultado, 404
    return resultado, 200

#Editar quantidade de produto no pedido
@app.route('/pedidos/<int:id_pedido>/produtos/<int:id_produto>', methods=['PUT'])
def editar_quantidade_produto_route(id_pedido, id_produto):
    dados = request.get_json()

    if not dados:
        return {
            "success": False,
            "message": "JSON inválido ou ausente"
        }, 400
    
    if "nova_quantidade" not in dados:
        return {
            "success": False,
            "message": "Campo obrigatório ausente: nova_quantidade"
        }, 400

    if dados["nova_quantidade"] <= 0:
        return {
            "success": False,
            "message": "A quantidade deve ser maior que zero"
        }, 400
    
    resultado = editar_quantidade_produto_pedido(
        id_pedido=id_pedido,
        id_produto=id_produto,
        nova_quantidade=dados["nova_quantidade"]
    )
    if not resultado["success"]:
        return resultado, 400
    return resultado, 200

#rota para remover produto do pedido
@app.route('/pedidos/<int:id_pedido>/produtos/<int:id_produto>', methods=['DELETE'])
def remover_produto_do_pedido_route(id_pedido, id_produto):
    resultado = remover_produto_do_pedido(id_pedido, id_produto)
    if not resultado["success"]:
        return resultado, 404
    return resultado, 200

#verifica se o script está sendo executado diretamente
if __name__ == '__main__':
    app.run(debug=True)
#"Sobre o app.run" Inicia o servidor Flask em modo de depuração, permitindo que o aplicativo seja
#acessado localmente e fornecendo mensagens de erro detalhadas durante o desenvolvimento.