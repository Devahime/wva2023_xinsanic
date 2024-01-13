from database.database import get_db

class ObjednavkaService:
    @staticmethod
    def get_all():
        db = get_db()

        sql = "SELECT * FROM objednavka"
        return db.execute(sql).fetchall()

    @staticmethod
    def get_pocet():
        db = get_db()
        result = db.execute(
            "SELECT COUNT(*) FROM objednavka"
        ).fetchone()
        return result[0] if result else 0

    @staticmethod
    def get_mnozstevni_slevu():
        db = get_db()
        total_orders = db.execute("SELECT COUNT(*) FROM objednavka").fetchone()[0]
        discount = min((total_orders // 10) * 5, 30)

        return discount