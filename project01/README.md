## 1주차 예제 : 나만의 일기장
### 적용 기술
- `Flask 프레임워크`를 활용하여 웹사이트를 만든다.
- 일기를 작성하여 `MongoDB`에 `저장`한다.
- 저장한 일기를 DB로부터 불러오고 `목록을 출력`한다.
- 비동기식 `Ajax`를 이용하여 `HTTP request`를 전송한다.

<img src="https://user-images.githubusercontent.com/75527311/137595035-40ab9dad-6baf-4a83-a02b-92287d489f8c.PNG"/>

### 주요 코드

#### 일기 등록하기 (Ajax)
```javascript
// index.html
function posting() {
    let title = $('#title').val()
    let content = $("#content").val()

    let file = $('#file')[0].files[0] //업로드한 이미지 파일
    let form_data = new FormData() //file과 같이 보내기 위해 FormData() 이용

    form_data.append("file_give", file)
    form_data.append("title_give", title)
    form_data.append("content_give", content)

    //비동기식 Ajax를 이용하여 HTTP request 전송
    $.ajax({
        type: "POST",
        url: "/diary",
        data: form_data,
        cache: false,
        contentType: false,
        processData: false,
        success: function (response) {  //일기 등록 완료
            alert(response["msg"])  //완료 메세지
            window.location.reload()    //새로고침
        }
    });
}
```

```python
# app.py
@app.route('/diary', methods=['POST'])
def save_diary():
    title_receive = request.form['title_give'] # ajax의 data로 넘긴 데이터 받아오기
    content_receive = request.form['content_give']

    file = request.files["file_give"] # 이미지 파일 받아오기
    extension = file.filename.split('.')[-1]  # 파일 확장자

    # 파이썬의 datetime을 이용하여 고유한 파일 이름 지정하기
    today = datetime.now()  # 현재 날짜 시각
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')  # 원하는 형태로 변환하기
    today_date = today.strftime('%Y.%m.%d')  # 등록 날짜
    filename = f'file-{mytime}'

    save_to = f'static/{filename}.{extension}'
    file.save(save_to)  # 해당 경로로 파일 저장하기

    doc = {
        'title': title_receive,
        'content': content_receive,
        'file': f'{filename}.{extension}',
        'date': today_date
    }

    db.diary.insert_one(doc)  # MongoDB에 저장

    return jsonify({'msg': '저장 완료'})  # 성공 메세지
```

#### 일기 조회하기
```python
# app.py
@app.route('/diary', methods=['GET'])
def show_diary():
    diaries = list(db.diary.find({}, {'_id': False}))  # MongoDB의 diary 안에 있는 모든 값 조회
    return jsonify({'all_diary': diaries})  # json 형식으로 리턴
```
```javascript
// index.html
function listing() {
    //비동기식 Ajax를 이용하여 HTTP request 전송
    $.ajax({
        type: "GET",
        url: "/diary",
        data: {},
        success: function (response) {
            let diaries = response['all_diary'];    // 받아온 json 파일 중 all_diary
            for (let i = 0; i < diaries.length; i++) {
                let title = diaries[i]['title'];
                let content = diaries[i]['content'];
                let date = diaries[i]['date'];
                let file = diaries[i]['file'];

                let temp_html = `<div class="card">
                                    <img src="../static/${file}" class="card-img-top">
                                    <div class="card-body">
                                        <h5 class="card-title">${title}</h5>
                                        <p class="card-text">${content}</p>
                                        <p class="save-date">${date}</p>
                                    </div>
                                </div>`;
                $('#cards-box').append(temp_html);  // append해서 목록 출력하기
            }
        }
    })
}
```
