from flask import Flask, request, render_template_string

app = Flask(__name__)

# 주류별 정보 (이름, 용량, 도수, 단위당 알콜 그램)
alcohol_info = {
    'soju': {
        'name': "소주",
        'volume': "360 mL",
        'abv': "20%",
        'grams': 56.8
    },
    'beer': {
        'name': "맥주",
        'volume': "500 mL",
        'abv': "4.5%",
        'grams': 17.75
    },
    'wine': {
        'name': "와인",
        'volume': "150 mL",
        'abv': "12%",
        'grams': 14.2
    },
    'makgeolli': {
        'name': "막걸리",
        'volume': "300 mL",
        'abv': "6%",
        'grams': 14.2
    },
    'whiskey': {
        'name': "양주",
        'volume': "30 mL",
        'abv': "40%",
        'grams': 9.5
    }
}

@app.route('/', methods=['GET', 'POST'])
def index():
    result = ""
    details = ""
    if request.method == 'POST':
        # 입력값 받기
        gender = request.form.get('gender')
        weight = float(request.form.get('weight'))
        hours = float(request.form.get('hours'))
        
        # 각 주류별 섭취량 입력 (입력하지 않으면 0으로 처리)
        counts = {}
        total_alcohol = 0
        details_list = []
        for key in alcohol_info:
            count = int(request.form.get(key, 0))
            counts[key] = count
            grams = count * alcohol_info[key]['grams']
            total_alcohol += grams
            details_list.append(
                f"{alcohol_info[key]['name']}: {count}회 ({alcohol_info[key]['volume']}, {alcohol_info[key]['abv']}) → {grams:.2f} g"
            )
        
        # 성별에 따른 알콜 분포율 (Widmark 공식)
        r = 0.68 if gender == 'male' else 0.55
        
        # Widmark 공식으로 혈중 알콜 농도(BAC) 계산
        bac = (total_alcohol / (weight * 1000 * r)) * 100 - 0.015 * hours
        bac = max(bac, 0)  # 음수면 0으로 조정

        # 처벌 기준 (예시)
        # BAC < 0.03: 운전해도 괜찮음
        # 0.03 <= BAC < 0.08: 징역 1년
        # 0.08 <= BAC < 0.15: 징역 2년
        # BAC >= 0.15: 벌금 500만원
        if bac < 0.03:
            penalty = "운전해도 괜찮습니다."
        elif bac < 0.08:
            penalty = "징역 1년!"
        elif bac < 0.15:
            penalty = "징역 2년!"
        else:
            penalty = "벌금 500만원!"
        
        # 결과 메시지 구성
        details = "<ul>" + "".join(f"<li>{item}</li>" for item in details_list) + "</ul>"
        result = (
            f"<p>총 알콜 섭취량: {total_alcohol:.2f} g</p>"
            f"<p>혈중 알콜 농도 (BAC): {bac:.3f}%</p>"
            f"<p>처벌 기준:</p>"
            "<ul>"
            "<li>BAC 0.03% 이상: 징역 1년</li>"
            "<li>BAC 0.08% 이상: 징역 2년</li>"
            "<li>BAC 0.15% 이상: 벌금 500만원</li>"
            "</ul>"
            f"<p>최종 결과: {penalty}</p>"
        )
    
    # HTML 폼 및 결과 화면 (각 술의 정보를 입력란 옆에 표시)
    html = '''
    <!doctype html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>음주 측정기</title>
    </head>
    <body>
        <h1>음주 측정기</h1>
        <form method="post">
            <label for="gender">성별:</label>
            <select name="gender" id="gender">
                <option value="male">남성</option>
                <option value="female">여성</option>
            </select>
            <br><br>
            
            <label for="weight">몸무게 (kg):</label>
            <input type="number" name="weight" id="weight" step="0.1" required>
            <br><br>
            
            <label for="hours">음주 후 경과 시간 (시간):</label>
            <input type="number" name="hours" id="hours" step="0.1" required>
            <br><br>
            
            <h3>각 주류별 섭취량</h3>
            {% for key, info in alcohol_info.items() %}
                <label for="{{ key }}">
                    {{ info.name }} ({{ info.volume }}, {{ info.abv }}):
                </label>
                <input type="number" name="{{ key }}" id="{{ key }}" value="0">
                <br><br>
            {% endfor %}
            
            <input type="submit" value="측정하기">
        </form>
        
        <hr>
        <div>
            <h2>입력 내역</h2>
            {{ details | safe }}
            <h2>측정 결과</h2>
            {{ result | safe }}
        </div>
    </body>
    </html>
    '''
    # render_template_string에 alcohol_info도 전달해서 템플릿에서 사용할 수 있게 함
    return render_template_string(html, result=result, details=details, alcohol_info=alcohol_info)

if __name__ == '__main__':
    app.run(debug=True)
