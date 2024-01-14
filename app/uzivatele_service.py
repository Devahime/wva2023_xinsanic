from database.database import get_db

class UzivateleService:
    @staticmethod
    def get_all():
        db = get_db()

        sql = "SELECT * FROM uzivatel"
        return db.execute(sql).fetchall()

    @staticmethod
    def get_role_uzivatelu():
        db = get_db()

        sql = "SELECT user_id, jmeno, prijmeni, r.nazev AS nazev_role FROM uzivatel JOIN role_uzivatele ru on uzivatel.user_id = ru.uzivatele_id JOIN role r on ru.role_id = r.role_id"
        return db.execute(sql).fetchall()

