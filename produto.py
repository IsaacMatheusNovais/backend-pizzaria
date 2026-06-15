from database import conectar

#criar produto------------------------------------------------------------------------
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
        
#listar produtos----------------------------------------------------------------------
def listar_produto():
    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute("""
                           SELECT id_produto, nome, preco
                           FROM produto
                           ORDER BY id_produto""")
            produtos = cursor.fetchall()
            resultado = []
            for produto in produtos:
                resultado.append({
                    "id_produto": produto[0],
                    "nome": produto[1],
                    "preco": produto[2]
                })
            return resultado

#obter produto----------------------------------------------------------------------
def obter_produto(id_produto):
    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute("""
                           SELECT id_produto, nome, preco
                           FROM produto
                           WHERE id_produto = %s""", (id_produto,))
            produto = cursor.fetchone()
            if produto:
                return {
                    "success": True,
                    "data":{
                        "id_produto": produto[0],
                        "nome": produto[1],
                        "preco": produto[2]
                    }
                }
            return {
                "success": False,
                "message": "Produto não encontrado"}

#editar produto----------------------------------------------------------------------
def editar_produto(id_produto, novo_nome, novo_preco):
    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute("""
                UPDATE produto
                SET nome = %s, preco = %s
                WHERE produto.id_produto = %s
            """, (novo_nome, novo_preco, id_produto))
            
            if cursor.rowcount == 0:
                return {
                    "success": False,
                    "message": "Produto não encontrado"
                }
            return {
                "success": True,
                "data": {
                    "id_produto": id_produto,
                    "novo_nome": novo_nome,
                    "novo_preco": novo_preco
                }
            }

#deletar produto----------------------------------------------------------------------
def deletar_produto(id_produto):
    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute("""
                DELETE FROM produto
                WHERE id_produto = %s
            """, (id_produto,))
        rowcount = cursor.rowcount
        if rowcount == 0:
            return {
                "success": False,
                "message": "Produto não encontrado"
            }
        return {
            "success": True,
            "data": {
                "id_produto": id_produto
            }
        }