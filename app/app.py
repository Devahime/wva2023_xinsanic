from flask import Flask, render_template, request

from database import database

from restaurace_service import RestauraceService
from objednavka_service import ObjednavkaService
from uzivatele_service import UzivateleService

app = Flask(__name__, static_folder='static', static_url_path='/static')

app = Flask(__name__)
app.config['DEBUG'] = True
app.config.from_object('config')
database.init_app(app)

@app.route('/')
def index():
    #return '<a href="http://127.0.0.1:5000/html/index.html">Dovážková služba</a>'
    restaurace = RestauraceService.get_all()
    return render_template('/html/index.html', restaurace=restaurace)

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
                           nevyrizene=nevyrizene, volne=volne, vyrizene=vyrizene)

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
    return render_template('/html/menu/uzivatele.html',
                           uzivatele=uzivatele
                           )


if __name__ == '__main__':
    app.run(debug=True, port=5000)