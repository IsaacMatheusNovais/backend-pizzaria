from database import conectar
import psycopg2.extras
from psycopg2.errors import ForeignKeyViolation

#criar pedido com tratamento de excessão para cliente inexistente
def criar_pedido(id_cliente):
    try: #tratamento de excessão
        with conectar() as conexao:
            with conexao.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO pedido (id_cliente) VALUES (%s) RETURNING id_pedido",(id_cliente,)
                )
                id_pedido = cursor.fetchone()[0]

                return {
                    "success": True,
                    "data":{
                        "id_pedido":id_pedido,
                        "id_cliente": id_cliente
                    }
                }
    except ForeignKeyViolation: #Tratamento de excessão daqui em diante
        return {
            "success": False,
            "message": "cliente não encontrado"
        }

#adicionar produto ao pedido
def adicionar_produto_ao_pedido(id_pedido, id_produto, quantidade):
    try:
        with conectar() as conexao:
            with conexao.cursor() as cursor:
                
                #busca e armazena nome do produto
                cursor.execute("""
                               SELECT nome FROM produto
                               WHERE id_produto = %s""", (id_produto,))
                
                produto = cursor.fetchone()

                # Verifica se o produto já existe no pedido
                cursor.execute(
                    """
                    SELECT quantidade
                    FROM pedido_produto
                    WHERE id_pedido = %s
                    AND id_produto = %s
                    """,
                    (id_pedido, id_produto)
                )

                registro = cursor.fetchone()

                # Se já existe, soma a quantidade
                if registro:

                    cursor.execute(
                        """
                        UPDATE pedido_produto
                        SET quantidade = quantidade + %s
                        WHERE id_pedido = %s
                        AND id_produto = %s
                        RETURNING quantidade
                        """,
                        (quantidade, id_pedido, id_produto)
                    )

                    quantidade_total = cursor.fetchone()[0]

                    return {
                        "success": True,
                        "message": "Quantidade atualizada com sucesso",
                        "data": {
                            "id_pedido": id_pedido,
                            "produto": produto[0],
                            "quantidade_total": quantidade_total
                        }
                    }

                # Se não existe, cria o registro
                else:

                    cursor.execute(
                        """
                        INSERT INTO pedido_produto
                        (
                            id_pedido,
                            id_produto,
                            quantidade
                        )
                        VALUES
                        (
                            %s,
                            %s,
                            %s
                        )
                        """,
                        (id_pedido, id_produto, quantidade)
                    )

                    return {
                        "success": True,
                        "message": "Produto adicionado ao pedido",
                        "data": {
                            "id_pedido": id_pedido,
                            "produto": produto[0],
                            "quantidade": quantidade
                        }
                    }

    except ForeignKeyViolation:

        return {
            "success": False,
            "message": "Pedido ou produto não encontrado"
        }
    

#buscar pedido por id do pedido, retornando o nome do cliente, 
#nome do produto, preço unitário e quantidade de cada produto no pedido. 
#Além disso, deve retornar o total do pedido.
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
                    LEFT JOIN pedido_produto ON pedido.id_pedido = pedido_produto.id_pedido
                    LEFT JOIN produto ON produto.id_produto = pedido_produto.id_produto
                    WHERE pedido.id_pedido = %s
                """, (id_pedido,))

                resultados = cursor.fetchall()

                if not resultados:

                    return {"success": False,
                        "message": "Pedido não encontrado"
                        } 
                
                if resultados[0]["produto"] is None:
                    return {
                    "success": True,
                    "data": {
                        "id_pedido": id_pedido,
                        "itens": [],
                        "total": 0
                        }   
                    }
                
                total = total_pedido(id_pedido)['data']['total']

                return {
                    "success": True,
                    "data" : {
                        "id_pedido": id_pedido,
                        "itens" : resultados,
                        "total": total
                    }
                }
# LEFT JOIN é utilizado para permitir que pedidos sem produtos
# ainda sejam retornados pela consulta. Nesses casos os campos
# de produto virão como None.

# Função para calcular o total do pedido usada na função busca_pedido
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

#Função para editar a quantidade de um produto em um pedido
def editar_quantidade_produto_pedido(id_pedido, id_produto, nova_quantidade):
    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute("""
                           UPDATE pedido_produto
                           SET quantidade = %s
                           WHERE id_pedido = %s AND id_produto = %s
                           """, (nova_quantidade, id_pedido, id_produto))
            if nova_quantidade <= 0:
                return {
                    "success": False,
                    "message": "A quantidade deve ser maior que zero"
            }
    
            if cursor.rowcount == 0:
                return {
                    "success": False,
                    "message": "Produto não encontrado no pedido"
                }
            
            cursor.execute("""
                           SELECT nome FROM produto
                           WHERE id_produto = %s
                           """, (id_produto,))
            
            nome_produto = cursor.fetchone()

            return {
                "success": True,
                "message": "Quantidade atualizada com sucesso",
                "data": {
                    "id_pedido": id_pedido,
                    "nome_produto": nome_produto[0],
                    "nova_quantidade": nova_quantidade
                }
            }

# Função para remover produto do pedido
def remover_produto_do_pedido(id_pedido, id_produto):
    with conectar() as conexao:
        with conexao.cursor() as cursor:

            cursor.execute("""
                SELECT nome
                FROM produto
                WHERE id_produto = %s
            """, (id_produto,))#SELECT para pegar o nome do produto antes de deletar.

            produto = cursor.fetchone()#Armazena o nome.

            cursor.execute("""
                           DELETE FROM pedido_produto
                           WHERE id_pedido = %s AND id_produto = %s
                           """, (id_pedido, id_produto))
            linhas_afetadas = cursor.rowcount
            if linhas_afetadas == 0:
                return {
                    "success": False,
                    "message": "Produto não encontrado no pedido"
                }
            return {
                "success": True,
                "message": "Produto removido do pedido",
                "data": {
                    "id_pedido": id_pedido,
                    "nome_produto": produto[0]
                }
            }