from flask import Flask, request, send_file
from flask_sqlalchemy import SQLAlchemy
import datetime
import os
import json

with open('config.json') as config_file:
    config = json.load(config_file)

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{config['USERNAME']}:{config['PASSWORD']}@{config['HOSTNAME']}:{config['PORT']}/{config['DATABASE']}?charset=utf8mb4"

db = SQLAlchemy(app)


class File(db.Model):
    __tablename__ = "files"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    filename = db.Column(db.String(100), nullable=False)
    datetime = db.Column(db.String(100), nullable=False)


with app.app_context():
    db.create_all()


@app.route('/upload', methods=['POST'])
def upload():
    uploadfile = request.files['upload']
    if uploadfile:
        filename = uploadfile.filename
        if not os.path.exists('files'):
            os.makedirs('files')
        filepath = os.path.join('files', filename)
        uploadfile.save(filepath)
        current_datetime = datetime.datetime.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        file = File(filename=filename, datetime=formatted_datetime)
        db.session.add(file)
        db.session.commit()
        return 'upload success'
    else:
        return 'upload fail'


@app.route('/download/<filename>', methods=['GET'])
def download(filename):
    if not os.path.exists('files'):
        os.makedirs('files')
    file = os.path.join('files', filename)
    if file:
        return send_file(file, as_attachment=True)
    else:
        return 'file not found'


if __name__ == '__main__':
    app.run()
