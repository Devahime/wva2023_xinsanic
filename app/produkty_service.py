import datetime

from database.database import get_db

class ProduktyService:
    @staticmethod
    def get_prudukty_restaurace(restaurace_id=0):
        db = get_db()

        sql = "SELECT * FROM produkt JOIN restaurace USING(restaurace_id) WHERE 1=1"
        arguments = []
        if restaurace_id is not None:
            sql += " AND restaurace_id = ?"
            arguments.append(restaurace_id)
        return db.execute(sql, arguments).fetchall()

    @staticmethod
    def get_nedostupne_produkty(restaurace_id=None):
        db = get_db()
        sql = "SELECT * FROM produkt WHERE 1=1"
        arguments = []

        if restaurace_id is not None:
            sql += " AND datetime('now', 'localtime') < datetime(dostupny_od) AND restaurace_id = ?"
            arguments.append(restaurace_id)

        return db.execute(sql, arguments).fetchall()

    @staticmethod
    def get_nadchazejici_produkty(restaurace_id=None):
        db = get_db()
        sql = "SELECT * FROM produkt WHERE 1=1"
        arguments = []

        if restaurace_id is not None:
            sql += " AND datetime('now', 'localtime') > datetime(dostupne_do) AND restaurace_id = ?"
            arguments.append(restaurace_id)

        return db.execute(sql, arguments).fetchall()

    @staticmethod
    def get_limitovane_dostupne(restaurace_id=None):
        db = get_db()
        sql = "SELECT * FROM produkt WHERE 1=1"
        arguments = []

        if restaurace_id is not None:
            sql += " AND datetime('now', 'localtime') BETWEEN datetime(dostupny_od) AND datetime(dostupne_do) AND restaurace_id = ?"
            arguments.append(restaurace_id)

        return db.execute(sql, arguments).fetchall()

    @staticmethod
    def get_zobrazit_dostupne(restaurace_id=None):
        db = get_db()
        sql = "SELECT * FROM produkt WHERE 1=1"
        arguments = []

        if restaurace_id is not None:
            sql += " AND ((datetime('now', 'localtime') BETWEEN datetime(dostupny_od) AND datetime(dostupne_do) AND restaurace_id = ?) OR (dostupny_od IS NULL AND dostupne_do IS NULL AND restaurace_id = ?))"
            arguments.extend([restaurace_id, restaurace_id])

        return db.execute(sql, arguments).fetchall()

    @staticmethod
    def funkce_na_soucet():
        db = get_db()
        sql = "SELECT produkt_id, cena FROM produkt"
        return db.execute(sql).fetchall()

    @staticmethod
    def vlozit_do_databaze(user_id, stav, product_quantities, total_cost):
        db = get_db()
        current_date = datetime.datetime.now().strftime('%Y-%m-%d')
        db.execute(
            "INSERT INTO objednavka (cena, stav_objednavky, uzivatel_id, vytvoreni) VALUES (?, ?, ?, current_date)",
            (total_cost, stav, user_id)
        )
        db.commit()

        order_id = db.execute("SELECT last_insert_rowid()").fetchone()[0]

        for product_id, quantity in product_quantities.items():
            db.execute(
                "INSERT INTO objednavka_produkt (mnozstvi, objednavka_id, produkt_id) VALUES (?, ?, ?)",
                (quantity, order_id, product_id)
            )
            db.commit()
