from flask import Flask, request, render_template_string

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = ""
    if request.method == 'POST':
        # 입력값 받기
        gender = request.form.get('gender')
        weight = float(request.form.get('weight'))
        hours = float(request.form.get('hours'))
        
        # 각 주류별 섭취량 (입력하지 않으면 0으로 처리)
        soju_count = int(request.form.get('soju', 0))
        beer_count = int(request.form.get('beer', 0))
        wine_count = int(request.form.get('wine', 0))
        makgeolli_count = int(request.form.get('makgeolli', 0))
        whiskey_count = int(request.form.get('whiskey', 0))
        
        # 주류별 단위당 알콜 함량 (그램)
        alcohol_grams = {
            'soju': 56.8,     # 360 mL, 20% ABV
            'beer': 17.75,    # 500 mL, 4.5% ABV
            'wine': 14.2,     # 150 mL, 12% ABV
            'makgeolli': 14.2,  # 300 mL, 6% ABV
            'whiskey': 9.5    # 30 mL, 40% ABV
        }
        
        # 총 섭취 알콜(그램) 계산
        total_alcohol = (
            soju_count * alcohol_grams['soju'] +
            beer_count * alcohol_grams['beer'] +
            wine_count * alcohol_grams['wine'] +
            makgeolli_count * alcohol_grams['makgeolli'] +
            whiskey_count * alcohol_grams['whiskey']
        )
        
        # 성별에 따른 알콜 분포율
        if gender == 'male':
            r = 0.68
        else:
            r = 0.55
        
        # Widmark 공식에 따른 혈중 알콜 농도 계산
        bac = (total_alcohol / (weight * 1000 * r)) * 100 - 0.015 * hours
        bac = max(bac, 0)  # 음수가 될 경우 0으로 조정
        
        # 결과 메시지 (한국의 음주운전 기준: 0.03% 이상이면 처벌)
        if bac >= 0.03:
            result = f"혈중 알콜 농도: {bac:.3f}% - 지금 운전하시면 징역 1년!"
        else:
            result = f"혈중 알콜 농도: {bac:.3f}% - 운전해도 괜찮습니다."
    
    # 간단한 HTML 폼 (render_template_string을 사용하여 바로 렌더링)
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
            <label for="soju">소주 (병 수):</label>
            <input type="number" name="soju" id="soju" value="0">
            <br><br>
            
            <label for="beer">맥주 (캔 수):</label>
            <input type="number" name="beer" id="beer" value="0">
            <br><br>
            
            <label for="wine">와인 (잔 수):</label>
            <input type="number" name="wine" id="wine" value="0">
            <br><br>
            
            <label for="makgeolli">막걸리 (잔 수):</label>
            <input type="number" name="makgeolli" id="makgeolli" value="0">
            <br><br>
            
            <label for="whiskey">양주 (샷 수):</label>
            <input type="number" name="whiskey" id="whiskey" value="0">
            <br><br>
            
            <input type="submit" value="측정하기">
        </form>
        <h2>{{ result }}</h2>
    </body>
    </html>
    '''
    return render_template_string(html, result=result)

if __name__ == '__main__':
    app.run(debug=True)
