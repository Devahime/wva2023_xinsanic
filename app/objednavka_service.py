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

    @staticmethod
    def get_nevyrizene():
        db = get_db()
        nevyrizeno = db.execute("SELECT DISTINCT objednavka.objednavka_id, restaurace.nazev, objednavka.uzivatel_id, stav_objednavky FROM objednavka JOIN objednavka_produkt USING(objednavka_id) JOIN produkt USING(produkt_id) JOIN restaurace USING (restaurace_id) WHERE stav_objednavky = 'nedoruceno'").fetchall()
        return nevyrizeno

    @staticmethod
    def get_volne_objednavky():
        db = get_db()
        volne = db.execute(
            "SELECT DISTINCT objednavka.objednavka_id, restaurace.nazev, objednavka.uzivatel_id, stav_objednavky FROM objednavka JOIN objednavka_produkt USING(objednavka_id) JOIN produkt USING(produkt_id) JOIN restaurace USING (restaurace_id) WHERE stav_objednavky = 'volna'").fetchall()
        return volne

    @staticmethod
    def get_vyrizene():
        db = get_db()
        vyrizene = db.execute(
            "SELECT DISTINCT objednavka.objednavka_id, restaurace.nazev, objednavka.uzivatel_id, stav_objednavky FROM objednavka JOIN objednavka_produkt USING(objednavka_id) JOIN produkt USING(produkt_id) JOIN restaurace USING (restaurace_id) WHERE stav_objednavky = 'doruceno'").fetchall()
        return vyrizene

    @staticmethod
    def get_statistika():
        db = get_db()
        statistika = db.execute("SELECT  DISTINCT objednavka.objednavka_id, restaurace.nazev, u.user_id AS uzivatel, k.user_id AS kuryr, objednavka.stav_objednavky, cesta.cena, objednavka.cena * 0.15 AS provize FROM objednavka LEFT JOIN uzivatel u ON objednavka.uzivatel_id=u.user_id LEFT JOIN cesta ON objednavka.objednavka_id = cesta.objednavka_id LEFT JOIN uzivatel k ON cesta.user_id = k.user_id LEFT JOIN uzivatel JOIN objednavka_produkt USING(objednavka_id)LEFT JOIN produkt USING(produkt_id)LEFT JOIN restaurace USING(restaurace_id)").fetchall()
        return statistika

    @staticmethod
    def update_stav(objednavka_id: int, novy_stav: str):
        db = get_db()
        sql = "UPDATE objednavka SET stav_objednavky = ? WHERE objednavka_id = ?"
        db.execute(sql, (novy_stav, objednavka_id))
        db.commit()
        return True

    @staticmethod
    def get_moje_objednavky(user_id):
        db = get_db()
        sql = "SELECT * FROM objednavka WHERE uzivatel_id = ?"
        return db.execute(sql, (user_id,)).fetchall()

    @staticmethod
    def get_moje_objednavky_pocet(user_id):
        db = get_db()
        sql = "SELECT COUNT(*) FROM objednavka WHERE uzivatel_id = ?"
        result = db.execute(sql, (user_id,)).fetchone()
        return result[0] if result else 0

    @staticmethod
    def get_moje_mnozstevni_slevu(user_id):
        db = get_db()
        sql = "SELECT COUNT(*) FROM objednavka WHERE uzivatel_id = ?"
        result = db.execute(sql, (user_id,)).fetchone()
        discount = min((result[0] // 10) * 5, 30)

        return discount

    @staticmethod
    def get_moje_vyrizene(user_id):
        db = get_db()
        sql ="SELECT DISTINCT objednavka.objednavka_id, restaurace.nazev, objednavka.uzivatel_id, stav_objednavky FROM objednavka JOIN objednavka_produkt USING(objednavka_id) JOIN produkt USING(produkt_id) JOIN restaurace USING (restaurace_id) JOIN cesta c on objednavka.objednavka_id = c.objednavka_id WHERE stav_objednavky = 'doruceno' AND c.user_id = ?"
        return db.execute(sql, (user_id,)).fetchall()

    @staticmethod
    def get_moje_nevyrizene(user_id):
        db = get_db()
        sql = "SELECT DISTINCT objednavka.objednavka_id, restaurace.nazev, objednavka.uzivatel_id, stav_objednavky FROM objednavka JOIN objednavka_produkt USING(objednavka_id) JOIN produkt USING(produkt_id) JOIN restaurace USING (restaurace_id) JOIN cesta c on objednavka.objednavka_id = c.objednavka_id WHERE stav_objednavky = 'nedoruceno' AND c.user_id = ?"
        return db.execute(sql, (user_id,)).fetchall()

    def create_or_update_cesta(objednavka_id, user_id):
        db = get_db()

        existing_cesta = db.execute("SELECT cesta_id FROM cesta WHERE objednavka_id = ?", (objednavka_id,)).fetchone()

        if existing_cesta:
            cesta_id = existing_cesta['cesta_id']
        else:
            cesta_id = db.execute("INSERT INTO cesta (user_id, cena, objednavka_id) VALUES (?, 0, ?)",
                                  (user_id, objednavka_id)).lastrowid
            db.commit()

        total_cost = db.execute("SELECT cena FROM objednavka WHERE objednavka_id = ?", (objednavka_id,)).fetchone()[
            'cena']

        cesta_cost = 0.1 * total_cost

        db.execute("UPDATE cesta SET cena = ? WHERE cesta_id = ?", (cesta_cost, cesta_id))
        db.commit()

    @staticmethod
    def get_castky():
        db = get_db()
        statistika_query = """
            SELECT
                SUM(cesta.cena) AS celkova_cena_cesty,
                SUM(objednavka.cena * 0.15) AS celkova_cena_proviz,
                SUM(cesta.cena + objednavka.cena * 0.15) AS celkovy_zisk
            FROM
                objednavka
                LEFT JOIN uzivatel u ON objednavka.uzivatel_id = u.user_id
                LEFT JOIN cesta ON objednavka.objednavka_id = cesta.objednavka_id
                LEFT JOIN uzivatel k ON cesta.user_id = k.user_id
                LEFT JOIN uzivatel
                LEFT JOIN objednavka_produkt USING (objednavka_id)
                LEFT JOIN produkt USING (produkt_id)
                LEFT JOIN restaurace USING (restaurace_id)
        """
        return db.execute(statistika_query).fetchone()
