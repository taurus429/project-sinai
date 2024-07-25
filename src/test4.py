import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtCore import Qt, QTimer

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("메인 화면")
        self.setGeometry(100, 100, 600, 400)

        # 상태바에 자막을 출력할 QLabel 생성
        self.subtitle_label = QLabel("여기에서 자막이 오른쪽에서 왼쪽으로 흐릅니다.", self)

        # 상태바 설정
        self.statusBar().addWidget(self.subtitle_label)

        # 자막 이동 타이머 설정
        self.subtitle_pos = self.width()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.move_subtitle)
        self.timer.start(30)

    def move_subtitle(self):
        self.subtitle_pos -= 2  # 자막을 왼쪽으로 이동
        if self.subtitle_pos < -self.subtitle_label.width():
            self.subtitle_pos = self.width()
        self.subtitle_label.move(self.subtitle_pos, 0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
