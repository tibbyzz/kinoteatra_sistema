from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__, template_folder='templates')

DATABASE = 'kino.db'


def create_tables():
  print("Creating tables...")
  conn = sqlite3.connect(DATABASE)
  c = conn.cursor()
  c.execute('''CREATE TABLE IF NOT EXISTS films (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              film_name TEXT NOT NULL,
              film_length TEXT NOT NULL,
              film_genre TEXT NOT NULL,
              sub_lang TEXT NOT NULL,
              audio_lang TEXT NOT NULL,
              distributor TEXT NOT NULL,
              director TEXT NOT NULL,
              film_description TEXT NOT NULL)''')
  c.execute('''CREATE TABLE IF NOT EXISTS seansi (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              films_id INTEGER,
              available_seats INTEGER,
              taken_seats INTEGER,
              time TEXT NOT NULL,
              date TEXT NOT NULL,
              FOREIGN KEY (films_id) REFERENCES films(id))''')
  c.execute('''CREATE TABLE IF NOT EXISTS workers(
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              name TEXT NOT NULL,
              last_name TEXT NOT NULL, 
              email TEXT NOT NULL,
              password TEXT NOT NULL,
              mobile_number TEXT NOT NULL)''')
  c.execute('''CREATE TABLE IF NOT EXISTS reservations (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              films_id INTEGER,
              name_r TEXT NOT NULL, 
              last_name_r TEXT NOT NULL, 
              mobile_number_r TEXT NOT NULL, 
              FOREIGN KEY (films_id) REFERENCES films(id)) ''')


create_tables()


#1.page
@app.route('/')
def start_page():
  return render_template('start_page.html')


#2.page
def get_all_films():
  conn = sqlite3.connect(DATABASE)
  c = conn.cursor()
  c.execute(
      "SELECT id, film_name, film_length, film_genre, sub_lang, audio_lang, distributor, director FROM films"
  )
  films = c.fetchall()
  conn.close()
  return films


@app.route('/all_seansi')
def all_seansi():
  sensi = get_all_seansi()
  return render_template('all_seansi.html', seansi=sensi)


@app.route('/all_seansi_authorized')
def all_seansi_authorized():
  sensi = get_all_seansi()
  return render_template('all_seansi_authorized.html', seansi=sensi)


#3.page


def get_film_desc():
  conn = sqlite3.connect(DATABASE)
  c = conn.cursor()
  c.execute("SELECT id, film_description FROM films")
  films = c.fetchall()
  conn.close
  return films


#4.page
@app.route('/reserveInfo', methods=['GET', 'POST'])
def reserveInfo():
  if request.method == 'POST':
    name_r = request.form['name_r']
    last_name_r = request.form['last_name_r']
    mobile_number_r = request.form['mobile_number_r']
    films_id = request.form['films_id']
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute(
        "INSERT INTO reservations (name_r,last_name_r,mobile_number_r,films_id) VALUES (?,?,?,?)",
        (name_r, last_name_r, mobile_number_r, films_id))
    conn.commit()
    conn.close()
    print(name_r, last_name_r, mobile_number_r, films_id)
    return redirect("/successful")

  else:
    films = get_all_films()
  return render_template("reserveInfo.html", films=films)


#5.page
@app.route('/successful')
def successful():
  return render_template('successful.html')


#6.page
@app.route('/authorize', methods=['GET', 'POST'])
def authorize():
  if request.method == 'POST':

    email = request.form.get('email')
    password = request.form.get('password')
    if check_credential(email, password):
      return redirect(url_for('manage_page'))
    else:
      return redirect(url_for('authorize'))
  else:
    return render_template("authorize.html")


#7page
@app.route('/manage')
def manage_page():
  return render_template("manage.html")


#8.page
@app.route('/new_film', methods=['GET', 'POST'])
def new_film():
  if request.method == 'POST':
    film_name = request.form['film_name']
    film_length = request.form['film_length']
    film_genre = request.form['film_genre']
    sub_lang = request.form['sub_lang']
    audio_lang = request.form['audio_lang']
    distributor = request.form['distributor']
    director = request.form['director']
    film_description = request.form['film_description']
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute(
        "INSERT INTO films (film_name, film_length, film_genre, sub_lang, audio_lang, distributor, director, film_description) VALUES (?,?,?,?,?,?,?,?)",
        (film_name, film_length, film_genre, sub_lang, audio_lang, distributor,
         director, film_description))
    conn.commit()
    conn.close()
    print(film_name, film_length, film_genre, sub_lang, audio_lang,
          distributor, director, film_description)
    return redirect("/manage")

  return render_template("new_film.html")


@app.route('/new_seans', methods=['GET', 'POST'])
def new_seans():
  if request.method == 'POST':
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    films_id = request.form['films_id']
    available_seats = request.form['available_seats']
    taken_seats = request.form['taken_seats']
    time = request.form['time']
    date = request.form['date']
    c.execute(
        "INSERT INTO seansi (films_id, available_seats, taken_seats, time, date) VALUES (?,?,?,?,?)",
        (films_id, available_seats, taken_seats, time, date))
    conn.commit()
    conn.close()
    return redirect("/manage")

  else:
    films = get_all_films()
    return render_template("new_seans.html", films=films)


#9.page
def get_all_films():
  conn = sqlite3.connect(DATABASE)
  c = conn.cursor()
  c.execute("SELECT * FROM films")
  films = c.fetchall()
  conn.close()
  return films


@app.route('/all_films')
def all_films():
  films = get_all_films()
  return render_template('all_films.html', films=films)


#10.page
def get_all_reservations():
  conn = sqlite3.connect(DATABASE)
  c = conn.cursor()
  c.execute('''SELECT f.film_name, r.name_r, r.last_name_r, r.mobile_number_r
            FROM reservations r
            JOIN films f ON r.films_id=f.id''')
  reservations = c.fetchall()
  conn.close()
  return reservations


@app.route('/all_reserv')
def all_reserv():
  reservations = get_all_reservations()
  return render_template('all_reserv.html', reservations=reservations)


#11.page
def get_all_seansi():
  conn = sqlite3.connect(DATABASE)
  c = conn.cursor()
  c.execute(
      '''SELECT f.film_name, s.available_seats, s.taken_seats, s.time, s.date, f.film_description
            FROM seansi s
            JOIN films f ON s.films_id=f.id ''')
  seansi = c.fetchall()
  conn.close()
  return seansi


@app.route('/seansi')
def seansi():
  seansi = get_all_seansi()
  return render_template('seansi.html', seansi=seansi)


@app.route('/register_worker', methods=['GET', 'POST'])
def register_employee():
  if request.method == 'POST':
    mail = request.form['email']
    password = request.form['password']
    name = request.form['workerName']
    lastName = request.form['workerLastName']
    mobile = request.form['workerMobile']
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute(
        "INSERT INTO workers (name, last_name, email, password, mobile_number) "
        "VALUES (?,?,?,?,?)", (name, lastName, mail, password, mobile))
    conn.commit()
    conn.close()
  return render_template('register_worker.html')


def check_credential(email, password):
  conn = sqlite3.connect(DATABASE)
  c = conn.cursor()
  c.execute("SELECT * FROM workers")
  all_rows = c.fetchall()
  for row in all_rows:
    print(row)
  c.execute("SELECT * FROM workers WHERE email=? AND password=?",
            (email, password))
  result = c.fetchone()
  conn.close()
  print(result is not None)
  return result is not None


if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0')
