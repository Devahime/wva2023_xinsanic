DROP TABLE IF EXISTS role_uzivatele;
DROP TABLE IF EXISTS objednavka;
DROP TABLE IF EXISTS cesta;
DROP TABLE IF EXISTS objednavka_produkt;
DROP TABLE IF EXISTS uzivatel;
DROP TABLE IF EXISTS heslo;
DROP TABLE IF EXISTS produkt;
DROP TABLE IF EXISTS restaurace_kategorie;
DROP TABLE IF EXISTS role;
DROP TABLE IF EXISTS kategorie;
DROP TABLE IF EXISTS restaurace;


create table kategorie
(
    kategorie_id INTEGER
        primary key,
    nazev        TEXT
);

create table restaurace
(
    restaurace_id INTEGER
        primary key,
    nazev         TEXT,
    telefon       TEXT
        unique,

	obrazekrestaurace	TEXT,
    adresa        TEXT
    uzivatel_id INTEGER references uzivatel
);

create table produkt
(
    produkt_id    INTEGER
        primary key,
    nazev         TEXT,
    popis         TEXT,
    cena          INTEGER,
    dostupny_od   TEXT,
    dostupne_do   TEXT,
	obrazek	TEXT,
    restaurace_id INTEGER
        references restaurace
);

create table restaurace_kategorie
(
    restaurace_kategorie_id INTEGER
        primary key,
    restaurace_id           INTEGER
        references restaurace,
    kategorie_id            INTEGER
        references kategorie
);

create table role
(
    role_id INTEGER
        primary key,
    nazev   TEXT
);



create table uzivatel
(
    user_id        INTEGER
        primary key,
    jmeno          TEXT,
    prijmeni       TEXT,
    telefon        TEXT
        unique,
    adresa         TEXT,
    platebni_karta TEXT
);

create table heslo
(
    heslo_id  INTEGER
        primary key,
    heslo     TEXT,
    platne_od TEXT,
    user_id   INTEGER
        references uzivatel
);

create table objednavka
(
    objednavka_id   INTEGER
        primary key,
    cena            INTEGER,
    vytvoreni       TEXT,
    stav_objednavky TEXT,
    uzivatel_id     INTEGER
        references uzivatel
);

create table cesta
(
    cesta_id      INTEGER
        primary key,
    user_id       INTEGER
        references uzivatel,
    cena          INTEGER,
    objednavka_id INTEGER
        references objednavka
);

create table objednavka_produkt
(
    objednavka_produkt_id INTEGER
        primary key,
    mnozstvi              INTEGER,
    objednavka_id         INTEGER
        references objednavka,
    produkt_id            INTEGER
        references produkt
);

create table role_uzivatele
(
    role_uzivatele_id INTEGER
        primary key,
    role_id           INTEGER
        references role,
    uzivatele_id      INTEGER
        references uzivatel
);


