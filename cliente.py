from database import conectar

def criar_cliente(nome, telefone, endereco):
    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(
                "INSERT INTO cliente (nome, telefone, endereco) VALUES (%s, %s, %s) RETURNING id_cliente",
                (nome, telefone, endereco)
            )
            id_cliente = cursor.fetchone()[0]
            return {
                "success":True,
                "data":{
                    "id_cliente":id_cliente
                }
            }
        
def editar_cliente(id_cliente, nome, telefone, endereco):
    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(
                """
                UPDATE cliente
                SET nome = %s, telefone = %s, endereco = %s
                WHERE id_cliente = %s
                """, (nome, telefone, endereco, id_cliente)
            )
            return {
                "success":True,
                "data":{
                    "id_cliente":id_cliente
                }
            }
        
def excluir_cliente(id_cliente):
    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(
                "DELETE FROM cliente WHERE id_cliente = %s", (id_cliente,)
            )
            return {
                "success":True,
                "data":{
                    "id_cliente":id_cliente
                }
            }