import pandas as pd

# 엑셀 파일 경로
file_path = '../data/temp2.xlsx'  # 로컬 파일 경로로 수정하세요

# 엑셀 파일 읽기
df = pd.read_excel(file_path)

# 필요하지 않은 행 제거 및 인덱스 재설정
df_cleaned = df.dropna(how='all').reset_index(drop=True)

# 데이터 프레임의 실제 컬럼 수 확인
num_columns = len(df_cleaned.columns)
print(f"Columns in dataframe: {num_columns}")

# 4의 배수인 경우 오른쪽에 빈 컬럼 추가
if (num_columns) % 4 == 0:
    df_cleaned['Empty'] = None
    num_columns += 1
print(df_cleaned)
# 기본 컬럼 이름 패턴
base_columns = ['Name', 'Birthday', 'Phone', 'Gender']

# 컬럼 이름 생성
columns = ['Index']
for i in range(1, (num_columns - 1) // 4 + 1):
    columns += [f'{col}{i}' for col in base_columns]
print(columns)
# 컬럼 이름 재설정
df_cleaned.columns = columns

# 인적 정보 추출
persons = []
for _, row in df_cleaned.iterrows():
    print(row)
    for i in range(1, (num_columns - 1) // 4 + 1):
        name = row[f'Name{i}']
        birthday = row[f'Birthday{i}']
        phone = row[f'Phone{i}']
        gender = row[f'Gender{i}']
        if pd.notna(name) and pd.notna(birthday) and pd.notna(phone):
            persons.append({'Name': name, 'Birthday': birthday, 'Phone': phone, 'Gender': gender})
print(persons)
# 인적 정보 데이터프레임 생성
person_info_df = pd.DataFrame(persons)

# 엑셀 파일로 저장
output_file_path = '인적정보_출석부_처리됨.xlsx'  # 로컬 파일 경로로 수정하세요
person_info_df.to_excel(output_file_path, index=False)

print(f"엑셀 파일이 성공적으로 저장되었습니다: {output_file_path}")