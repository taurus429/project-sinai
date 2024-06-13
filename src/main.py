import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QTableWidget, QFileDialog, QTableWidgetItem
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRect
from PyQt5.QtGui import QFont, QFontDatabase, QColor

class CounterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.counter = 0
        self.initUI()

    def initUI(self):
        # Layout setup
        self.layout = QVBoxLayout()

        # Label to display the counter
        self.label = QLabel(f"Counter: {self.counter}", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("""
            font-family: 'Arial';
            font-size: 24px;
            font-weight: bold;
            color: #FFFFFF;
        """)
        self.layout.addWidget(self.label)
        self.table_widget = QTableWidget()
        self.layout.addWidget(self.table_widget)

        # Button to increase the counter
        self.button = QPushButton('마을원 등록', self)
        self.button.clicked.connect(self.increase_counter)
        self.button.clicked.connect(self.load_excel_file)
        self.button.setStyleSheet("""
            QPushButton {
                background-color: #1E90FF;
                color: white;
                font-family: 'Arial';
                font-size: 18px;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #63B8FF;
            }
        """)
        self.layout.addWidget(self.button)

        # Set the layout and window properties
        self.setLayout(self.layout)
        self.setWindowTitle('Counter App')
        self.setGeometry(100, 100, 300, 200)
        self.setStyleSheet("background-color: #0D1B2A;")

    def increase_counter(self):
        self.counter += 1
        self.label.setText(f"Counter: {self.counter}")

    def load_excel_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Excel File", "", "Excel Files (*.xlsx *.xls)", options=options)
        print(file_path)
        if file_path:
            df = pd.read_excel(file_path, engine='openpyxl')
            print(df)
            if not df.empty:
                self.display_data(df)

    def display_data(self, df):
        self.table_widget.setRowCount(df.shape[0])
        self.table_widget.setColumnCount(df.shape[1])
        self.table_widget.setHorizontalHeaderLabels(df.columns)

        for i in range(df.shape[0]):
            for j in range(df.shape[1]):
                item = QTableWidgetItem(str(df.iat[i, j]))
                item.setForeground(QColor(255, 255, 255))  # 텍스트 색상을 흰색으로 설정
                self.table_widget.setItem(i, j, item)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = CounterApp()
    ex.show()
    sys.exit(app.exec_())
