import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QScrollArea, QGroupBox, \
    QHBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QSpacerItem, QSizePolicy, QToolTip, QTextBrowser
from PyQt5.QtGui import QPainter, QColor, QFontMetrics, QPalette, QFontDatabase, QFont, QCursor
from PyQt5.QtCore import Qt, QRect, QSize, QPoint
import util
import test2

scrollbar_style = """
        QScrollBar:vertical {
            border: none;
            background: #f0f0f0;
            width: 10px;
            margin: 0px 0px 0px 0px;
        }
        QScrollBar::handle:vertical {
            background: #c0c0c0;
            min-height: 20px;
        }
        QScrollBar::add-line:vertical {
            background: #d0d0d0;
            height: 0px;
            subcontrol-position: bottom;
            subcontrol-origin: margin;
        }
        QScrollBar::sub-line:vertical {
            background: #d0d0d0;
            height: 0px;
            subcontrol-position: top;
            subcontrol-origin: margin;
        }
        QScrollBar:horizontal {
            border: none;
            background: #f0f0f0;
            height: 10px;
            margin: 0px 0px 0px 0px;
        }
        QScrollBar::handle:horizontal {
            background: #c0c0c0;
            min-width: 20px;
        }
        QScrollBar::add-line:horizontal {
            background: #d0d0d0;
            width: 0px;
            subcontrol-position: right;
            subcontrol-origin: margin;
        }
        QScrollBar::sub-line:horizontal {
            background: #d0d0d0;
            width: 0px;
            subcontrol-position: left;
            subcontrol-origin: margin;
        }
        """

class RoundedRectLabel(QWidget):
    def __init__(self, text):
        super().__init__()
        self.text = text
        self.setMinimumSize(20, 20)  # 최소 크기 설정 (가로, 세로)
        self.setMouseTracking(True)  # 마우스 움직임 추적 활성화
        self.tooltip_info = ["2024년 6월 30일"]

    def getToolTipText(self):
        text = f"<b>{self.tooltip_info[0]}</b><br>{self.text}"
        return text

    def enterEvent(self, event):
        tooltip_height = self.calculate_tooltip_height()
        cursor_pos = QCursor.pos()
        tooltip_pos = cursor_pos + QPoint(0, -tooltip_height)
        QToolTip.showText(tooltip_pos, self.getToolTipText(), self, self.rect(), 3000)
        super().enterEvent(event)

    def leaveEvent(self, event):
        QToolTip.hideText()  # 툴팁 숨기기
        super().leaveEvent(event)

    def mouseMoveEvent(self, event):
        tooltip_height = self.calculate_tooltip_height()
        cursor_pos = QCursor.pos()
        tooltip_pos = cursor_pos + QPoint(0, -tooltip_height)
        QToolTip.showText(tooltip_pos, self.getToolTipText(), self, self.rect(), 3000)
        super().mouseMoveEvent(event)

    def calculate_tooltip_height(self):
        # QFontMetrics를 사용하여 텍스트의 높이 계산
        font_metrics = QFontMetrics(QToolTip.font())
        text_height = font_metrics.height()
        line_count = f"<b>안내</b><br>{self.text}".count("<br>") + 1
        total_height = text_height * line_count + 35  # 텍스트 라인 수에 따라 높이 계산 (패딩 포함)
        return total_height

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)  # 안티앨리어싱 활성화

        rect = event.rect()  # 위젯의 사각형 영역
        rect.adjust(2, 2, -2, -2)  # 사각형을 약간 안쪽으로 줄임

        icon_color = {
            "자체예배": "#ff595e",
            "더원": "#ff595e",
            "사랑모임": "#f79824",
            "금철": "#1982c4",
            "대예배": "#6a4c93",
        }
        if icon_color.__contains__(self.text):
            painter.setBrush(QColor(icon_color[self.text]))  # 직사각형 색상 설정
        else:
            painter.setBrush(QColor("#FFFFFF"))  # default 색상 설정

        painter.drawRoundedRect(rect, 5, 5)  # 둥근 직사각형 그리기

        font_metrics = QFontMetrics(self.font())  # 현재 폰트 메트릭스
        text_width = font_metrics.horizontalAdvance(self.text)  # 텍스트의 너비 계산
        text_height = font_metrics.height()  # 텍스트의 높이 계산
        text_rect = QRect(rect.left()+2, rect.top()+3, text_width, text_height)  # 텍스트 위치 지정

        painter.setPen(Qt.white)  # 펜 색상 설정
        painter.drawText(text_rect, Qt.AlignCenter, self.text)  # 텍스트를 중앙 정렬하여 그리기

    def sizeHint(self):
        font_metrics = QFontMetrics(self.font())  # 현재 폰트 메트릭스
        text_width = font_metrics.horizontalAdvance(self.text)  # 텍스트의 너비 계산
        text_height = font_metrics.height()  # 텍스트의 높이 계산
        return QSize(text_width+10, text_height+10)  # 위젯의 기본 크기 지정

class StudentDetailsWindow(QWidget):
    def __init__(self, 마을원_uid, res):
        try:
            super().__init__()
            self.setWindowTitle("마을원 세부 정보")
            self.setGeometry(150, 150, 400, 300)

            main_layout = QVBoxLayout()
            main_layout.setContentsMargins(0, 0, 0, 0)  # 여백을 제거합니다.
            main_layout.setSpacing(0)  # 위젯 간의 간격을 제거합니다.

            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)
            scroll_area.setStyleSheet("background-color: #FFFFFF;")

            scroll_widget = QWidget()
            scroll_widget.setStyleSheet("background-color: #FFFFFF;")
            scroll_layout = QVBoxLayout(scroll_widget)
            scroll_layout.setContentsMargins(0, 0, 0, 0)  # 여백을 제거합니다.
            scroll_layout.setSpacing(0)  # 위젯 간의 간격을 제거합니다.
            scrollbar_style = """
                        QScrollBar:vertical {
                            background-color: #F0F0F0;
                            width: 15px;
                            margin: 0px 3px 0px 3px;
                        }
                        QScrollBar::handle:vertical {
                            background-color: #C0C0C0;
                            min-height: 5px;
                            border-radius: 5px;
                        }
                        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                            background: none;
                            border: none;
                        }
                        """
            scroll_widget.setStyleSheet(scrollbar_style)

            # Add QTextBrowser to display HTML content
            html_content = """
                        <html>
                        <head>
                            <style>
                                body {
                                    font-family: Arial, sans-serif;
                                    background-color: #E0E0E0;
                                    padding: 5px;
                                }
                                h1 {
                                    text-align: center;
                                    color: #333333;
                                }
                            </style>
                        </head>
                        <body>
                            <h1>마을원 세부 정보</h1>
                        </body>
                        </html>
                        """
            text_browser = QTextBrowser()
            text_browser.setHtml(html_content)
            text_browser.setFixedHeight(50)
            scroll_layout.addWidget(text_browser)

            for week_info in res.keys():
                meetings = res[week_info]
                group_box = QGroupBox(f"{week_info}")
                group_box.setFixedHeight(50)
                if len(meetings) > 0:
                    group_box.setStyleSheet("background-color: #D4E4FE;")
                else:
                    group_box.setStyleSheet("background-color: #FFEEEE;")

                group_layout = QVBoxLayout()

                # Horizontal layout to hold labels in a row
                h_layout = QHBoxLayout()

                for meeting in meetings:
                    label = RoundedRectLabel(meeting)
                    label.setFixedSize(label.sizeHint())
                    h_layout.addWidget(label)

                spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
                h_layout.addItem(spacer)

                group_layout.addLayout(h_layout)
                group_box.setLayout(group_layout)
                scroll_layout.addWidget(group_box)

            scroll_widget.setLayout(scroll_layout)
            scroll_area.setWidget(scroll_widget)

            main_layout.addWidget(scroll_area)
            self.setLayout(main_layout)

            # Connect the vertical scroll bar's valueChanged signal to a custom method
            scroll_area.verticalScrollBar().valueChanged.connect(self.refresh_window)
        except Exception as e:
            print(f"Error: {e}")
            return None

    def refresh_window(self):
        # Force a repaint of the window
        self.repaint()


class StudentListWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.util = util.Util()
        self.setWindowTitle("마을원 명단")
        self.setGeometry(100, 100, 400, 500)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.students = self.util.select_all("마을원")
        self.header = ['uid'] + self.students[0][1:]  # Include 'uid' in the header
        self.student_table = QTableWidget()
        self.student_table.setColumnCount(len(self.header))
        self.student_table.setHorizontalHeaderLabels(self.header)
        self.layout.addWidget(self.student_table)

        self.populate_student_table()

        # UID 열 숨기기
        self.student_table.hideColumn(0)

        # 버튼 추가
        self.button_layout = QHBoxLayout()
        self.save_button = QPushButton("저장")
        self.reset_button = QPushButton("초기화")
        self.save_button.setEnabled(False)
        self.reset_button.setEnabled(False)
        self.button_layout.addWidget(self.save_button)
        self.button_layout.addWidget(self.reset_button)
        self.layout.addLayout(self.button_layout)

        # 이벤트 연결
        self.student_table.cellChanged.connect(self.enable_buttons)
        self.save_button.clicked.connect(self.save_changes)
        self.reset_button.clicked.connect(self.reset_changes)

        self.student_table.cellClicked.connect(self.handle_cell_click)
        self.student_table.horizontalHeader().sectionClicked.connect(self.sort_by_column)

        self.current_highlighted_row = -1
        self.sort_order = Qt.AscendingOrder
        self.details_windows = []  # List to keep track of detail windows

        self.original_data = [row[:] for row in self.students]  # Save original data

    def handle_cell_click(self, row, column):
        column_name = self.student_table.horizontalHeaderItem(column).text()
        if column_name == "이름":
            self.show_student_details(row, column)

    def populate_student_table(self):
        students = self.students[1:]  # Skip the header row
        self.student_table.setRowCount(len(students))

        for row, student in enumerate(students):
            for col, data in enumerate(student):  # Skip the 'uid' column
                item = QTableWidgetItem(str(data))
                if self.header[col] == '성별':  # Assuming '성별' is the gender column
                    if data == "남":
                        item.setBackground(QColor(173, 216, 230))  # Light blue for male #D4E4FE
                    else:
                        item.setBackground(QColor(255, 182, 193))  # Light pink for female #FFEEEE
                self.student_table.setItem(row, col, item)

    def enable_buttons(self):
        self.save_button.setEnabled(True)
        self.reset_button.setEnabled(True)

    def reset_changes(self):
        self.students = [row[:] for row in self.original_data]
        self.populate_student_table()
        self.save_button.setEnabled(False)
        self.reset_button.setEnabled(False)

    def save_changes(self):
        changed_data = []
        for row in range(self.student_table.rowCount()):
            row_data = []
            for col in range(self.student_table.columnCount()):
                item = self.student_table.item(row, col)
                row_data.append(item.text() if item else "")
            changed_data.append(row_data)
        print("Changed Data:", changed_data)
        self.save_button.setEnabled(False)
        self.reset_button.setEnabled(False)

    def sort_by_column(self, column_index):
        if self.student_table.horizontalHeader().sortIndicatorOrder() == Qt.AscendingOrder:
            self.student_table.sortItems(column_index, Qt.AscendingOrder)
            self.student_table.horizontalHeader().setSortIndicator(column_index, Qt.DescendingOrder)
        else:
            self.student_table.sortItems(column_index, Qt.DescendingOrder)
            self.student_table.horizontalHeader().setSortIndicator(column_index, Qt.AscendingOrder)

    def show_student_details(self, row, column):
        마을원_uid = self.student_table.item(row, 0).text()
        res = self.util.참석조회(마을원_uid)
        weeks = dict()
        for r in res[1:]:
            week = test2.get_week_of_month(r[2])
            if not weeks.__contains__(week):
                weeks[week] = []
            if r[0] == 1:
                weeks[week].append(r[1])
        details_window = StudentDetailsWindow(마을원_uid, weeks)
        details_window.show()
        self.details_windows.append(details_window)

def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(scrollbar_style)
    font_path = '../asset/font/감탄로드바탕체 Regular.ttf'
    font_path = '../asset/font/감탄로드돋움체 Regular.ttf'
    font_id = QFontDatabase.addApplicationFont(font_path)
    font_family = QFontDatabase.applicationFontFamilies(font_id)[0]

    custom_font = QFont(font_family, 10)
    app.setStyleSheet("QToolTip { color: #000000; background-color: #FFFFFF; border: 1px solid white; padding: 5px; }")

    QToolTip.setFont(custom_font)
    app.setFont(custom_font)

    window = StudentListWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
