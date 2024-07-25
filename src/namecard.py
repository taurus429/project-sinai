import os
import sys
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea, QApplication
from PyQt5.QtGui import QPainter, QColor, QPen, QFont, QFontMetrics
from PyQt5.QtCore import QRectF, Qt
import font_util, util, medal, trophy

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
    def __init__(self, 마을원정보):
        super().__init__()
        self.util = util.Util()
        name = 마을원정보["이름"]
        titles = self.util.사랑장조회(마을원정보["uid"])
        phone = 마을원정보["전화번호"]
        birthdate = str(마을원정보["생년월일"])

        # Set up the main layout
        main_layout = QVBoxLayout()

        # Horizontal layout for name and titles
        name_title_layout = QHBoxLayout()

        font_path = "../asset/font/감탄로드바탕체 Bold.ttf"  # Replace with your font file path
        custom_font_family = font_util.load_custom_font(font_path)

        # Name label
        name_label = QLabel(f"{name} ({birthdate[:2]}또래)")
        name_label.setFont(QFont(custom_font_family, 16))
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

        # Create a new horizontal layout for phone and birthdate
        down_layout = QHBoxLayout()

        # Left layout for phone
        phone_layout = QVBoxLayout()
        phone_label = QLabel(phone)
        phone_label.setAlignment(Qt.AlignLeft)
        phone_layout.addWidget(phone_label)
        birthdate_label = QLabel(birthdate)
        birthdate_label.setAlignment(Qt.AlignLeft)
        phone_layout.addWidget(birthdate_label)

        c, _ = self.util.모임코드조회()
        # Right layout for medal
        medal_layout = QHBoxLayout()
        medal_layout.setAlignment(Qt.AlignRight)
        statis = self.util.참석통계(마을원정보["uid"])[1:]
        for s in statis:
            if len(s) >= 2:
                code = c[s[0][0]]
                if s[0][2] == 1 and s[1][1] == 1:
                    if not os.path.exists(f'../asset/img/trophy{code[2][1:]}{code[3][1:]}.png'):
                        trophy.Trophy(code[2], code[3]).create_img()
                    image_label = QLabel(self)
                    image_label.setAlignment(Qt.AlignRight)

                    # QPixmap 로드 및 크기 조정
                    pixmap = QPixmap(f'../asset/img/trophy{code[2][1:]}{code[3][1:]}.png')
                    pixmap = pixmap.scaled(30, 30, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)

                    image_label.setPixmap(pixmap)
                    # self.image_label.setToolTip("trophy.png")  # 툴팁 설정
                    medal_layout.addWidget(image_label)
                else:
                    if s[0][2] <= 3:
                        if not os.path.exists(f'../asset/img/medal{s[0][2]}{code[2][1:]}{code[3][1:]}.png'):
                            medal.Medal(s[0][2], code[2], code[3]).create_img()
                        image_label = QLabel(self)
                        image_label.setAlignment(Qt.AlignRight)

                        # QPixmap 로드 및 크기 조정
                        pixmap = QPixmap(f'../asset/img/medal{s[0][2]}{code[2][1:]}{code[3][1:]}.png')
                        pixmap = pixmap.scaled(30, 30, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)

                        image_label.setPixmap(pixmap)
                        # self.image_label.setToolTip("trophy.png")  # 툴팁 설정
                        medal_layout.addWidget(image_label)
                    if s[1][1] <= 3:
                        if not os.path.exists(f'../asset/img/medal{s[1][1]}{code[2][1:]}{code[3][1:]}.png'):
                            medal.Medal(s[1][1], code[2], code[3]).create_img()
                        image_label = QLabel(self)
                        image_label.setAlignment(Qt.AlignRight)

                        # QPixmap 로드 및 크기 조정
                        pixmap = QPixmap(f'../asset/img/medal{s[1][1]}{code[2][1:]}{code[3][1:]}.png')
                        pixmap = pixmap.scaled(30, 30, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)

                        image_label.setPixmap(pixmap)
                        # self.image_label.setToolTip("trophy.png")  # 툴팁 설정
                        medal_layout.addWidget(image_label)



        # Add phone and birthdate layouts to the main phone_birthdate_layout
        down_layout.addLayout(phone_layout)
        down_layout.addLayout(medal_layout)

        # Add the phone and birthdate layout to the main layout
        main_layout.addLayout(down_layout)

        # Set the layout for the widget
        self.setLayout(main_layout)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Set up the main window layout
        main_layout = QVBoxLayout()

        # Create business card widgets
        card1 = BusinessCardWidget({'uid': 4, '이름': '박찬호', '생년월일': 960429, '성별': '남', '전화번호': '010-7378-7996'})
        card2 = BusinessCardWidget({'uid': 4, '이름': '박찬호', '생년월일': 960429, '성별': '남', '전화번호': '010-7378-7996'})

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
