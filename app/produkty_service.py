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

