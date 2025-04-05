from flask import Flask, jsonify
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from DataBase.Mysql_connection import Mysql_Connector

app = Flask(__name__)

@app.route('/')
def index():
    cnn =  Mysql_Connector.Connection()
    cursor = cnn[0]

    cursor.execute("USE Empregos")
    cursor.execute("SELECT * FROM Empregos")
    resultados = cursor.fetchall()

    empregos = list()

    for jobs in resultados:
        empregos.append(
            {
                "Title": jobs[0],
                "company_name": jobs[1],
                "location": jobs[2],
                "description": jobs[3],
                "salary": jobs[4],
            }
        )

    return jsonify(empregos)

if __name__ == '__main__':
    app.run(debug=True)