import os
import sys
from PyQt5.QtGui import QPixmap, QFontDatabase
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea, QApplication
from PyQt5.QtGui import QPainter, QColor, QPen, QFont, QFontMetrics
from PyQt5.QtCore import QRectF, Qt
import font_util, util, medal, trophy

class TitleWidget(QWidget):
    def __init__(self, title):
        # 커스텀 폰트 등록
        super().__init__()
        font_path = "../asset/font/감탄로드돋움체 Thin.ttf"  # 커스텀 폰트 파일 경로
        font_id = QFontDatabase.addApplicationFont(font_path)
        self.font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        self.title = title
        self.setFixedHeight(20)  # 직사각형의 높이 설정
        self.set_width_to_title()

    def set_width_to_title(self):

        font = QFont(self.font_family, 10)
        metrics = QFontMetrics(font)
        if self.title[2] == 3:
            text = f'{self.title[1]} 목자'
        elif self.title[2] == 2:
            text = f'{self.title[1]} 새가족사랑장'
        elif self.title[2] == 1:
            text = f'{self.title[1]} 사랑장'
        elif self.title[2] == 0:
            text = f'{self.title[1]} {self.title[0]}사랑'
        text_width = metrics.horizontalAdvance(text)
        self.setFixedWidth(text_width + 20)  # 텍스트 너비에 여백 추가

    def paintEvent(self, event):
        painter = QPainter(self)

        # 아이콘 색상 설정
        icon_color = {
            "사랑원": "#fed9b7",
            "사랑장": "#cddafd",
            "새가족사랑장": "#cddafd",
            "목자": "#bee1e6",
        }

        # 둥근 사각형 그리기
        painter.setRenderHint(QPainter.Antialiasing)  # 안티앨리어싱 활성화로 부드러운 경계선 처리

        # 제목 텍스트와 배경 색상 결정
        if self.title[2] == 3:
            text = f'{self.title[1]} 목자'
            background_color = icon_color["목자"]
        elif self.title[2] == 2:
            text = f'{self.title[1]} 새가족사랑장'
            background_color = icon_color["새가족사랑장"]
        elif self.title[2] == 1:
            text = f'{self.title[1]} 사랑장'
            background_color = icon_color["사랑장"]
        elif self.title[2] == 0:
            text = f'{self.title[1]} {self.title[0]}사랑'
            background_color = icon_color["사랑원"]

        # QFontMetrics를 사용하여 텍스트의 너비 계산
        font = QFont(self.font_family, 10)  # 폰트 설정 (폰트 이름, 크기)
        font.setWeight(QFont.Medium)  # 폰트 굵기 설정 (여기서는 Bold로 설정)

        painter.setFont(font)
        font_metrics = QFontMetrics(font)
        text_width = font_metrics.horizontalAdvance(text)  # 텍스트 너비 측정

        # 미관을 위한 여백 추가
        padding = 20
        rect_width = text_width + padding
        rect_height = self.height()

        # 직사각형을 화면 중앙에 위치시키기 위한 위치 계산
        rect_x = (self.width() - rect_width) / 2
        rect_y = 0

        # 동적으로 너비를 설정한 QRectF 생성
        rect = QRectF(rect_x, rect_y, rect_width, rect_height)

        # 브러쉬 및 펜 설정
        painter.setBrush(QColor(background_color))
        painter.setPen(Qt.NoPen)

        # 둥근 직사각형 그리기
        painter.drawRoundedRect(rect, 10, 10)  # 동적 너비로 둥근 사각형 그리기

        # 제목 텍스트 그리기
        painter.setPen(QColor(0, 0, 0))  # 텍스트 색상 설정 (검정색)
        painter.drawText(rect, Qt.AlignCenter, text)  # 사각형 안에 텍스트 중앙 정렬하여 그리기


class BusinessCardWidget(QWidget):
    def __init__(self, 마을원정보):
        super().__init__()
        self.util = util.Util()
        name = 마을원정보["이름"]
        titles = self.util.사랑장조회(마을원정보["uid"])
        phone = 마을원정보["전화번호"]
        birthdate = str(마을원정보["생년월일"])
        birthyear = str(마을원정보["또래"])

        # Set up the main layout
        main_layout = QVBoxLayout()

        # Horizontal layout for name and titles
        name_title_layout = QHBoxLayout()

        font_path = "../asset/font/감탄로드바탕체 Bold.ttf"  # Replace with your font file path
        custom_font_family = font_util.load_custom_font(font_path)

        # Name label
        name_label = QLabel(f"{name} ({birthyear}또래)")
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
        목자이력 = self.util.목자이력조회(마을원정보["uid"])[1:]
        for m in 목자이력:
            titles.append((마을원정보["이름"], m[0], 3))

        titles = sorted(titles, key=lambda x: x[1], reverse=True)
        print(titles)
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

        # 메달/트로피 설정을 위한 메인 로직
        c, _ = self.util.모임코드조회()
        medal_layout = QHBoxLayout()
        medal_layout.setAlignment(Qt.AlignRight)
        statis = self.util.참석통계(마을원정보["uid"])[1:]

        for s in statis:
            if len(s) >= 2:
                code = c[s[0][0]]
                if code[4] < 5:
                    continue
                # 이미지 타입 결정
                if s[0][2] == 1 and s[1][1] == 1:
                    image_type = 'trophy'
                    ranks = [(1, '참석수/참석률')]  # 트로피는 순위가 필요 없음
                else:
                    image_type = 'medal'
                    # 두 랭크 중 더 높은 랭크를 선택 (숫자가 낮을수록 랭크가 높다)
                    rank1 = (s[0][2], '참석수')
                    rank2 = (s[1][1], '참석률')

                    # 두 랭크가 모두 3위 이내에 있는지 확인하고 더 높은 랭크 선택
                    if rank1[0] <= 3 and rank2[0] <= 3:
                        rank_to_use = min(rank1, rank2, key=lambda x: x[0])
                        ranks = [rank_to_use]
                    elif rank1[0] <= 3:
                        ranks = [rank1]
                    elif rank2[0] <= 3:
                        ranks = [rank2]
                    else:
                        ranks = []  # 둘 다 3위 이내가 아니면 추가 안 함

                # 조건에 따라 이미지 추가
                for rank in ranks:
                    image_path = self.create_image_if_not_exists(image_type, rank[0], code[2], code[3])
                    self.add_image_to_layout(medal_layout, image_path, f"{code[1]} {rank[1]} #{rank[0]}")

        # Add phone and birthdate layouts to the main phone_birthdate_layout
        down_layout.addLayout(phone_layout)
        down_layout.addLayout(medal_layout)

        # Add the phone and birthdate layout to the main layout
        main_layout.addLayout(down_layout)

        # Set the layout for the widget
        self.setLayout(main_layout)

    def add_image_to_layout(self, layout, image_path, tooltip_text):
        """
        QPixmap을 사용하여 QLabel을 생성하고 레이아웃에 추가하며 툴팁을 설정하는 헬퍼 함수.

        Args:
            layout (QHBoxLayout): QLabel을 추가할 레이아웃.
            image_path (str): QPixmap에 로드할 이미지의 경로.
            tooltip_text (str): 이미지 위에 마우스를 올렸을 때 표시할 툴팁 텍스트.
        """
        image_label = QLabel(self)
        image_label.setAlignment(Qt.AlignRight)

        # QPixmap을 로드하고 크기 조정
        pixmap = QPixmap(image_path)
        pixmap = pixmap.scaled(30, 30, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)

        image_label.setPixmap(pixmap)
        image_label.setToolTip(tooltip_text)  # 툴팁 설정
        layout.addWidget(image_label)

    def create_image_if_not_exists(self, image_type, rank, code2, code3):
        """
        이미지가 존재하지 않을 경우 이미지를 생성하는 헬퍼 함수.

        Args:
            image_type (str): 이미지의 종류 ('trophy' 또는 'medal').
            rank (int): 메달의 순위 번호.
            code2 (str): 코드의 두 번째 부분.
            code3 (str): 코드의 세 번째 부분.

        Returns:
            str: 이미지 파일의 경로.
        """
        if image_type == 'trophy':
            image_path = f'../asset/img/trophy{code2[1:]}{code3[1:]}.png'
            if not os.path.exists(image_path):
                trophy.Trophy(code2, code3).create_img()
        else:
            image_path = f'../asset/img/medal{rank}{code2[1:]}{code3[1:]}.png'
            if not os.path.exists(image_path):
                medal.Medal(rank, code2, code3).create_img()

        return image_path


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
