from database import conectar
import psycopg2.extras

def criar_pedido(id_cliente):
    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(
                "INSERT INTO pedido (id_cliente) VALUES (%s) RETURNING id_pedido",(id_cliente,)
            )
            id_pedido = cursor.fetchone()[0]
            return {
                "success": True,
                "data":{
                    "id_pedido":id_pedido
                }
            }
        
def adicionar_produto_ao_pedido(id_pedido, id_produto, quantidade):
    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(
                "INSERT INTO pedido_produto (id_pedido, id_produto, quantidade) VALUES (%s, %s, %s)", 
                (id_pedido, id_produto, quantidade)
            )
            return {
                "success": True,
                "data": {
                    "id_pedido": id_pedido,
                    "id_produto": id_produto,
                    "quantidade":quantidade
                }
            }
        
def busca_pedido(id_pedido):
    with conectar() as conexao:
        with conexao.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            cursor.execute("""
                SELECT
                    cliente.nome AS cliente,
                    produto.nome AS produto,
                    produto.preco AS preco_unitario,
                    pedido_produto.quantidade

                FROM pedido
                JOIN cliente ON pedido.id_cliente = cliente.id_cliente
                JOIN pedido_produto ON pedido.id_pedido = pedido_produto.id_pedido
                JOIN produto ON produto.id_produto = pedido_produto.id_produto
                WHERE pedido.id_pedido = %s
            """, (id_pedido,))

            resultados = cursor.fetchall()

    total = total_pedido(id_pedido)['data']['total']
    return {
            "success": True,
            "data" : {
                "itens" : resultados,
                "total": total
            }
        }

def total_pedido(id_pedido):
    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute("""
                SELECT
                    SUM(produto.preco * pedido_produto.quantidade) AS total
                           FROM pedido
                           JOIN pedido_produto ON pedido.id_pedido = pedido_produto.id_pedido
                           JOIN produto ON produto.id_produto = pedido_produto.id_produto
                           WHERE pedido.id_pedido = %s
                           """, (id_pedido,))
            total = cursor.fetchone()[0]
            return {
                "success":True,
                "data":{    
                    "id_pedido": id_pedido,
                    "total": total
                }
            }