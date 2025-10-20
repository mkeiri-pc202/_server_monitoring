from flask import request, jsonify, render_template, make_response
from app import app
from models import Server_Status, db
from datetime import datetime
from zoneinfo import ZoneInfo
import matplotlib.pyplot as plt
from io import BytesIO
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas


# --------------------------
# ✅ API：ステータス登録・取得
# --------------------------
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
        is_visible = 1
        timestamp = datetime.now(ZoneInfo('Asia/Tokyo'))

        monitor_data = Server_Status(
            server_name=server_id,
            cpu=cpu,
            memory=memory,
            disk_free_gb=disk_free_gb,
            is_visible=is_visible,
            timestamp=timestamp
        )
        db.session.add(monitor_data)
        db.session.commit()

        return jsonify({'message': 'Status updated'}), 200

    else:  # GET
        server = request.args.get('server')
        date_str = request.args.get('date')

        query = Server_Status.query
        if server:
            query = query.filter(Server_Status.server_name == server)
        if date_str:
            try:
                date = datetime.strptime(date_str, '%Y-%m-%d').date()
                query = query.filter(db.func.date(Server_Status.timestamp) == date)
            except ValueError:
                return jsonify({'error': 'Invalid date format'}), 400

        data = query.order_by(Server_Status.timestamp.desc()).limit(100).all()
        result = [
            {
                'server_name': d.server_name,
                'cpu': d.cpu,
                'memory': d.memory,
                'disk_free_gb': d.disk_free_gb,
                'timestamp': d.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            }
            for d in data
        ]
        return jsonify({'data': result})


# --------------------------
# ✅ メインページ
# --------------------------
@app.route('/')
def index():
    monitor_data = Server_Status.query.order_by(Server_Status.timestamp.desc()).limit(50).all()
    server_list = [row.server_name for row in db.session.query(Server_Status.server_name).distinct()]
    number_of_items = [25,50,100]
    return render_template('index.html', data=monitor_data, server_list=server_list,number_of_items=number_of_items)


# --------------------------
# ✅ グラフ出力 (PNG)
# --------------------------
@app.route('/plot.png')
def plot_png():
    server = request.args.get('server')
    date_str = request.args.get('date')
    limit = request.args.get('numberOfItemsSelect')

    query = Server_Status.query
    if server:
        query = query.filter(Server_Status.server_name == server)
    if date_str:
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
            query = query.filter(db.func.date(Server_Status.timestamp) == date)
        except ValueError:
            pass  # 日付が不正なら無視

    data = query.order_by(Server_Status.timestamp.asc()).limit(limit).all()

    if not data:
        # データがない場合はメッセージ付きの空グラフを返す
        fig, ax = plt.subplots(figsize=(6, 3))
        ax.text(0.5, 0.5, 'No Data Found', ha='center', va='center', fontsize=14)
        plt.tight_layout()
    else:
        timestamps = [d.timestamp.strftime('%H:%M:%S') for d in data]
        cpu_values = [d.cpu for d in data]
        memory_values = [d.memory for d in data]
        disk_free_gb = [d.disk_free_gb for d in data]

        fig, ax = plt.subplots(1,2,figsize=(8, 4))
        ax[0].plot(timestamps, cpu_values, label='CPU %')
        ax[0].plot(timestamps, memory_values, label='Memory %')
        ax[0].set_xlabel('Time')
        ax[0].set_ylabel('Usage (%)')
        ax[0].legend()
        
        ax[1].plot(timestamps, disk_free_gb, label='Disc Free Space(GB)')
        ax[1].set_xlabel('Time')
        ax[1].set_ylabel('Disc Free Space(GB)')
        ax[1].legend()
        
        plt.xticks(rotation=45)
        plt.tight_layout()

    output = BytesIO()
    FigureCanvas(fig).print_png(output)
    plt.close(fig)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response
