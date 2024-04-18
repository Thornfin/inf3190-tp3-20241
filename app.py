# file: app.py
from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a_secret_key_for_session_management'  # Necessary for session management

def get_db_connection():
    conn = sqlite3.connect('db/animaux.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    animaux = conn.execute('SELECT * FROM animaux ORDER BY RANDOM() LIMIT 5').fetchall()
    conn.close()
    return render_template('index.html', animaux=animaux)

@app.route('/add', methods=['GET', 'POST'])
def add_animal():
    if request.method == 'POST':
        nom = request.form['nom']
        espece = request.form['espece']
        race = request.form['race']
        age = request.form['age']
        description = request.form['description']
        courriel = request.form['courriel']
        adresse = request.form['adresse']
        ville = request.form['ville']
        cp = request.form['cp']
        if not (nom and espece and race and description and courriel and adresse and ville and cp):
            flash('All fields are required!', 'error')
        elif ',' in nom + espece + race + description + courriel + adresse + ville + cp:
            flash('Fields may not contain commas.', 'error')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO animaux (nom, espece, race, age, description, courriel, adresse, ville, cp) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', 
                         (nom, espece, race, int(age), description, courriel, adresse, ville, cp))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    return render_template('form.html')

@app.route('/animal/<int:id>')
def animal(id):
    conn = get_db_connection()
    animal = conn.execute('SELECT * FROM animaux WHERE id = ?', (id,)).fetchone()
    conn.close()
    if animal is None:
        return 'Animal not found!'
    return render_template('animal.html', animal=animal)

@app.route('/search')
def search():
    query = request.args.get('q', '')
    conn = get_db_connection()
    animaux = conn.execute('SELECT * FROM animaux WHERE nom LIKE ?', ('%' + query + '%',)).fetchall()
    conn.close()
    return render_template('search_results.html', animaux=animaux)

if __name__ == '__main__':
    app.run(debug=True)
