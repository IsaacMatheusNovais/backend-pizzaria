from database import conectar


def criar_produto(nome, preco):
    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(
                "INSERT INTO produto (nome, preco) VALUES (%s, %s) RETURNING id_produto",
                (nome, preco)
            )
            id_produto = cursor.fetchone()[0]
            return {
                "success":True,
                "data":{
                    "id_produto":id_produto
                }
            }


def editar_preco_produto(id_produto, novo_preco):
    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute("""
                UPDATE produto
                SET preco = %s
                WHERE produto.id_produto = %s
            """, (novo_preco, id_produto))

            return {
                "success": True,
                "data": {
                    "id_produto": id_produto,
                    "novo_preco": novo_preco
                }
            }

def deletar_produto(id_produto):
    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute("""
                DELETE FROM produto
                WHERE id_produto = %s
            """, (id_produto,))

            return {
                "success": True,
                "data": {
                    "id_produto": id_produto
                }
            }