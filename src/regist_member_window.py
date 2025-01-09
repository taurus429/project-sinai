import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class MemberRegistration(QWidget):
    def __init__(self):
        super().__init__()

        # 이미지 파일 목록 (사용할 이미지 경로 추가)
        self.image_file = "../asset/img/desc/마을원입력.png"

        # 이미지 표시 QLabel
        self.image_label = QLabel(self)
        pixmap = QPixmap(self.image_file)
        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(True)
        self.image_label.setAlignment(Qt.AlignCenter)

        # 등록 버튼
        self.register_button = QPushButton("엑셀 파일 등록", self)
        self.register_button.clicked.connect(self.open_file_dialog)

        # 레이아웃 설정
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(self.register_button)
        self.setLayout(layout)

        # 윈도우 설정
        self.setWindowTitle("마을원 등록")
        self.setGeometry(300, 200, 600, 400)

    def open_file_dialog(self):
        """ 엑셀 파일을 선택하고 기존 데이터 처리 기능 실행 """
        file_path, _ = QFileDialog.getOpenFileName(self, "엑셀 파일 선택", "", "Excel Files (*.xlsx *.xls)")
        if file_path:
            self.process_excel(file_path)

    def process_excel(self, file_path):
        try:
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
            output_file_path = '인적정보_출석부_처리됨.xlsx'  # 로컬 파일 경로로 수정하세요
            person_info_df.to_excel(output_file_path, index=False, header=False)

            print(f"엑셀 파일이 성공적으로 저장되었습니다: {output_file_path}")

            # 성공 메시지 창 표시
            app = QApplication(sys.argv)
            QMessageBox.information(None, "완료", "엑셀 파일이 성공적으로 저장되었습니다.")

        except Exception as e:
            print(f"오류 발생: {e}")

            # 오류 메시지 창 표시
            app = QApplication(sys.argv)
            QMessageBox.critical(None, "오류", f"파일 처리 중 오류가 발생했습니다: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MemberRegistration()
    window.show()
    sys.exit(app.exec_())