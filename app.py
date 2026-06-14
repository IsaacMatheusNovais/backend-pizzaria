from flask import Flask, request
from cliente import criar_cliente, obter_cliente, listar_clientes, atualizar_cliente, excluir_cliente

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


#verifica se o script está sendo executado diretamente
if __name__ == '__main__':
    app.run(debug=True)
#"Sobre o app.run" Inicia o servidor Flask em modo de depuração, permitindo que o aplicativo seja
#acessado localmente e fornecendo mensagens de erro detalhadas durante o desenvolvimento.