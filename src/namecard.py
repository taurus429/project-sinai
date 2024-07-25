import sys

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea, QApplication
from PyQt5.QtGui import QPainter, QColor, QPen, QFont, QFontMetrics
from PyQt5.QtCore import QRectF, Qt

class TitleWidget(QWidget):
    def __init__(self, title):
        super().__init__()
        self.title = title
        self.setFixedHeight(20)  # 직사각형의 높이 설정
        self.set_width_to_title()

    def set_width_to_title(self):
        font = QFont('Arial', 10)
        metrics = QFontMetrics(font)
        if self.title[2] == 1:
            text = f'{self.title[1]} 사랑장'
        else:
            text = f'{self.title[1]} {self.title[0]}사랑'
        text_width = metrics.horizontalAdvance(text)
        self.setFixedWidth(text_width + 20)  # 텍스트 너비에 여백 추가

    def paintEvent(self, event):
        painter = QPainter(self)
        rect = QRectF(0, 0, self.width(), self.height())

        icon_color = {
            "사랑원": "#fed9b7",
            "사랑장": "#cddafd",
            "목자": "#bee1e6",
        }

        # Draw round rectangle
        painter.setRenderHint(QPainter.Antialiasing)
        if self.title[2] == 1:
            painter.setBrush(QColor(icon_color["사랑장"]))  # 사랑장
        else:
            painter.setBrush(QColor(icon_color["사랑원"]))  # 사랑원
        painter.setPen(QPen(Qt.NoPen))
        painter.drawRoundedRect(rect, 10, 10)  # 원형 모서리 직사각형 그리기

        # Draw title text
        painter.setPen(QColor(0, 0, 0))  # 텍스트 색상 설정
        painter.setFont(QFont('Arial', 10))
        if self.title[2] == 1:
            text = f'{self.title[1]} 사랑장'
        else:
            text = f'{self.title[1]} {self.title[0]}사랑'
        painter.drawText(rect, Qt.AlignCenter, text)

class BusinessCardWidget(QWidget):
    def __init__(self, name, titles, phone, email):
        super().__init__()

        # Set up the main layout
        main_layout = QVBoxLayout()

        # Horizontal layout for name and titles
        name_title_layout = QHBoxLayout()

        # Name label
        name_label = QLabel(name)
        name_label.setFont(QFont('Arial', 16, QFont.Bold))
        name_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        name_title_layout.addWidget(name_label)

        # Scroll area for titles
        titles_scroll_area = QScrollArea()
        titles_scroll_area.setWidgetResizable(True)
        titles_scroll_area.setFixedHeight(47)  # 스크롤 영역 높이 설정
        titles_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 세로 스크롤바 비활성화

        # 스크롤바 스타일 설정 및 외부 테두리 제거
        titles_scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
            }
            QScrollBar:horizontal {
                height: 8px;
                background: #f0f0f0;
                margin: 0px 0px 0px 0px;
            }
            QScrollBar::handle:horizontal {
                background: #888;
                min-width: 10px;
                min-height: 1px; 
                border-radius: 4px;
            }
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                width: 0px;
                background: none;
            }
        """)

        titles_widget = QWidget()
        titles_layout = QHBoxLayout(titles_widget)
        titles_layout.setAlignment(Qt.AlignRight)  # 우측 정렬
        titles_widget.setLayout(titles_layout)
        titles_scroll_area.setWidget(titles_widget)

        titles = titles[1:]
        titles = sorted(titles, key=lambda x: x[1], reverse=True)
        for title in titles:
            title_widget = TitleWidget(title)
            titles_layout.addWidget(title_widget)

        name_title_layout.addWidget(titles_scroll_area)

        # Add the name and titles layout to the main layout
        main_layout.addLayout(name_title_layout)

        # Phone label
        phone_label = QLabel(phone)
        phone_label.setAlignment(Qt.AlignLeft)
        main_layout.addWidget(phone_label)

        # Email label
        email_label = QLabel(email)
        email_label.setAlignment(Qt.AlignLeft)
        main_layout.addWidget(email_label)

        # Set the layout for the widget
        self.setLayout(main_layout)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Set up the main window layout
        main_layout = QVBoxLayout()

        # Create business card widgets
        card1 = BusinessCardWidget("John Doe", ["Software Engineer", "Team Lead"], "+1-234-567-890",
                                   "john.doe@example.com")
        card2 = BusinessCardWidget("Jane Smith", ["Product Manager", "Scrum Master", "UX Designer", "HR", "Receiption"], "+1-987-654-321",
                                   "jane.smith@example.com")

        # Add the business cards to the main layout
        main_layout.addWidget(card1)
        main_layout.addWidget(card2)

        # Set the layout for the main window
        self.setLayout(main_layout)

        # Set the window title
        self.setWindowTitle("Business Cards")

        # Set the window size
        self.resize(400, 300)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
