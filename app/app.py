import time
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

@app.route('/')
def index():
    #return '<a href="http://127.0.0.1:5000/html/index.html">Dovážková služba</a>'

    kategorie_id = request.args.get("kategorie_id", None, int)

    restaurace = RestauraceService.get_all(kategorie_id)
    kategorie = RestauraceService.get_category_name(kategorie_id)
    return render_template('/html/index.html',
                           restaurace=restaurace,
                           kategorie = kategorie
                           )

@app.route('/objednavky')
def view_objednavka_page():
    objednavky = ObjednavkaService.get_all()
    pocet_objednavek = ObjednavkaService.get_pocet()
    mnozstevni_sleva = ObjednavkaService.get_mnozstevni_slevu()
    return render_template('/html/menu/objednavky.html',
                           objednavky=objednavky,
                           pocet_objednavek=pocet_objednavek,
                           mnozstevni_sleva=mnozstevni_sleva
                           )

@app.route('/vyber')
def view_vyber_page():
    nevyrizene = ObjednavkaService.get_nevyrizene()
    volne = ObjednavkaService.get_volne_objednavky()
    vyrizene = ObjednavkaService.get_vyrizene()
    return render_template('/html/menu/vyberobjednavek.html',
                           nevyrizene=nevyrizene,
                           volne=volne,
                           vyrizene=vyrizene)

@app.route('/statistika')
def view_statistika_page():
    pocet_objednavek = ObjednavkaService.get_pocet()
    objednavky = ObjednavkaService.get_statistika()
    return render_template('/html/menu/statistika.html',
                           objednavky=objednavky,
                           pocet_objednavek = pocet_objednavek
                           )

@app.route('/uzivatele')
def view_prehled_uzivatelu_page():
    uzivatele = UzivateleService.get_role_uzivatelu()
    role = UzivateleService.get_role()
    return render_template('/html/menu/uzivatele.html',
                           uzivatele=uzivatele,
                           role = role
                           )


@app.route('/produkty')
def view_produkty_page():
    restaurace_id = request.args.get("restaurace_id", None, int)
    restaurace = RestauraceService.get_by_id(restaurace_id)
    produkty = ProduktyService.get_prudukty_restaurace(restaurace_id)
    return  render_template('/html/produkty.html',
                            produkty = produkty,
                            restaurace = restaurace
                            )

@app.route('/objednat')
def view_objednat_page():
    restaurace_id = request.args.get("restaurace_id", None, int)
    restaurace = RestauraceService.get_by_id(restaurace_id)
    produkty = ProduktyService.get_prudukty_restaurace(restaurace_id)
    return render_template('/html/objednani.html',
                           produkty = produkty,
                           restaurace = restaurace
                           )

@app.get("/registrace")
def view_registrace():
    return render_template('/html/menu/registrace.html')

@app.post("/registrace")
def action_registrace():

    # TODO: Přidat ostatní data z formuláře pro registraci
    data = request.form.to_dict()
    
    if 'name' not in data or 'surname' not in data:
        return render_template('/html/menu/registrace.html', error='Invalid data.')
    
    if UzivateleService.get_uzivatel_by_phone(data['telefon']) == None:
        return render_template('/html/menu/registrace.html', error='User with this phone already exists.')

    # Zahashovat heslo
    data['heslo'] = hash(data['heslo'])

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

    # TODO: Kontrolovat heslo uzivatele
    # TODO: Pouzivat Timing attack safe porovnani
    # TODO: Pouzivat lepsi hashovani
    if user == None or hash(data['heslo']) != data['heslo']:
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
        # TODO: Najit uzivatele podle user_id pomoci UzivateleService
        # user = UzivateleService.get_uzivatel(user_id)
        # print(f'found user {user.id} from session')
        pass

    return user

@app.route('/update_role', methods=['POST'])
def update_role():
    user_id = request.form.get('submit_button', None, int)
    new_role_id = request.form.get('role_select', None, int)
    UzivateleService.update_role_uzivatele(user_id, new_role_id)
    return redirect('/uzivatele')

if __name__ == '__main__':
    app.run(debug=True, port=5000)