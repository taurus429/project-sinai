import pandas as pd
import datetime

def get_all_mon_thu(start_date, end_date):
    current_date = start_date
    mon_thu = []
    while current_date <= end_date:
        if current_date.weekday() in [0, 3]:  # 0은 월요일, 3은 목요일
            mon_thu.append(current_date.strftime('%Y-%m-%d 22:00:00'))
        current_date += datetime.timedelta(days=1)
    return mon_thu

# 시작 날짜와 오늘 날짜 설정
start_date = datetime.date(2024, 4, 1)
end_date = datetime.date.today()

# 모든 월요일과 목요일 날짜 가져오기
mon_thu = get_all_mon_thu(start_date, end_date)

# 데이터프레임 생성
df = pd.DataFrame([mon_thu])

# 엑셀 파일에 데이터프레임 저장
excel_file_path = 'mon_thu_22_00.xlsx'
df.to_excel(excel_file_path, index=False, header=False)

print(f"All Mondays and Thursdays from {start_date} to {end_date} have been written to {excel_file_path}")
