from models.database import get_db


class PedidoModel:
    def create(self, usuario_id, itens):
        db = get_db()
        cursor = db.cursor()

        total = 0
        for item in itens:
            cursor.execute(
                "SELECT * FROM produtos WHERE id = ?", (item["produto_id"],)
            )
            produto = cursor.fetchone()
            if produto is None:
                return {"erro": f"Produto {item['produto_id']} nao encontrado"}
            if produto["estoque"] < item["quantidade"]:
                return {"erro": f"Estoque insuficiente para {produto['nome']}"}
            total += produto["preco"] * item["quantidade"]

        cursor.execute(
            "INSERT INTO pedidos (usuario_id, status, total) VALUES (?, 'pendente', ?)",
            (usuario_id, total),
        )
        pedido_id = cursor.lastrowid

        for item in itens:
            cursor.execute(
                "SELECT preco FROM produtos WHERE id = ?", (item["produto_id"],)
            )
            produto = cursor.fetchone()
            cursor.execute(
                "INSERT INTO itens_pedido (pedido_id, produto_id, quantidade, preco_unitario) VALUES (?, ?, ?, ?)",
                (pedido_id, item["produto_id"], item["quantidade"], produto["preco"]),
            )
            cursor.execute(
                "UPDATE produtos SET estoque = estoque - ? WHERE id = ?",
                (item["quantidade"], item["produto_id"]),
            )

        db.commit()
        return {"pedido_id": pedido_id, "total": total}

    def get_by_user(self, usuario_id):
        return self._get_pedidos_with_itens(
            "WHERE p.usuario_id = ?", (usuario_id,)
        )

    def get_all(self):
        return self._get_pedidos_with_itens()

    def update_status(self, pedido_id, novo_status):
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "UPDATE pedidos SET status = ? WHERE id = ?",
            (novo_status, pedido_id),
        )
        db.commit()

    def get_sales_report(self):
        db = get_db()
        cursor = db.cursor()

        cursor.execute(
            "SELECT COUNT(*) as total, COALESCE(SUM(total), 0) as faturamento FROM pedidos"
        )
        row = cursor.fetchone()
        total_pedidos = row["total"]
        faturamento = row["faturamento"]

        cursor.execute("""
            SELECT
                COALESCE(SUM(CASE WHEN status = 'pendente' THEN 1 ELSE 0 END), 0) as pendentes,
                COALESCE(SUM(CASE WHEN status = 'aprovado' THEN 1 ELSE 0 END), 0) as aprovados,
                COALESCE(SUM(CASE WHEN status = 'cancelado' THEN 1 ELSE 0 END), 0) as cancelados
            FROM pedidos
        """)
        status_row = cursor.fetchone()

        return {
            "total_pedidos": total_pedidos,
            "faturamento_bruto": faturamento,
            "pedidos_pendentes": status_row["pendentes"],
            "pedidos_aprovados": status_row["aprovados"],
            "pedidos_cancelados": status_row["cancelados"],
        }

    def _get_pedidos_with_itens(self, where_clause="", params=()):
        db = get_db()
        cursor = db.cursor()

        query = f"""
            SELECT p.id, p.usuario_id, p.status, p.total, p.criado_em,
                   i.produto_id, i.quantidade, i.preco_unitario,
                   pr.nome as produto_nome
            FROM pedidos p
            LEFT JOIN itens_pedido i ON p.id = i.pedido_id
            LEFT JOIN produtos pr ON i.produto_id = pr.id
            {where_clause}
            ORDER BY p.id
        """
        cursor.execute(query, params)
        rows = cursor.fetchall()

        pedidos = {}
        for row in rows:
            pid = row["id"]
            if pid not in pedidos:
                pedidos[pid] = {
                    "id": pid,
                    "usuario_id": row["usuario_id"],
                    "status": row["status"],
                    "total": row["total"],
                    "criado_em": row["criado_em"],
                    "itens": [],
                }
            if row["produto_id"] is not None:
                pedidos[pid]["itens"].append({
                    "produto_id": row["produto_id"],
                    "produto_nome": row["produto_nome"] or "Desconhecido",
                    "quantidade": row["quantidade"],
                    "preco_unitario": row["preco_unitario"],
                })

        return list(pedidos.values())
