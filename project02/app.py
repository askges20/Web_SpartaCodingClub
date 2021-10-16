from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient
import requests


app = Flask(__name__)

# client = MongoClient('localhost', 27017)
# client = MongoClient('mongodb://id:pw@ip', 27017) # 이런 방법도 있다.
client = MongoClient('52.78.107.146', 27017, username="test", password="test")
db = client.dbsparta_plus_week2


@app.route('/')
def main():
    # DB에서 저장된 단어 찾아서 HTML에 나타내기
    msg = request.args.get("msg")
    words = list(db.words.find({}, {"_id": False}))  # _id에 해당하는 열은 빼고
    return render_template("index.html", words=words, msg=msg)


@app.route('/detail/<keyword>')
def detail(keyword):
    status_receive = request.args.get("status_give")
    # API에서 단어 뜻 찾아서 결과 보내기
    r = requests.get(f"https://owlbot.info/api/v4/dictionary/{keyword}", headers={"Authorization": "Token 658679be993d1b24d8a6919d69f04f488a6a5b7c"})
    if r.status_code != 200:
        return redirect(url_for("main", msg="사전에 존재하지 않는 단어입니다."))
        #  return redirect('/')
    result = r.json()
    print(result)
    return render_template("detail.html", word=keyword, result=result, status=status_receive)


@app.route('/api/save_word', methods=['POST'])
def save_word():
    # 단어 저장하기
    word_receive = request.form["word_give"]
    definition_receive = request.form["definition_give"]
    doc = {"word": word_receive, "definition": definition_receive}
    db.words.insert_one(doc)
    return jsonify({'result': 'success', 'msg': f'단어 {word_receive} 저장'})


@app.route('/api/delete_word', methods=['POST'])
def delete_word():
    # 단어 삭제하기
    word_receive = request.form["word_give"]
    db.words.delete_one({"word": word_receive})  # 단어 삭제
    db.examples.delete_many({"word": word_receive})  # 해당 단어 예문 삭제
    return jsonify({'result': 'success', 'msg': f'단어 {word_receive} 삭제'})


@app.route('/api/get_exs', methods=["GET"])
def get_exs():
    # 예문 가져오기
    word_receive = request.args.get("word_give")
    result = list(db.examples.find({"word": word_receive}, {'_id': 0}))
    return jsonify({'result': 'success', 'examples': result})


@app.route('/api/save_ex', methods=["POST"])
def save_ex():
    # 예문 저장하기
    word_receive = request.form["word_give"]
    example_receive = request.form["example_give"]
    doc = {"word": word_receive, "example": example_receive}
    db.examples.insert_one(doc)
    return jsonify({'result': 'success', 'msg': '예문 저장 완료'})


@app.route('/api/delete_ex', methods=["POST"])
def delete_ex():
    word_receive = request.form['word_give']
    number_receive = int(request.form['number_give'])
    example = list(db.examples.find({'word': word_receive}))[number_receive]['example']
    db.examples.delete_one({'word': word_receive, 'example': example})
    return jsonify({'result': 'success'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)