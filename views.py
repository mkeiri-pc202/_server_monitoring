from flask import request, jsonify, render_template
from app import app
from models import Server_Status,db
from datetime import datetime
from zoneinfo import ZoneInfo

@app.route('/api/status', methods=['POST'])
def receive_status():
    data = request.json
    if not data or 'server_id' not in data:
        return jsonify({'error': 'Invalid data'}), 400

    server_id = data['server_id']
    cpu = data['cpu']
    memory = data['memory']
    disk_free_gb = data['disk_free_gb']
    is_visible =  1
    timestamp = datetime.now(ZoneInfo('Asia/Tokyo'))

    monitor_data = Server_Status(server_name = server_id,cpu=cpu,memory=memory,disk_free_gb=disk_free_gb,is_visible=is_visible,timestamp=timestamp)
    db.session.add(monitor_data)
    db.session.commit()
    
    return jsonify({'message': 'Status updated'}), 200

@app.route('/api/status', methods=['GET'])
def get_status():
    return jsonify({'message': 'GET method was Received'})

@app.route('/')
def index():
    monitor_data = Server_Status.query.order_by(Server_Status.timestamp.desc()).limit(50).all()
    return render_template('index.html', data=monitor_data)
