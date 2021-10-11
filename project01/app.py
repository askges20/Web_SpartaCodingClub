from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

from pymongo import MongoClient

# MongoDB 연결하기
client = MongoClient('localhost', 27017)
db = client.dbsparta_plus_week1

from datetime import datetime


# 기본 페이지 index.html
@app.route('/')
def home():
    return render_template('index.html')


# GET 요청 API 코드
@app.route('/diary', methods=['GET'])
def show_diary():
    diaries = list(db.diary.find({}, {'_id': False}))  # MongoDB의 diary 안에 있는 모든 값
    return jsonify({'all_diary': diaries})  # json 형식으로 리턴


# POST 요청 API 코드
@app.route('/diary', methods=['POST'])
def save_diary():
    title_receive = request.form['title_give']
    content_receive = request.form['content_give']

    file = request.files["file_give"]
    extension = file.filename.split('.')[-1] # 파일 확장자

    today = datetime.now() # 현재 날짜 시각
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')  # 원하는 형태로 변환하기
    filename = f'file-{mytime}'

    save_to = f'static/{filename}.{extension}'
    file.save(save_to)  # 해당 경로로 파일 저장

    doc = {
        'title': title_receive,
        'content': content_receive,
        'file': f'{filename}.{extension}'
    }

    db.diary.insert_one(doc)  # MongoDB에 저장

    return jsonify({'msg': '저장 완료'})  # 성공 메세지


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)  # localhost:5000
