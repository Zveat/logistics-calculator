from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Данные по городским перевозкам
city_data = [
    {"Вид транспорта": "Легковая машина", "Вес груза": 40, "Длинна груза": 2, "Стоимость доставки": "4000-8000"},
    {"Вид транспорта": "Газель", "Вес груза": 300, "Длинна груза": 3, "Стоимость доставки": "4000-12000"},
    {"Вид транспорта": "Длинномер/бортовой", "Вес груза": 1000, "Длинна груза": 12, "Стоимость доставки": "30000-35000"},
    {"Вид транспорта": "Газель Бортовая", "Вес груза": 2000, "Длинна груза": 4, "Стоимость доставки": "10000-20000"},
    {"Вид транспорта": "Бортовой грузовик", "Вес груза": 6000, "Длинна груза": 7, "Стоимость доставки": "20000-30000"},
    {"Вид транспорта": "Фура", "Вес груза": 23000, "Длинна груза": 12, "Стоимость доставки": "50000-60000"}
]

# Данные по междугородним перевозкам
intercity_data = {
    "Алматы-Астана": 500000,
    "Алматы-Шымкент": 300000,
    "Алматы-Актау": 1200000,
    "Алматы-Атырау": 800000
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calculate_city', methods=['POST'])
def calculate_city():
    data = request.get_json()
    weight = data.get('weight')
    length = data.get('length')

    suitable_options = [
        entry for entry in city_data if weight <= entry['Вес груза'] and (length is None or length <= entry['Длинна груза'])
    ]

    if not suitable_options:
        return jsonify({"result": "Нет подходящих вариантов"})

    suitable_options.sort(key=lambda x: int(x["Стоимость доставки"].split('-')[0]))

    best_option = suitable_options[0]
    alternative_option = suitable_options[1] if len(suitable_options) > 1 else None

    response = {
        "Лучший вариант": f"{best_option['Вид транспорта']} ({best_option['Стоимость доставки']} тг)"
    }

    if alternative_option:
        response["Альтернатива"] = f"{alternative_option['Вид транспорта']} ({alternative_option['Стоимость доставки']} тг)"

    return jsonify(response)

@app.route('/calculate_intercity', methods=['POST'])
def calculate_intercity():
    data = request.get_json()
    direction = data.get('direction')
    weight = data.get('weight')

    if direction not in intercity_data:
        return jsonify({"result": "Нет данных по данному направлению"})

    tariff = intercity_data[direction]
    capacity = 20  # Фура до 20 тонн
    coef = 2  # Коэффициент догруза

    cost = (tariff / capacity) * weight * coef
    return jsonify({"Стоимость": f"{round(cost)} тг"})

import os

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))


