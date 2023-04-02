import sqlite3
from flask import Flask, g, render_template, request, redirect, url_for

app = Flask(__name__)
app.config['DATABASE'] = 'adres_defteri.db'
app.config['SECRET_KEY'] = 'gizli_anahtar'


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(error):
    if 'db' in g:
        g.db.close()

@app.route('/')
def index():
    db = get_db()
    kisiler = db.execute('SELECT * FROM kisiler').fetchall()
    return render_template('index.html', kisiler=kisiler)

@app.route('/ekle', methods=['GET', 'POST'])
def ekle():
    if request.method == 'POST':
        ad = request.form['ad']
        soyad = request.form['soyad']
        eposta = request.form['eposta']
        db = get_db()
        db.execute(
            'INSERT INTO kisiler (ad, soyad, eposta) VALUES (?, ?, ?)',
            (ad, soyad, eposta)
        )
        db.commit()
        return redirect(url_for('index'))
    return render_template('ekle.html')

@app.route('/duzenle/<int:kisi_id>', methods=['GET', 'POST'])
def duzenle(kisi_id):
    db = get_db()
    kisi = db.execute(
        'SELECT * FROM kisiler WHERE id = ?',
        (kisi_id,)
    ).fetchone()
    if request.method == 'POST':
        ad = request.form['ad']
        soyad = request.form['soyad']
        eposta = request.form['eposta']
        db.execute(
            'UPDATE kisiler SET ad = ?, soyad = ?, eposta = ? WHERE id = ?',
            (ad, soyad, eposta, kisi_id)
        )
        db.commit()
        return redirect(url_for('index'))
    return render_template('duzenle.html', kisi=kisi)

@app.route('/sil/<int:kisi_id>', methods=['GET', 'POST'])
def sil(kisi_id):
    # kisi_id'ye göre kişiyi sil
    db = get_db()
    db.execute("DELETE FROM kisiler WHERE id=?", (kisi_id,))
    db.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=False)
   
