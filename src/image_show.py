import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class ImageViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Image Viewer")
        self.setGeometry(100, 100, 200, 200)  # 설정할 창의 크기

        # 중앙 위젯과 레이아웃 설정
        central_widget = QWidget()
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # 이미지 라벨 설정
        self.image_label = QLabel(self)

        # QPixmap 로드 및 크기 조정
        pixmap = QPixmap('./trophy.png')
        pixmap = pixmap.scaled(30, 30, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)

        self.image_label.setPixmap(pixmap)
        self.image_label.setToolTip("trophy.png")  # 툴팁 설정
        layout.addWidget(self.image_label)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = ImageViewer()
    viewer.show()
    sys.exit(app.exec_())
