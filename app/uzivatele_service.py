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

        sql = "SELECT user_id, jmeno, prijmeni, r.nazev AS nazev_role FROM uzivatel LEFT JOIN role_uzivatele ru ON uzivatel.user_id = ru.uzivatele_id LEFT JOIN role r ON ru.role_id = r.role_id"
        return db.execute(sql).fetchall()

    @staticmethod
    def get_role():
        db = get_db()
        sql = "SELECT * FROM role"
        return db.execute(sql).fetchall()

    @staticmethod
    def update_role_uzivatele(user_id: int, new_role_id: int):
        db = get_db()
        sql = "UPDATE role_uzivatele SET role_id = ? WHERE uzivatele_id = ? "
        db.execute(sql, (new_role_id, user_id))
        db.commit()
        return True

    @staticmethod
    def get_uzivatel_by_id(user_id: str):
        db = get_db()

        cur = db.cursor()
        user = cur.execute('SELECT uzivatel.user_id, jmeno, prijmeni, heslo.heslo FROM uzivatel LEFT JOIN heslo on heslo.user_id = uzivatel.user_id WHERE uzivatel.user_id = ?', [user_id]).fetchone()

        return None if user == None else { 'user_id': user[0], 'name': user[1], 'surname': user[2], 'heslo': user[3] }

    @staticmethod
    def get_uzivatel_by_phone(phone: str):
        db = get_db()

        cur = db.cursor()
        user = cur.execute('SELECT uzivatel.user_id, jmeno, prijmeni, heslo.heslo FROM uzivatel LEFT JOIN heslo on heslo.user_id = uzivatel.user_id WHERE uzivatel.telefon = ?', [phone]).fetchone()

        return None if user == None else { 'user_id': user[0], 'name': user[1], 'surname': user[2], 'heslo': user[3] }
    
    @staticmethod
    def create_uzivatel(data):
        db = get_db()

        cur = db.cursor()

        count = cur.execute('SELECT COUNT(*) FROM uzivatel').fetchone()[0] +1

        cur.execute('INSERT INTO uzivatel (user_id, jmeno, prijmeni, telefon) VALUES (?, ?, ?, ?)', [count, data['name'], data['surname'], data['telefon']])
        
        # TODO: Nastavit heslo_id
        cur.execute('INSERT INTO heslo (user_id, heslo) VALUES (?, ?)', [count, data['heslo']])

        user = cur.execute(f'SELECT user_id, jmeno, prijmeni FROM uzivatel WHERE user_id = ?', [count]).fetchone()
        db.commit()
        return { 'user_id': user[0], 'name': user[1], 'surname': user[2] }

