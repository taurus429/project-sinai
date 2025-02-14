import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, pyqtSignal
from src.util import Util

class MemberRegistration(QWidget):
    update_signal = pyqtSignal()
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
            sheets = pd.read_excel(file_path, sheet_name=None)

            base_columns = ['Name', 'Birthday', 'Phone', 'Gender']
            all_persons = []
            # 시트 이름을 오름차순으로 정렬
            sorted_sheet_names = sorted(sheets.keys())

            # 정렬된 시트 이름을 사용하여 순회
            for sheet_name in sorted_sheet_names:
                df = sheets[sheet_name]  # 정렬된 순서대로 데이터 가져오기
                print(f"Processing sheet: {sheet_name}")

                df_cleaned = df.dropna(how='all').reset_index(drop=True)
                num_columns = len(df_cleaned.columns)
                print(f"Columns in dataframe: {num_columns}")

                if num_columns % 4 == 0:
                    df_cleaned['Empty'] = None
                    num_columns += 1

                columns = ['Index']
                for i in range(1, (num_columns - 1) // 4 + 1):
                    columns += [f'{col}{i}' for col in base_columns]

                df_cleaned.columns = columns

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

            person_info_df = pd.DataFrame(all_persons)

            u = Util()
            u.마을원저장(df=person_info_df)
            self.update_done()
            QMessageBox.information(self, "완료", "엑셀 파일이 성공적으로 저장되었습니다.")

        except Exception as e:

            QMessageBox.critical(self, "오류", f"파일 처리 중 오류가 발생했습니다: {e}")

    def update_done(self):
        # ... update_done 기능 ...
        print("Update done is called.")

        # 필요한 작업 수행 후 신호 방출
        self.update_signal.emit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MemberRegistration()
    window.show()
    sys.exit(app.exec_())