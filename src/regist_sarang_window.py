import sys, os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QFileDialog, \
    QTextEdit, QComboBox
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap

import src.util

from PyQt5.QtWidgets import QProgressBar

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

        self.category_dropdown = QComboBox(self)
        self.category_dropdown.addItems(["테이블사랑", "새가족", "장결자"])

        self.select_button = QPushButton("파일 선택", self)
        self.select_button.clicked.connect(self.open_directory_dialog)

        # 진행 상황을 표시할 프로그래스바 추가
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setGeometry(100, 300, 400, 30)
        self.progress_bar.setRange(0, 100)  # 0%에서 100%까지

        # 로그 출력용 QTextEdit
        self.log_output = QTextEdit(self)
        self.log_output.setReadOnly(True)  # 읽기 전용
        self.log_output.setLineWrapMode(QTextEdit.NoWrap)  # 줄바꿈 비활성화 (옵션)

        # 가로 레이아웃에 버튼 추가
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.category_dropdown)
        button_layout.addWidget(self.select_button)
        # 전체 레이아웃 설정
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addLayout(button_layout)  # 버튼들을 가로로 배치
        layout.addWidget(self.log_output)
        layout.addWidget(self.progress_bar)  # 프로그래스바 추가
        self.setLayout(layout)

    def open_directory_dialog(self):
        """ 디렉터리 선택하는 다이얼로그 열기 """
        category = self.category_dropdown.currentText()
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
                u.출석파일저장(file_list, self.update_progress, self.update_log)
            elif category == "새가족":
                u.새가족파일저장(file_list)
            elif category == "장결자":
                u.장결자파일저장(file_list)
            u.업데이트_사랑장_리더여부()
            self.update_done()

    def update_progress(self, progress):
        """ 진행 상태 업데이트 """
        self.progress_bar.setValue(progress)

    def update_log(self, log, status):
        if status == "error":
            self.log_output.append(f'<span style="color:red;">{log}</span>')  # 빨간색
        else:
            self.log_output.append(log)

    def update_done(self):
        # ... update_done 기능 ...
        print("Update done is called.")
        self.update_signal.emit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SarangRegist()
    window.show()
    sys.exit(app.exec_())
