from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import pytz

app = Flask(__name__)
CORS(app)

# Для збереження подій в пам'яті (або замініть на базу даних)
event_logs = []

# Функція для отримання серверного часу
def get_server_time():
    utc_now = datetime.utcnow()
    local_time = utc_now.astimezone(pytz.timezone("Europe/Kyiv"))
    return local_time.strftime("%Y-%m-%d %H:%M:%S")

# Маршрут для негайного відправлення aодій
@app.route('/log_event', methods=['POST'])
def log_event():
    data = request.json
    server_time = get_server_time()

    if 'description' not in data or 'timestamp' not in data:
        return jsonify({"error": "Invalid data format"}), 400

    event_logs.append({
        "description": data['description'],
        "local_time": data['timestamp'],
        "server_time": server_time,
        "event_number": len(event_logs) + 1
    })

    return jsonify({"message": "Event logged successfully", "server_time": server_time}), 200

# Маршрут для акумульованих даних
@app.route('/log_batch', methods=['POST'])
def log_batch():
    data = request.json

    if not isinstance(data, list):
        return jsonify({"error": "Invalid data format"}), 400

    for event in data:
        if 'description' not in event or 'timestamp' not in event:
            continue  # Пропускаємо некоректні події

        server_time = get_server_time()
        event_logs.append({
            "description": event['description'],
            "local_time": event['timestamp'],
            "server_time": server_time,
            "event_number": len(event_logs) + 1
        })

    return jsonify({"message": f"{len(data)} events logged successfully"}), 200

# Маршрут для перегляду подій
@app.route('/get_events', methods=['GET'])
def get_events():
    return jsonify(event_logs), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
