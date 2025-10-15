from flask import Flask
from flask_migrate import Migrate
from models import db

app = Flask(__name__)

app.config.from_object('config.Config')

db.init_app(app)

migrate = Migrate(app,db)

with app.app_context():
    db.create_all()  # ここでSQLiteファイルとテーブルが作成される

from views import *
from filter import *

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000) # type: ignore