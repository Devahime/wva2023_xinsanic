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
    
    @staticmethod
    def get_uzivatel_by_phone(phone: str):
        db = get_db()

        cur = db.cursor()
        user = cur.execute('SELECT user_id, jmeno, prijmeni, heslo.heslo FROM uzivatel WHERE uzivatel.telefon = ? LEFT JOIN heslo on heslo.user_id = uzivatel.user_id', [phone]).fetchone()

        return None if user == None else { 'user_id': user[0], 'name': user[1], 'surname': user[2], 'heslo': user[3] }
    
    @staticmethod
    def create_uzivatel(data):
        db = get_db()

        cur = db.cursor()

        count = cur.execute('SELECT COUNT(*) FROM uzivatel').fetchone()[0]

        cur.execute('INSERT INTO uzivatel (user_id, jmeno, prijmeni, telefon) VALUES (?, ?, ?, ?)', [count, data['name'], data['surname'], data['telefon']])
        
        # TODO: Nastavit heslo_id
        cur.execute('INSERT INTO heslo (user_id, heslo) VALUES (?, ?)', [count, data['heslo']])

        user = cur.execute(f'SELECT user_id, jmeno, prijmeni FROM uzivatel WHERE user_id = ?', count).fetchone()
        db.commit()
        return { 'user_id': user[0], 'name': user[1], 'surname': user[2] }

