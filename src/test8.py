import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QStackedWidget, QProgressBar
from PyQt5.QtCore import Qt, QTimer


class LoadingScreen(QWidget):
    """로딩 화면 (메인 윈도우가 로드되기 전 표시)"""

    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: black; color: white; font-size: 20px;")

        layout = QVBoxLayout()

        self.label = QLabel("Loading... Please wait")
        self.label.setAlignment(Qt.AlignCenter)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setStyleSheet(
            "QProgressBar { border: 2px solid white; border-radius: 5px; background: grey; } QProgressBar::chunk { background: green; width: 10px; }")

        layout.addWidget(self.label)
        layout.addWidget(self.progress_bar)

        self.setLayout(layout)

    def update_progress(self, value):
        """프로그램 진행 상태 업데이트"""
        self.progress_bar.setValue(value)


class MainWindow(QMainWindow):
    """메인 윈도우 (실제 프로그램 화면)"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Program")
        self.setGeometry(100, 100, 800, 600)
        label = QLabel("Main Program Loaded", self)
        label.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(label)


class AppController(QMainWindow):
    """로딩 화면과 메인 화면을 전환하는 컨트롤러"""

    def __init__(self):
        super().__init__()

        # QStackedWidget을 사용하여 로딩 화면과 메인 윈도우를 관리
        self.stack = QStackedWidget(self)

        # 로딩 화면과 메인 윈도우를 추가
        self.loading_screen = LoadingScreen()
        self.main_window = MainWindow()
        self.stack.addWidget(self.loading_screen)  # 0번 인덱스: 로딩 화면
        self.stack.addWidget(self.main_window)  # 1번 인덱스: 메인 윈도우

        self.setCentralWidget(self.stack)

        # 먼저 로딩 화면을 보여줌
        self.stack.setCurrentIndex(0)

        # 프로그래스 바를 증가시키는 타이머 설정
        self.progress = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(30)  # 30ms마다 실행하여 부드럽게 진행

    def update_progress(self):
        """로딩 진행 상태 업데이트"""
        self.progress += 1
        self.loading_screen.update_progress(self.progress)
        if self.progress >= 100:
            self.timer.stop()
            self.show_main_window()

    def show_main_window(self):
        """로딩이 끝나면 메인 윈도우로 전환"""
        self.stack.setCurrentIndex(1)  # 메인 화면으로 전환


def run_application():
    app = QApplication(sys.argv)
    controller = AppController()
    controller.show()  # 윈도우 프레임을 먼저 표시
    sys.exit(app.exec_())


if __name__ == "__main__":
    run_application()
