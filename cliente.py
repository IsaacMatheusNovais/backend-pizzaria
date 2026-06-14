from database import conectar

#criar cliente------------------------------------------------------------------------
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

#obter cliente por id-----------------------------------------------------------------
def obter_cliente(id_cliente):
    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(
                "SELECT id_cliente, nome, telefone, endereco FROM cliente WHERE id_cliente = %s",
                (id_cliente,)
            )
            cliente = cursor.fetchone()
            if cliente:
                return {
                    "success":True,
                    "data":{
                        "id_cliente":cliente[0],
                        "nome":cliente[1],
                        "telefone":cliente[2],
                        "endereco":cliente[3]
                    }
                }
            return {
                "success":False,
                "message":"Cliente não encontrado"}

#listar clientes----------------------------------------------------------------------
def listar_clientes():
    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute("""
            SELECT id_cliente, nome, telefone, endereco
            FROM cliente
            ORDER BY id_cliente""")

            clientes = cursor.fetchall()

            resultado = []

            for cliente in clientes:
                resultado.append({
                    "id_cliente": cliente[0],
                    "nome": cliente[1],
                    "telefone": cliente[2],
                    "endereco": cliente[3]
                })

            return resultado

#atualizar cliente--------------------------------------------------------------------
def atualizar_cliente(id_cliente, nome, telefone, endereco):

    with conectar() as conexao:
        with conexao.cursor() as cursor:

            cursor.execute(
                """
                UPDATE cliente
                SET
                    nome = %s,
                    telefone = %s,
                    endereco = %s
                WHERE id_cliente = %s
                """,
                (nome, telefone, endereco, id_cliente)
            )
            if cursor.rowcount == 0:
                return {
                    "success": False,
                    "message": "Cliente não encontrado"
                }
        return {
            "success": True,
            "data": {
                "id_cliente": id_cliente,
                "nome": nome,
                "telefone": telefone,
                "endereco": endereco
            }
        }
    
#excluir cliente----------------------------------------------------------------------
def excluir_cliente(id_cliente):
    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(
                "DELETE FROM cliente WHERE id_cliente = %s", (id_cliente,)
            )
            if cursor.rowcount == 0:
                return {
                    "success": False,
                    "message": "Cliente não encontrado"
                }
            return {
                "success":True,
                "data":{
                    "id_cliente":id_cliente,
                    "message":"Cliente excluído com sucesso"
                }
            }