from flask import Flask, request, jsonify, render_template
from flask_cors import CORS  # Добавляем CORS
import os

app = Flask(__name__)
CORS(app)  # Разрешаем запросы с других доменов (например, ngrok)

FILE_PATH = "/Users/air/Downloads/delivery_calculator-main/data.txt"

# Маршрут для проверки работы сервера
@app.route("/")
def home():
    return render_template("index.html")


# Основной маршрут для сохранения данных
@app.route("/save", methods=["POST"])
def save_data():
    try:
        data = request.json
        user_ip = request.remote_addr  # Получаем IP пользователя
        user_agent = request.headers.get("User-Agent")  # Браузер пользователя
        referrer = request.headers.get("Referer")  # Откуда пришел пользователь (если есть)

        # Получаем Telegram ID и доп. данные
        telegram_id = data.get("telegram_id")
        username = data.get("username")
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        language_code = data.get("language_code")

        print(f"Полученные данные: {data}")  # Логируем всё

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO deliveries 
            (category, weight, length, width, height, cost, quantity, user_ip, user_agent, referrer, 
             telegram_id, username, first_name, last_name, language_code)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (data["category"], data["weight"], data["length"], data["width"],
              data["height"], data["cost"], data["quantity"], user_ip, user_agent, referrer,
              telegram_id, username, first_name, last_name, language_code))

        conn.commit()
        cur.close()
        conn.close()

        print(f"✅ Данные сохранены в БД: {data}")
        return jsonify({"status": "success", "message": "Данные сохранены в БД"}), 200

    except Exception as e:
        print("❌ Ошибка при записи в БД:", e)
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
