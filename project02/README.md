## 2주차 예제 : 나만의 단어장
### 적용 기술
- `Flask`를 활용하여 멀티페이지 사이트를 만든다.
- `Owlbot Dictionary API` 사전 API를 이용하여 영어 단어 데이터를 받아온다.
- 나만의 단어와 예문을 `MongoDB`에 `저장`하고 불러온다.
- 비동기식 `Ajax`를 이용하여 `HTTP request`를 전송한다.
- Flask의 `Jinja2 템플릿`을 이용한다. 

### 구현 화면
- 나만의 단어장 메인 화면
<img src="https://user-images.githubusercontent.com/75527311/137753305-17f8d6d5-d29a-4aa0-b74c-2db77016ce44.PNG"/>

- 단어 검색 결과 상세 페이지
<img src="https://user-images.githubusercontent.com/75527311/137753467-594acd91-fd9d-43aa-8e51-daffb7202a3b.PNG"/>

- 단어를 나만의 단어장에 추가하기
<img src="https://user-images.githubusercontent.com/75527311/137753609-b0ea1ebf-04d1-42e7-addf-e27c56fadbc0.PNG"/>
<img src="https://user-images.githubusercontent.com/75527311/137753662-6bcfb939-e031-4295-a284-a52e1bff8979.PNG"/>

- 단어의 예문 추가하기
<img src="https://user-images.githubusercontent.com/75527311/137753740-b4941e2a-e0fa-48a9-a386-d69d40708734.PNG"/>
<img src="https://user-images.githubusercontent.com/75527311/137753756-5a5c26c3-f3af-4796-9ca9-6816ed063103.PNG"/>



### 주요 코드
- 단어장에 저장된 단어 목록 불러오기, 메인 화면에 출력하기
```python
# app.py에서 단어 목록 조회
@app.route('/')
def main():
    # DB에서 저장된 단어 찾아서 HTML에 나타내기
    msg = request.args.get("msg")
    words = list(db.words.find({}, {"_id": False}))  # _id에 해당하는 열은 빼고
    return render_template("index.html", words=words, msg=msg)
```

```html
<!-- index.html에서 Jinja2 템플릿을 이용하여 출력 -->
<tbody id="tbody-box">
{% for word in words %}
    <tr id="word-{{ word.word }}">
        <td><a href="/detail/{{ word.word }}?status_give=old">{{ word.word }}</a></td>
        <td>{{ word.definition }}</td>
    </tr>
{% endfor %}
</tbody>
```

- 단어 검색해서 단어장에 있으면 하이라이트, 없으면 상세 페이지로 이동
```javascript
{% if msg %}
    alert("{{ msg }}")
{% endif %}
let words = {{ words|tojson }}; //html이 아니라 json임을 명시
let word_list = [];
for (let i = 0; i < words.length; i++) {
    word_list.push(words[i]["word"])  // 단어장에 저장된 단어 목록
}

function find_word() {
    let word = $("#input-word").val().toLowerCase() // 입력된 영어 단어를 소문자로 변환 후
    if (word == "") { // 아무것도 입력하지 않았으면
        alert("값을 입력해주세요!")
        return
    }
    if (word_list.includes(word)) { // 단어장에 있으면
        $(`#word-${word}`).addClass("highlight")  // addClass로 해당 단어에 하이라이트 효과
        $(`#word-${word}`).siblings().removeClass("highlight")  // siblings와 removeClass로 다른 단어는 하이라이트 효과 해제
        $(`#word-${word}`)[0].scrollIntoView()  // 해당 단어 위치로 스크로
    } else {
        window.location.href = `/detail/${word}?status_give=new`  // 단어장에 없으면 상세페이지로
    }
}
```

- Owlbot에 Ajax 요청으로 단어 데이터 가져오기
```javascript
$.ajax({
    type: "GET",
    url: `https://owlbot.info/api/v4/dictionary/${word}`,
    beforeSend: function (xhr) {
        xhr.setRequestHeader("Authorization", "Token 발급받은토큰");
    },
    data: {},
    error: function (xhr, status, error) {
        alert("에러 발생!");
    },
    success: function (response) {
        console.log(response)
        $('#word').text(response['word'])
        if (response["pronunciation"] == null) {  // 발음 정보가 없는 경우
            $('#pronunciation').text('')  // 빈칸으로
        } else {
            $('#pronunciation').text(`/${response['pronunciation']}/`)
        }
        let definitions = response['definitions']
        $('#definitions').empty() // 기존에 있던 정의 삭제
        for (let i = 0; i <= definitions.length; i++) {
            console.log(definitions[i])
            let definition = definitions[i]
            let html_temp = ''
            if (definition['example'] == null) {  // 예문이 없으면 출력X
                html_temp = `<div style="padding:10px">
                                <i>${definition['type']}</i>
                                <br>${definition['definition']}<br>
                            </div>`
            } else {  // 예문이 있으면 출력 O
                html_temp = `<div style="padding:10px">
                                <i>${definition['type']}</i>
                                <br>${definition['definition']}<br>
                                <span class="example">${definition['example']}</span>
                            </div>`
            }
            $('#definitions').append(html_temp)
        }
    }
})
```
