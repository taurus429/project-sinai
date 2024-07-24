import pandas as pd
from datetime import datetime, timedelta

# 시작일과 종료일 설정
start_date = datetime(2023, 10, 1)
end_date = datetime.now()

# 금요일만 포함할 리스트 생성
dates = []
current_date = start_date

while current_date <= end_date:
    if current_date.weekday() == 4:  # 금요일은 4
        formatted_date = current_date.strftime("%Y-%m-%d") + " 20:00:00"
        dates.append([formatted_date])
    current_date += timedelta(days=1)

# DataFrame 생성
df = pd.DataFrame(dates, columns=["Date"])

# 엑셀 파일 저장
file_path = "Fridays_Dates.xlsx"
df.to_excel(file_path, index=False, engine='openpyxl')

print(f"엑셀 파일이 생성되었습니다: {file_path}")