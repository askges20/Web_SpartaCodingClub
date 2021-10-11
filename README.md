# 스파르타코딩클럽 웹개발 플러스
스파르타코딩클럽 강의를 수강하며 진행한 실습 예제입니다.

## 🛠 개발 환경 및 도구
- IDE : PyCharm
- Language : Python, Javascript 등
- Framework : Flask
- Database : MongoDB & Robo 3T
- Package : flask, pymongo
- Hosting : AWS EC2

## 💻 실습 예제
### 1) 나만의 일기장
- `Ajax`를 통한 GET/POST 요청으로 `MongoDB`에 일기를 저장하고 불러온다.
- `AWS EC2`로 배포한다.
- [소스 코드](./Project01)

## ✏ 공부 기록
[티스토리 블로그](https://askges20.tistory.com/category/%5B%EC%8A%A4%ED%8C%8C%EB%A5%B4%ED%83%80%EC%BD%94%EB%94%A9%ED%81%B4%EB%9F%BD%5D/%EC%9B%B9%EA%B0%9C%EB%B0%9C%20%ED%94%8C%EB%9F%AC%EC%8A%A4)

<div>　</div>
<div align="center">⚪　⚪　⚪</div>
<div>　</div>

## Flask
- 웹 애플리케이션 개발을 위한 파이썬 프레임워크
### 기본 코드
```python
from flask import Flask, render_template, jsonfiy, request
app = Flask(__name__)

@app.route('/')
def home():
	return render_template('index.html')

if __name__ == '__main__':
	app.run('0.0.0.0', port=5000, debug=True)
```
### 프로젝트 구조
1. `templates` 폴더 : `HTML 파일` 저장
2. `static` 폴더 : CSS, Javascript, image 파일 등 `정적 파일` 저장
3. `app.py` : Flask 메인 파일
