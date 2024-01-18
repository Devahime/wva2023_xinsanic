import time
import bcrypt
from flask import Flask, make_response, redirect, render_template, request

from database import database

from restaurace_service import RestauraceService
from objednavka_service import ObjednavkaService
from uzivatele_service import UzivateleService
from produkty_service import ProduktyService

app = Flask(__name__, static_folder='static', static_url_path='/static')

app = Flask(__name__)
app.config['DEBUG'] = True
app.config.from_object('config')
database.init_app(app)


def check_user_authentication():
    user_id_cookie = request.cookies.get('connect.sid')
    return user_id_cookie is not None

def get_logged_in_user():
    user_authenticated = check_user_authentication()

    if user_authenticated:
        user_id = request.cookies.get('connect.sid')
        prihlaseny = UzivateleService.najit_uzivatele(int(user_id))
        return prihlaseny
    else:
        return None

def get_role_prihlaseneho_uzivatele():
    role = UzivateleService.get_role_by_id(int(request.cookies.get('connect.sid')))
    return role

@app.route('/')
def index():
    #return '<a href="http://127.0.0.1:5000/html/index.html">Dovážková služba</a>'

    kategorie_id = request.args.get("kategorie_id", None, int)

    restaurace = RestauraceService.get_all(kategorie_id)
    kategorie = RestauraceService.get_category_name(kategorie_id)

    prihlaseny = get_logged_in_user()

    return render_template('/html/index.html',
                           restaurace=restaurace,
                           kategorie = kategorie,
                           prihlaseny=prihlaseny
                           )

@app.route('/mujprofil')
def view_profil_page():

    prihlaseny = get_logged_in_user()

    if prihlaseny == None:
        return render_template('/html/neprihlaseny_uzivatel.html',
                               prihlaseny=prihlaseny
                               )

    return render_template('/html/menu/mujprofil.html',
                           prihlaseny=prihlaseny
                           )

@app.route('/objednavky')
def view_objednavka_page():

    prihlaseny = get_logged_in_user()

    if prihlaseny == None:
        return render_template('/html/neprihlaseny_uzivatel.html',
                               prihlaseny=prihlaseny
                               )

    pocet_objednavek = ObjednavkaService.get_moje_objednavky_pocet(int(request.cookies.get('connect.sid')))
    objednavky = ObjednavkaService.get_moje_objednavky(int(request.cookies.get('connect.sid')))
    mnozstevni_sleva = ObjednavkaService.get_moje_mnozstevni_slevu(int(request.cookies.get('connect.sid')))



    return render_template('/html/menu/objednavky.html',
                           objednavky=objednavky,
                           pocet_objednavek=pocet_objednavek,
                           mnozstevni_sleva=mnozstevni_sleva,
                           prihlaseny=prihlaseny
                           )

#@app.route('/platebniudaje')
#def view_udaje_page():

    #prihlaseny = get_logged_in_user()

    #return render_template('/html/menu/platebniudaje.html',
                           #prihlaseny=prihlaseny
                           #)



@app.route('/vyber')
def view_vyber_page():
    volne = ObjednavkaService.get_volne_objednavky()

    prihlaseny = get_logged_in_user()

    if prihlaseny == None:
        return render_template('/html/neprihlaseny_uzivatel.html',
                               prihlaseny=prihlaseny
                               )
    if get_role_prihlaseneho_uzivatele() != 'kuryr' or get_role_prihlaseneho_uzivatele() != 'admin':
        return render_template('/html/neopraveneny_pristup.html',
                               prihlaseny=prihlaseny
                               )

    vyrizene = ObjednavkaService.get_moje_vyrizene(int(request.cookies.get('connect.sid')))
    nevyrizene = ObjednavkaService.get_moje_nevyrizene(int(request.cookies.get('connect.sid')))



    return render_template('/html/menu/vyberobjednavek.html',
                           nevyrizene=nevyrizene,
                           volne=volne,
                           vyrizene=vyrizene,
                           prihlaseny=prihlaseny
                           )

@app.route('/statistika')
def view_statistika_page():
    pocet_objednavek = ObjednavkaService.get_pocet()
    objednavky = ObjednavkaService.get_statistika()

    prihlaseny = get_logged_in_user()

    if prihlaseny == None:
        return render_template('/html/neprihlaseny_uzivatel.html',
                               prihlaseny=prihlaseny
                               )

    if get_role_prihlaseneho_uzivatele() != 'admin':
        return render_template('/html/neopraveneny_pristup.html',
                               prihlaseny=prihlaseny
                               )

    vysledek = ObjednavkaService.get_castky()

    celkova_cena_cesty = round(vysledek['celkova_cena_cesty'], 1)
    celkova_cena_proviz = round(vysledek['celkova_cena_proviz'], 1)
    celkovy_zisk = round(vysledek['celkovy_zisk'], 1)



    return render_template('/html/menu/statistika.html',
                           objednavky=objednavky,
                           pocet_objednavek = pocet_objednavek,
                           prihlaseny=prihlaseny,
                             celkova_cena_cesty=celkova_cena_cesty,
                        celkova_cena_proviz=celkova_cena_proviz,
                        celkovy_zisk=celkovy_zisk,
                           )

@app.route('/uzivatele')
def view_prehled_uzivatelu_page():
    uzivatele = UzivateleService.get_role_uzivatelu()
    role = UzivateleService.get_role()

    prihlaseny = get_logged_in_user()

    if get_role_prihlaseneho_uzivatele() != 'admin':
        return render_template('/html/neopraveneny_pristup.html',
                               prihlaseny=prihlaseny
                               )

    if prihlaseny == None:
        return render_template('/html/neprihlaseny_uzivatel.html',
                               prihlaseny=prihlaseny
                               )

    return render_template('/html/menu/uzivatele.html',
                           uzivatele=uzivatele,
                           role = role,
                           prihlaseny=prihlaseny
                           )

@app.route('/produkty')
def view_produkty_page():
    restaurace_id = request.args.get("restaurace_id", None, int)
    restaurace = RestauraceService.get_by_id(restaurace_id)

    prihlaseny = get_logged_in_user()

    show_unavailable = request.args.get("unavailable", False, bool)
    show_upcoming = request.args.get("upcoming", False, bool)
    show_limited = request.args.get("limited", False, bool)

    if prihlaseny == None:
        return render_template('/html/neprihlaseny_uzivatel.html',
                               prihlaseny=prihlaseny
                               )

    if show_unavailable:
            produkty = ProduktyService.get_nadchazejici_produkty(restaurace_id)
    elif show_upcoming:
            produkty = ProduktyService.get_nedostupne_produkty(restaurace_id)
    elif show_limited:
            produkty = ProduktyService.get_limitovane_dostupne(restaurace_id)
    else:
            produkty = ProduktyService.get_zobrazit_dostupne(restaurace_id)

    return render_template('/html/produkty.html',
                           produkty=produkty,
                           restaurace=restaurace,
                           show_unavailable=show_unavailable,
                           show_upcoming=show_upcoming,
                           show_limited=show_limited,
                           prihlaseny=prihlaseny
                           )


@app.route('/objednat')
def view_objednat_page():
    restaurace_id = request.args.get("restaurace_id", None, int)
    restaurace = RestauraceService.get_by_id(restaurace_id)
    show_limited = request.args.get("limited", False, bool)

    prihlaseny = get_logged_in_user()

    if show_limited:
        produkty = ProduktyService.get_limitovane_dostupne(restaurace_id)
    else:
        produkty = ProduktyService.get_zobrazit_dostupne(restaurace_id)



    if prihlaseny == None:
        return render_template('/html/neprihlaseny_uzivatel.html',
                               prihlaseny=prihlaseny
                               )

    return render_template('/html/objednani.html',
                           produkty = produkty,
                           restaurace = restaurace,
                           show_limited = show_limited,
                           prihlaseny=prihlaseny
                           )


@app.get("/registrace")
def view_registrace():
    return render_template('/html/menu/registrace.html')

@app.post("/registrace")
def action_registrace():

    data = request.form.to_dict()

    if 'name' not in data or 'surname' not in data:
        return render_template('/html/menu/registrace.html', error='Invalid data.')

    if UzivateleService.get_uzivatel_by_phone(data['telefon']) != None:
        return render_template('/html/menu/registrace.html', error='Uživatel s tímto telefonním číslem je již zaregistrován.')

    if 'adresa' not in data:
        return render_template('/html/menu/registrace.html', error='Invalid data.')

    # snaha zahashovat heslo pres bcrypt
    plain_password = data['heslo'].encode('utf-8')
    hashed_password = bcrypt.hashpw(plain_password, bcrypt.gensalt())
    data['heslo'] = hashed_password

    user = UzivateleService.create_uzivatel(data)

    print(f'created user {user["user_id"]}')

    return render_template('/html/menu/prihlaseni.html')

@app.get("/prihlaseni")
def view_prihlaseni():
    return render_template('/html/menu/prihlaseni.html')

@app.post("/prihlaseni")
def action_prihlaseni():

    data = request.form.to_dict()

    if not data['telefon']:
        return render_template('/html/menu/prihlaseni.html', error='Nezadali jste tel. cislo.')

    if not data['heslo']:
        return render_template('/html/menu/prihlaseni.html', error='Nezadali jste heslo')

    user = UzivateleService.get_uzivatel_by_phone(data['telefon'])

    if user is None or not bcrypt.checkpw(data['heslo'].encode('utf-8'), user['heslo']):
        return render_template('/html/menu/prihlaseni.html', error='Špatné údaje')

    response = make_response(redirect('/'))
    response.set_cookie('connect.sid', str(user["user_id"]), expires=time.time() + 3600)
    return response

@app.get("/odhlaseni")
def view_odhlaseni():
    response = make_response(render_template('/html/menu/odhlaseni.html'))

    response.set_cookie('connect.sid', '', expires=time.time() - 3600)

    return response

def start_session():
    user = None
    user_id = request.cookies.get('connect.sid')

    print(f'Session user ID: {user_id}')

    if user_id is not None:
        user = UzivateleService.get_uzivatel_by_id(user_id)
        print(f'found user {user["user_id"]} from session')

    return user

@app.route('/update_role', methods=['POST'])
def update_role():
    user_id = request.form.get('submit_button', None, int)
    new_role_id = request.form.get('role_select', None, int)
    UzivateleService.update_role_uzivatele(user_id, new_role_id)
    return redirect('/uzivatele')

@app.route('/update_objednavky', methods=['POST'])
def update_stav_objednavky():
    objednavka_id = request.form.get('objednavka_id', None, int)
    novy_stav = request.form.get('novy_stav', None, str)

    ObjednavkaService.update_stav(objednavka_id, novy_stav)
    ObjednavkaService.create_or_update_cesta(objednavka_id, int(request.cookies.get('connect.sid')))

    return redirect('/vyber')


@app.route('/some-protected-route')
def protected_route():
    user_id = request.cookies.get('connect.sid')

    if user_id:
        user = UzivateleService.najit_uzivatele(int(user_id))
        if user:
            return f"Hello {user['jmeno']}, you are logged in!"
        else:
            return "User not found."
    else:
        return redirect('/prihlaseni')

@app.route('/objednat', methods=['POST'])
def objednat():
    prihlaseny_user_id = request.form.get('prihlaseny_uzivatel')
    stav = request.form.get('stav')

    product_quantities = {}
    for key, value in request.form.items():
        if key.startswith('quantity_'):
            product_id = key.split('_')[1]
            product_quantities[product_id] = int(value)

    total_cost = calculate_total_cost(product_quantities)

    print(f"User ID: {prihlaseny_user_id}")
    print(f"Stav: {stav}")
    print("Product Quantities:", product_quantities)
    print(f"Total Cost: {total_cost}")

    ProduktyService.vlozit_do_databaze(prihlaseny_user_id, stav, product_quantities, total_cost)

    return redirect('/mujprofil')

def calculate_total_cost(product_quantities):
    product_prices = {str(row['produkt_id']): float(row['cena']) for row in ProduktyService.funkce_na_soucet()}

    total_cost = sum(product_prices[product_id] * quantity for product_id, quantity in product_quantities.items())
    return total_cost

if __name__ == '__main__':
    app.run(debug=True, port=5000)