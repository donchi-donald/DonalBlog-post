import sqlite3

#öffnen dann eine Verbindung zu einer Datenbankdatei namens database.db, die erstellt wird, sobald Sie die Python-Datei ausführen.
connection = sqlite3.connect('database.db')

#Dann verwenden Sie die Funktion open(), um die Datei schema.sql zu öffnen. 
with open('schema.sql') as f:
    connection.executescript(f.read()) #Als Nächstes führen Sie ihre Inhalte mit der Methode executescript() aus, die mehrere SQL-Anweisungen auf einmal ausführt. Dadurch wird die Tabelle posts erstellt.

"""
Sie erstellen ein Cursor-Objekt, mit dem Sie die Methode execute() verwenden können, 
um zwei INSERT SQL-Anweisungen auszuführen und Ihrer Tabelle posts zwei Blogbeiträge hinzuzufügen. 
Schließlich committen Sie die Änderungen und schließen die Verbindung.

Speichern und schließen Sie die Datei und führen Sie sie dann im Terminal mit dem python-Befehl aus:
"""

cur = connection.cursor() 

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('First Post', 'Content for the first post')
            )

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('Second Post', 'Content for the second post')
            )

connection.commit()
connection.close()