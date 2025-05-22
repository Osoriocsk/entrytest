from flask import Flask, request, redirect, url_for, render_template_string, flash
import sqlite3
import requests
import os

app = Flask(__name__)
app.secret_key = 'cambiar_por_una_clave_segura'

DB_NAME = 'users.db'

# ——— Inicialización de la base de datos ———
def init_db():
    if not os.path.exists(DB_NAME):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE usuarios (
                username TEXT PRIMARY KEY,
                password TEXT NOT NULL
            );
        ''')
        # Usuario por defecto Santiago / 1234
        cursor.execute(
            "INSERT INTO usuarios (username, password) VALUES (?, ?)",
            ('Santiago', '1234')
        )
        conn.commit()
        conn.close()

# ——— Funciones de acceso a datos ———
def validate_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT 1 FROM usuarios WHERE username = ? AND password = ?",
        (username, password)
    )
    found = cursor.fetchone() is not None
    conn.close()
    return found

def fetch_characters():
    """
    Llama a la API de Rick & Morty y devuelve una lista de diccionarios
    con los campos que queremos mostrar.
    """
    API_URL = 'https://rickandmortyapi.com/api/character'
    try:
        r = requests.get(API_URL, timeout=5)
        r.raise_for_status()
        results = r.json().get('results', [])
        # Mapeamos a solo los campos que nos interesan:
        characters = []
        for c in results:
            characters.append({
                'name':    c['name'],
                'status':  c['status'],
                'species': c['species'],
                'gender':  c['gender'],
                'origin':  c['origin']['name'],
                'image':   c['image']
            })
        return characters
    except Exception as e:
        return []

# ——— Templates inline ———

# Login (igual que antes)
login_page = """
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <title>Login</title>
  <style>
    body { font-family: Arial, sans-serif; background: #f5f5f5; }
    .container { width: 300px; margin: 100px auto; padding: 20px;
                 background: white; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
    input { width: 100%; padding: 8px; margin: 6px 0; }
    button { width: 100%; padding: 8px; background: #007BFF;
             color: white; border: none; cursor: pointer; }
    .error { color: red; }
  </style>
</head>
<body>
  <div class="container">
    <h2>Login</h2>
    {% with messages = get_flashed_messages() %}
      {% if messages %}
        <div class="error">{{ messages[0] }}</div>
      {% endif %}
    {% endwith %}
    <form method="post">
      <input type="text"   name="username" placeholder="Usuario" required>
      <input type="password" name="password" placeholder="Contraseña" required>
      <button type="submit">Entrar</button>
    </form>
  </div>
</body>
</html>
"""

# Página de personajes con tarjetas
chars_page = """
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <title>Personajes R&M</title>
  <style>
    body { font-family: Arial, sans-serif; background: #fafafa; }
    .container { width: 90%; max-width: 1000px; margin: 30px auto; }
    .grid { display: flex; flex-wrap: wrap; gap: 20px; }
    .card {
      background: white; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);
      width: calc(25% - 20px); min-width: 200px; overflow: hidden;
      display: flex; flex-direction: column;
    }
    .card img { width: 100%; height: auto; }
    .card-body { padding: 10px; flex: 1; display: flex; flex-direction: column; }
    .card-body h3 { margin: 0 0 8px; font-size: 1.1em; }
    .card-body p { margin: 4px 0; font-size: 0.9em; }
    .logout { display: inline-block; margin-bottom: 20px;
              text-decoration: none; color: #007BFF; }
  </style>
</head>
<body>
  <div class="container">
    <a href="{{ url_for('login') }}" class="logout">← Cerrar sesión</a>
    <h1>Rick & Morty Characters</h1>
    <div class="grid">
      {% for c in characters %}
      <div class="card">
        <img src="{{ c.image }}" alt="{{ c.name }}">
        <div class="card-body">
          <h3>{{ c.name }}</h3>
          <p><strong>Estatus:</strong> {{ c.status }}</p>
          <p><strong>Especie:</strong> {{ c.species }}</p>
          <p><strong>Género:</strong> {{ c.gender }}</p>
          <p><strong>Origen:</strong> {{ c.origin }}</p>
        </div>
      </div>
      {% endfor %}
    </div>
  </div>
</body>
</html>
"""

# ——— Rutas web ———
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['username'].strip()
        pwd  = request.form['password'].strip()
        if validate_user(user, pwd):
            return redirect(url_for('characters'))
        else:
            flash('Usuario o contraseña incorrectos.')
    return render_template_string(login_page)

@app.route('/characters')
def characters():
    chars = fetch_characters()
    return render_template_string(chars_page, characters=chars)

# ——— Main ———
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
