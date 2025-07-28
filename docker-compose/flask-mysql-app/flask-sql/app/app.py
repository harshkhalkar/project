from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)

@app.route('/')
def hello():
    try:
        conn = mysql.connector.connect(
            host='db-sql',
            user='root',
            password='123',
            database='myapp'
        )
        cursor = conn.cursor()
        cursor.execute("SELECT message FROM greetings LIMIT 1;")
        result = cursor.fetchone()
        return jsonify({"message": result[0]})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
