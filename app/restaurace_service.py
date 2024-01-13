from database.database import get_db

class RestauraceService:
    @staticmethod
    def get_all():
        db = get_db()

        sql = "SELECT * FROM restaurace"
        return db.execute(sql).fetchall()