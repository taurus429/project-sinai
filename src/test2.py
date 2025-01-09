import pandas as pd

# 엑셀 파일 경로
file_path = '../data/2024년 3term 사랑개편.xlsx'  # 로컬 파일 경로로 수정하세요

# 엑셀 파일의 모든 시트 읽기
sheets = pd.read_excel(file_path, sheet_name=None)

# 기본 컬럼 이름 패턴
base_columns = ['Name', 'Birthday', 'Phone', 'Gender']

# 모든 시트의 데이터를 저장할 리스트
all_persons = []

# 각 시트에 대해 데이터 처리
for sheet_name, df in sheets.items():
    print(f"Processing sheet: {sheet_name}")

    # 필요하지 않은 행 제거 및 인덱스 재설정
    df_cleaned = df.dropna(how='all').reset_index(drop=True)

    # 데이터 프레임의 실제 컬럼 수 확인
    num_columns = len(df_cleaned.columns)
    print(f"Columns in dataframe: {num_columns}")

    # 4의 배수인 경우 오른쪽에 빈 컬럼 추가
    if num_columns % 4 == 0:
        df_cleaned['Empty'] = None
        num_columns += 1

    # 컬럼 이름 생성
    columns = ['Index']
    for i in range(1, (num_columns - 1) // 4 + 1):
        columns += [f'{col}{i}' for col in base_columns]

    # 컬럼 이름 재설정
    df_cleaned.columns = columns

    # 인적 정보 추출
    persons = []
    for _, row in df_cleaned.iterrows():
        for i in range(1, (num_columns - 1) // 4 + 1):
            name = row.get(f'Name{i}')
            birthday = row.get(f'Birthday{i}')
            phone = row.get(f'Phone{i}')
            gender = row.get(f'Gender{i}')
            if pd.notna(name) and pd.notna(birthday) and pd.notna(phone):
                persons.append({
                    'Name': name,
                    'Birthday': birthday,
                    'Phone': phone,
                    'Gender': gender
                })

    all_persons.extend(persons)

# 인적 정보 데이터프레임 생성
person_info_df = pd.DataFrame(all_persons)

# 엑셀 파일로 저장 (헤더 없이)
output_file_path = '../data/마을원명단.xlsx'  # 로컬 파일 경로로 수정하세요
person_info_df.to_excel(output_file_path, index=False, header=False)

print(f"엑셀 파일이 성공적으로 저장되었습니다: {output_file_path}")
