from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import psycopg2
import os

app = Flask(__name__, template_folder="templates")
CORS(app)

# Параметры подключения к БД
DB_HOST = "78.40.108.122"
DB_PORT = "5432"
DB_NAME = "mydb"
DB_USER = "myuser"
DB_PASSWORD = "mypassword123"

# Подключение к базе
def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    return conn

# Создание таблицы, если её нет
def create_table():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS deliveries (
            id SERIAL PRIMARY KEY,
            category TEXT,
            weight REAL,
            length REAL,
            width REAL,
            height REAL,
            cost REAL,
            quantity INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            user_ip TEXT,
            user_agent TEXT,
            telegram_id BIGINT
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

# Главная страница
@app.route("/")
def home():
    return render_template("index.html")

# Сохранение данных в БД с логированием
@app.route("/save", methods=["POST"])
def save_data():
    try:
        data = request.json
        user_ip = request.remote_addr
        user_agent = request.headers.get("User-Agent")
        telegram_id = data.get("telegram_id")

        print(f"Полученные данные: {data}")  # Логируем всё
        print(f"Telegram ID: {telegram_id}")  # Логируем Telegram ID

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO deliveries (category, weight, length, width, height, cost, quantity, user_ip, user_agent, telegram_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (data["category"], data["weight"], data["length"], data["width"],
              data["height"], data["cost"], data["quantity"], user_ip, user_agent, telegram_id))

        conn.commit()
        cur.close()
        conn.close()

        print(f"Данные сохранены в БД: {data}")
        return jsonify({"status": "success", "message": "Данные сохранены в БД"}), 200

    except Exception as e:
        print("Ошибка при записи в БД:", e)
        return jsonify({"status": "error", "message": str(e)}), 500


# Запуск сервера
if __name__ == "__main__":
    create_table()  # Создаём таблицу при старте
    app.run(host="0.0.0.0", port=8080, debug=True)
