from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# 기본 데이터 
schedules = [
    {"title": "물리 보고서 마감", "date": "2026-06-22", "category": "study"},
    {"title": "방송부 가이드라인 제작", "date": "2026-06-25", "category": "club"}
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/schedules', methods=['GET'])
def get_schedules():
    #[핵심] 화면이 켜지거나 새로고침될 때 무조건 날짜(date) 순서대로 정렬해서 보내기
    sorted_schedules = sorted(schedules, key=lambda x: x['date'])
    return jsonify(sorted_schedules)

@app.route('/api/schedules', methods=['POST'])
def add_schedule():
    data = request.json
    if not data:
        return jsonify({"success": False, "message": "데이터가 없습니다."}), 400
        
    user_text = data.get('title') or data.get('text') or data.get('content') or list(data.values())[0]
    
    if not user_text:
        return jsonify({"success": False, "message": "내용이 없습니다."}), 400
        
    try:
        #[수정] maxsplit=1 을 넣어서 맨 처음 나오는 '월'에서 딱 한 번만 쪼개도록 수정
        parts = user_text.split("월", 1)
        month = parts[0].strip()

        #맨 처음 나오는 '일'에서 한 번만 쪼개서 뒤에 제목은 보존
        remaining = parts[1].split("일", 1)
        day = remaining[0].strip()   
        real_title = remaining[1].strip()

        # 파이썬이 인식할 수 있는 '2026-07-22' 형태로 변환
        formatted_date = f"2026-{month.zfill(2)}-{day.zfill(2)}"
    except Exception as e:
        # 혹시 쪼개기 실패하면(예: '월'이나 '일'이 없는 문장 입력 시) 기본값 처리
        formatted_date = "2026-07-08"
        real_title = user_text

    new_schedule = {
        "title": real_title,
        "date": formatted_date,
        "category": "study"  # 기본값은 학업으로 세팅
    }
    
    schedules.append(new_schedule)
    
    # [핵심] 새 일정을 추가한 직후에도 날짜순으로 줄 세운 뒤 화면에 돌려주기
    sorted_schedules = sorted(schedules, key=lambda x: x['date'])
    return jsonify({"success": True, "schedules": sorted_schedules})

if __name__ == '__main__':
    app.run(debug=True, port=5000)