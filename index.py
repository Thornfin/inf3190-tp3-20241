# Copyright 2024 <Votre nom et code permanent>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# file: app.py
# file: app.py
# file: index.py
from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a_secret_key_for_session_management'

def get_db_connection():
    conn = sqlite3.connect('db/animaux.db')
    conn.row_factory = sqlite3.Row
    return conn

def validate_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def validate_postal_code(cp):
    return re.match(r"^[A-Za-z]\d[A-Za-z][ -]?\d[A-Za-z]\d$", cp)

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

        # Validation logic
        if not (nom and espece and race and description and courriel and adresse and ville and cp):
            flash('All fields are required!', 'error')
        elif ',' in nom + espece + race + description + courriel + adresse + ville + cp:
            flash('Fields may not contain commas.', 'error')
        elif len(nom) < 3 or len(nom) > 20:
            flash('Name must be between 3 and 20 characters.', 'error')
        elif not age.isdigit() or not (0 <= int(age) <= 30):
            flash('Age must be a number between 0 and 30.', 'error')
        elif not validate_email(courriel):
            flash('Invalid email format.', 'error')
        elif not validate_postal_code(cp):
            flash('Invalid Canadian postal code format.', 'error')
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
    return render_template('search_results.html', query=query, animaux=animaux)

if __name__ == '__main__':
    app.run(debug=True)
