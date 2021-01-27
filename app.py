import sqlite3 
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort


"""
Diese get_db_connection()-Funktion öffnet eine Verbindung zur Datenbankdatei database.db und legt dann das Attribut row_factory 
auf sqlite3. Row fest, damit Sie namenbasierten Zugriff auf Spalten erhalten.
 Das bedeutet, dass die Datenbankverbindung Zeilen zurückgibt, die sich wie reguelmäßige Python-Wörterbücher verhalten.

 Schließlich gibt die Funktion das Verbindungsobjekt conn zurück, das Sie zum Zugriff auf die Datenbank verwenden werden.

"""
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

"""
post_id-Argument, das bestimmt, welcher Blogbeitrag zurückgegeben wird.
Innerhalb der Funktion verwenden Sie die Funktion get_db_connection() zum Öffnen einer Datenbankverbindung 
und Ausführen einer SQL-Abfrage, um den Blogbeitrag zu erhalten, der mit dem angegebenen post_id-Wert verknüpft ist. 
Sie fügen die Methode fetchone() hinzu, um das Ergebnis zu erhalten und in der Variable post zu speichern. 
Dann schließen Sie die Verbindung. 
Wenn die Variable post den Wert None (Keine) hat, was bedeutet, dass in der Datenbank
 kein Ergebnis gefunden wird, verwenden Sie die Funktion abort(), die Sie zuvor importiert haben,
  um mit einem 404-Fehlercode zu reagieren; die Ausführung der Funktion wird beendet. 
  Wenn jedoch ein Beitrag gefunden wurde, geben Sie den Wert der Variable post zurück.

"""
def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post


app = Flask(__name__)
app.config['SECRET_KEY'] = 'doni'

@app.route('/')
def index():
    conn = get_db_connection() #ich mache hier eine Datenbankverbindung
    posts = conn.execute('SELECT * FROM posts').fetchall() #ich führe eine SQL-Abfrage, um alle Einträge aus der Tabelle posts auszuwählen, mit fetchall um alle zeile abzurufen
    conn.close()
    return render_template('index.html', posts=posts) # Das teilt render_template() mit, nach einer Datei namens index.html im Ordner templates zu suchen. ,ich übergebe  das Objekt posts als Argument, das die Ergebnisse enthält, die Sie aus der Datenbank erhalten haben. Das ermöglicht Ihnen, auf die Blogbeiträge in der Vorlage index.html zuzugreifen.


"""
In dieser neuen Ansichtsfunktion fügen Sie eine Variablenregel <int:post_id> hinzu, um
anzugeben, dass der Teil nach dem Schrägstrich (/) eine positive ganze Zahl ist (markiert mit dem
int-Konverter), die Sie in Ihrer Ansichtsfunktion aufrufen müssen. Flask erkennt das und übergibt
ihren Wert an das Schlüsselwortargument post_id Ihrer post()-Ansichtsfunktion. Dann
verwenden Sie die Funktion get_post(), um den Blogbeitrag abzurufen, der mit der angegebenen
ID verknüpft ist, und speichern das Ergebnis in der Variable post, die Sie an eine post.html-
Vorlage, die Sie bald erstellen werden, übergeben.
"""
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)

"""
Dadurch wird eine /create-Route erstellt, die sowohl GET- als auch POST-Anfragen akzeptiert.
GET-Anfragen werden standardmäßig akzeptiert. Um auch POST-Anfragen zu akzeptieren, die
vom Browser beim Übermitteln von Formularen gesendet werden, übergeben Sie ein Tupel mit
den akzeptierten Arten von Anfragen an das methods-Argument des @app.route()-Decorators.
"""
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)', (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('create.html')

"""
Der Beitrag, den Sie bearbeiten, wird von der URL bestimmt; Flask übergibt die ID-Nummer an die
Funktion edit() über das Argument id. Sie fügen diesen Wert der Funktion get_post() hinzu, um
den Beitrag, der mit der bereitgestellten ID verknüpft ist, aus der Datenbank abzurufen. Die neuen
Daten kommen in einer POST-Anfrage, die in der Bedingung if request.method == 'POST'
verwaltet wird.
"""
@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Du muss den Titel bitte eingeben!!!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, content = ?'  'WHERE id = ?',(title, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)

"""

"""
@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" wurde erfolgreich gelöscht!!!'.format(post['title']))
    return redirect(url_for('index'))