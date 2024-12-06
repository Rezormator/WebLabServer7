from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Налаштування бази даних SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///events.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Модель для збереження подій
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    server_time = db.Column(db.String(50), nullable=False)

# Ініціалізація бази даних
with app.app_context():
    db.create_all()

# Функція для отримання часу сервера
def get_server_time():
    return datetime.now(pytz.utc).strftime('%Y-%m-%d %H:%M:%S')

@app.route('/log_event', methods=['POST'])
def log_event():
    try:
        data = request.json
        new_event = Event(
            timestamp=data['timestamp'],
            description=data['description'],
            server_time=get_server_time()
        )
        db.session.add(new_event)
        db.session.commit()
        return jsonify({"status": "success", "message": "Event logged"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route('/log_batch', methods=['POST'])
def log_batch():
    try:
        batch = request.json
        for data in batch:
            new_event = Event(
                timestamp=data['timestamp'],
                description=data['description'],
                server_time=get_server_time()
            )
            db.session.add(new_event)
        db.session.commit()
        return jsonify({"status": "success", "message": "Batch events logged"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route('/get_events', methods=['GET'])
def get_events():
    events = Event.query.all()
    return jsonify([
        {
            "id": event.id,
            "timestamp": event.timestamp,
            "description": event.description,
            "server_time": event.server_time
        } for event in events
    ]), 200

if __name__ == '__main__':
    app.run(debug=True)
