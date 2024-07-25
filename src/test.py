import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QScrollArea, QGroupBox, \
    QHBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QSpacerItem, QSizePolicy, QToolTip, QTextBrowser, QMenuBar
from PyQt5.QtGui import QPainter, QColor, QFontMetrics, QPalette, QFontDatabase, QFont, QCursor
from PyQt5.QtCore import Qt, QRect, QSize, QPoint
import util
import 날짜유틸, namecard
from meeting import AttendanceTable
from graph import GraphWindow  # Import the GraphWindow class
from roundedRectLabel import RoundedRectLabel

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

class StudentDetailsWindow(QWidget):
    def __init__(self, 마을원정보, res, util):
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
            main_layout.addWidget(namecard.BusinessCardWidget(마을원정보["이름"], util.사랑장조회(마을원정보["uid"]), 마을원정보["전화번호"],
                                                              str(마을원정보["생년월일"])))

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
        self.setGeometry(100, 100, 800, 600)  # Increase width and height

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.menu_bar = QMenuBar(self)
        self.setMenuBar(self.menu_bar)

        file_menu = self.menu_bar.addMenu('파일')
        file_submenu1 = file_menu.addAction('파일 서브메뉴 1')
        file_submenu2 = file_menu.addAction('파일 서브메뉴 2')

        settings_menu = self.menu_bar.addMenu('설정')
        settings_submenu1 = settings_menu.addAction('설정 서브메뉴 1')
        settings_submenu2 = settings_menu.addAction('설정 서브메뉴 2')

        self.layout = QVBoxLayout(self.central_widget)

        self.graph_window = GraphWindow()  # Create an instance of the GraphWindow
        self.layout.addWidget(self.graph_window)  # Add the graph window to the layout

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

        # Connect file_submenu1 to open AddMeetingWindow
        file_submenu1.triggered.connect(self.open_add_meeting_window)

    def open_add_meeting_window(self):
        self.add_meeting_window = AttendanceTable()
        self.add_meeting_window.show()

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
            week = 날짜유틸.get_week_of_month(r[2])
            if not weeks.__contains__(week):
                weeks[week] = []
            if r[0] == 1:
                date = 날짜유틸.convert_date_format(r[2].split()[0])
                weeks[week].append((r[1], date))
        마을원정보 = self.util.마을원정보조회(마을원_uid)
        details_window = StudentDetailsWindow(마을원정보, weeks, self.util)
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
