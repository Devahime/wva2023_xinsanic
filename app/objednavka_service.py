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
        statistika = db.execute("SELECT  DISTINCT objednavka.objednavka_id, restaurace.nazev, u.user_id AS uzivatel, k.user_id AS kuryr, objednavka.stav_objednavky, cesta.cena FROM objednavka JOIN uzivatel u ON objednavka.uzivatel_id=u.user_id JOIN cesta ON objednavka.objednavka_id = cesta.objednavka_id JOIN uzivatel k ON cesta.user_id = k.user_id JOIN uzivatel JOIN objednavka_produkt USING(objednavka_id)JOIN produkt USING(produkt_id)JOIN restaurace USING(restaurace_id)").fetchall()
        return statistika

    @staticmethod
    def update_stav(objednavka_id: int, novy_stav: str):
        db = get_db()
        sql = "UPDATE objednavka SET stav_objednavky = ? WHERE objednavka_id = ?"
        db.execute(sql, (novy_stav, objednavka_id))
        db.commit()
        return True