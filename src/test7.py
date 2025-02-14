import sys
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QLabel
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt


class StatusBarWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Status Bar Example')

        # Layout for the status bar
        self.layout = QHBoxLayout(self)
        self.setLayout(self.layout)

        # Create the lamp label
        self.lamp_label = QLabel(self)
        self.lamp_label.setFixedSize(20, 20)  # Fixed size for lamp
        self.layout.addWidget(self.lamp_label)

        # Create the status message label
        self.status_label = QLabel('이상 없음', self)
        self.status_label.setAlignment(Qt.AlignLeft)
        self.layout.addWidget(self.status_label)

        self.update_status("normal")  # Set initial status

    def update_status(self, status):
        if status == "normal":
            self.lamp_label.setStyleSheet("background-color: green; border-radius: 10px;")
            self.status_label.setText("이상 없음")
        elif status == "warning":
            self.lamp_label.setStyleSheet("background-color: orange; border-radius: 10px;")
            self.status_label.setText("주의")
        elif status == "danger":
            self.lamp_label.setStyleSheet("background-color: red; border-radius: 10px;")
            self.status_label.setText("문제 발생")
        else:
            self.lamp_label.setStyleSheet("background-color: gray; border-radius: 10px;")
            self.status_label.setText("알 수 없는 상태")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = StatusBarWidget()
    widget.resize(300, 50)  # Resize the widget to fit the status bar
    widget.show()

    # For demonstration purposes, we can update the status after a delay
    from PyQt5.QtCore import QTimer


    def change_status():
        widget.update_status("warning")
        QTimer.singleShot(2000, lambda: widget.update_status("danger"))


    QTimer.singleShot(1000, change_status)

    sys.exit(app.exec_())
