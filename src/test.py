import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QScrollArea, QGroupBox, QHBoxLayout, QTableWidget, QTableWidgetItem, QPushButton
from PyQt5.QtGui import QPainter, QColor, QFontMetrics
from PyQt5.QtCore import Qt, QRect, QSize
import util
import test2

class RoundedRectLabel(QWidget):
    def __init__(self, text):
        super().__init__()
        self.text = text
        self.setMinimumSize(20, 20)  # 최소 크기 설정 (가로, 세로)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)  # 안티앨리어싱 활성화

        rect = event.rect()  # 위젯의 사각형 영역
        rect.adjust(2, 2, -2, -2)  # 사각형을 약간 안쪽으로 줄임

        painter.setBrush(QColor(200, 200, 200))  # 직사각형 색상 설정
        painter.drawRoundedRect(rect, 10, 10)  # 둥근 직사각형 그리기

        font_metrics = QFontMetrics(self.font())  # 현재 폰트 메트릭스
        text_width = font_metrics.horizontalAdvance(self.text)  # 텍스트의 너비 계산
        text_height = font_metrics.height()  # 텍스트의 높이 계산
        text_rect = QRect(rect.left(), rect.top(), text_width, text_height)  # 텍스트 위치 지정

        painter.setPen(Qt.black)  # 펜 색상 설정
        painter.drawText(text_rect, Qt.AlignCenter, self.text)  # 텍스트를 중앙 정렬하여 그리기

    def sizeHint(self):
        return QSize(100, 30)  # 위젯의 기본 크기 지정

class StudentDetailsWindow(QWidget):
    def __init__(self, 마을원_uid, res):
        try:
            super().__init__()
            self.setWindowTitle("Student Details")
            self.setGeometry(150, 150, 400, 300)

            main_layout = QVBoxLayout()
            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)

            scroll_widget = QWidget()
            scroll_layout = QVBoxLayout(scroll_widget)

            for week_info in res.keys():
                meetings = res[week_info]
                group_box = QGroupBox(f"{week_info}")
                group_layout = QVBoxLayout()

                # Horizontal layout to hold labels in a row
                h_layout = QHBoxLayout()

                for meeting in meetings:
                    label = RoundedRectLabel(meeting)
                    h_layout.addWidget(label)

                group_layout.addLayout(h_layout)
                group_box.setLayout(group_layout)
                scroll_layout.addWidget(group_box)

            scroll_widget.setLayout(scroll_layout)
            scroll_area.setWidget(scroll_widget)

            main_layout.addWidget(scroll_area)
            self.setLayout(main_layout)
        except Exception as e:
            print(f"Error: {e}")
            return None

class StudentListWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.util = util.Util()
        self.setWindowTitle("Student List")
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

        # 스타일시트 설정
        self.set_scrollbar_style()

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

        self.student_table.cellClicked.connect(self.show_student_details)
        self.student_table.horizontalHeader().sectionClicked.connect(self.sort_by_column)

        self.current_highlighted_row = -1
        self.sort_order = Qt.AscendingOrder
        self.details_windows = []  # List to keep track of detail windows

        self.original_data = [row[:] for row in self.students]  # Save original data

    def set_scrollbar_style(self):
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
        self.student_table.setStyleSheet(scrollbar_style)

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
        for w in weeks.keys():
            print(weeks[w])
        details_window = StudentDetailsWindow(마을원_uid, weeks)
        details_window.show()
        self.details_windows.append(details_window)

def main():
    app = QApplication(sys.argv)
    window = StudentListWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
