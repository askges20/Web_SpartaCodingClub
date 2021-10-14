from flask import Flask, render_template, request
import requests

app = Flask(__name__)


@app.route('/')
def main():
    myname = "Sparta"
    return render_template("index.html", name=myname)


@app.route('/detail/<keyword>')
def detail(keyword):
    r = requests.get(f"https://owlbot.info/api/v4/dictionary/{keyword}", headers={"Authorization": "Token 658679be993d1b24d8a6919d69f04f488a6a5b7c"})
    result = r.json()
    print(result)
    word_receive = request.args.get("word_give")
    print(word_receive)
    return render_template("detail.html", word=keyword)

    # 미세먼지
    # r = requests.get('http://openapi.seoul.go.kr:8088/6d4d776b466c656533356a4b4b5872/json/RealtimeCityAir/1/99')
    # response = r.json()  # 받아온 정보를 json 형식으로
    # rows = response['RealtimeCityAir']['row']

    # return render_template("detail.html", rows=rows, word=keyword)


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
