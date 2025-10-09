from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Server_Status(db.Model):
    __tablename__ = 'server_status'

    id = db.Column(db.Integer, primary_key=True,autoincrement=True) #　連番で数字をふってるだけ
    server_name = db.Column(db.String(80), nullable=False) #　PC名
    cpu = db.Column(db.Float, nullable=False)#　CPUの利用率
    memory = db.Column(db.Float, nullable=False)#　メモリの利用率
    disk_free_gb = db.Column(db.Float, nullable=False)#　ディスクの空き
    is_visible = db.Column(db.Boolean, default=True, nullable=False)#　いまのところ使ってない。利用終了したPC名に設定して非表示にする予定。
    timestamp = db.Column(db.DateTime, nullable=False)#　ディスクの空き# データを受け取った日時
