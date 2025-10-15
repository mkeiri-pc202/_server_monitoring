from flask import request, jsonify, render_template,make_response
from app import app
from models import Server_Status,db
from datetime import datetime
from zoneinfo import ZoneInfo
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

@app.route('/api/status', methods=['GET', 'POST'])
def status():
    if request.method == 'POST':
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

    else:  # GET
        return jsonify({'message': 'GET method was Received'})

@app.route('/')
def index():
    monitor_data = Server_Status.query.order_by(Server_Status.timestamp.desc()).limit(50).all()   
    return render_template('index.html', data=monitor_data)

@app.route('/plot.png')
def plot_png():
    data = Server_Status.query.order_by(Server_Status.timestamp.desc()).limit(50).all()

    # データを時系列順に並べ替え
    data = list(reversed(data))
    timestamps = [d.timestamp.strftime('%H:%M:%S') for d in data]
    cpu_values = [d.cpu for d in data]
    memory_values = [d.memory for d in data]

    # グラフ作成
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.plot(timestamps, cpu_values, label='CPU %')
    ax.plot(timestamps, memory_values, label='Memory %')
    ax.set_xlabel('Time')
    ax.set_ylabel('Usage (%)')
    ax.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()

    # PNGとして返す
    output = BytesIO()
    FigureCanvas(fig).print_png(output)
    plt.close(fig)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response