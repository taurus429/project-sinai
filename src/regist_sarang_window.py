import sys, os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QFileDialog
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap

import src.util

class SarangRegist(QWidget):
    update_signal = pyqtSignal()
    def __init__(self):
        super().__init__()

        # 윈도우 설정
        self.setWindowTitle("파일 디렉터리 선택 및 이미지 삽입")
        self.setGeometry(300, 200, 600, 400)

        # 이미지 표시할 QLabel 위젯
        self.image_label = QLabel(self)
        pixmap = QPixmap()  # 빈 이미지로 초기화
        self.image_label.setPixmap(pixmap)
        self.image_label.setAlignment(Qt.AlignCenter)

        # 디렉터리 선택 버튼 3개 생성
        self.table_sarang_button = QPushButton("테이블사랑", self)
        self.new_family_button = QPushButton("새가족", self)
        self.long_absent_button = QPushButton("장결자", self)

        # 버튼 클릭 이벤트 연결
        self.table_sarang_button.clicked.connect(lambda: self.open_directory_dialog("테이블사랑"))
        self.new_family_button.clicked.connect(lambda: self.open_directory_dialog("새가족"))
        self.long_absent_button.clicked.connect(lambda: self.open_directory_dialog("장결자"))

        # 가로 레이아웃에 버튼 추가
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.table_sarang_button)
        button_layout.addWidget(self.new_family_button)
        button_layout.addWidget(self.long_absent_button)

        # 전체 레이아웃 설정
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addLayout(button_layout)  # 버튼들을 가로로 배치
        self.setLayout(layout)

    def open_directory_dialog(self, category):
        """ 디렉터리 선택하는 다이얼로그 열기 """
        directory = QFileDialog.getExistingDirectory(self, f"{category} 디렉터리 선택")
        if directory:
            file_list = []
            for dirpath, dirnames, filenames in os.walk(directory):
                for filename in filenames:
                    # 엑셀 파일 확장자 확인 및 임시파일 제외
                    if (filename.lower().endswith(('.xlsx', '.xls')) and
                            not filename.lower().startswith('~$')):
                        full_filename = os.path.join(dirpath, filename)
                        file_list.append(full_filename)

            # Util 객체를 사용하여 출석 파일 저장
            u = src.util.Util()

            if category == "테이블사랑":
                u.출석파일저장(file_list)
            elif category == "새가족":
                u.새가족파일저장(file_list)
            elif category == "장결자":
                u.장결자파일저장(file_list)
            u.업데이트_사랑장_리더여부()
            self.update_done()

    def update_done(self):
        # ... update_done 기능 ...
        print("Update done is called.")

        # 필요한 작업 수행 후 신호 방출
        self.update_signal.emit()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SarangRegist()
    window.show()
    sys.exit(app.exec_())
