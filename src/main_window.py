import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QMenuBar,
    QSplitter,
    QToolTip,
    QCheckBox, QLabel
)
from PyQt5.QtGui import QFontDatabase, QFont, QIcon
from PyQt5.QtCore import Qt
import util
import 날짜유틸
from meeting import AttendanceTable
from setMeeting import MeetingApp
from graph import GraphWindow  # Import the GraphWindow class
from member_table_widget import StudentTableWidget
from member_details_window import StudentDetailsWindow


class StudentListWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.util = util.Util()
        self.setWindowTitle("마을원 명단")
        self.setGeometry(100, 100, 1200, 700)  # Increase width and height

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

        meeting_menu = self.menu_bar.addMenu('모임')
        meeting_submenu1 = meeting_menu.addAction('마을 모임 보기')
        meeting_submenu2 = meeting_menu.addAction('모임 관리')

        # Create a QSplitter to divide the window horizontally
        splitter = QSplitter(Qt.Horizontal)

        # Create widgets for the left and right sides of the splitter
        left_widget = QWidget()
        right_widget = QWidget()

        # Set up layouts for the left and right widgets
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        # Initialize GraphWindow and add it to the left layout
        self.graph_window = GraphWindow()
        left_layout.addWidget(self.graph_window)

        check_layout = QHBoxLayout()

        # Set alignment to left
        check_layout.setAlignment(Qt.AlignLeft)

        # Create checkboxes and connect to the methods
        self.gender_장결_include = QCheckBox('장결자 제외')
        self.gender_장결_include.setChecked(False)  # 기본 설정은 체크 해제 상태
        self.gender_장결_include.stateChanged.connect(self.toggle_absent_rows)
        check_layout.addWidget(self.gender_장결_include)

        self.gender_졸업_include = QCheckBox('졸업자 제외')
        self.gender_졸업_include.setChecked(False)  # 기본 설정은 체크 해제 상태
        self.gender_졸업_include.stateChanged.connect(self.toggle_absent_rows)
        check_layout.addWidget(self.gender_졸업_include)

        self.students = self.util.select_all("마을원")
        count_layout = QHBoxLayout()
        count_layout.setAlignment(Qt.AlignRight)
        self.count_label = QLabel(f'총 {len(self.students[1:])}명')
        count_layout.addWidget(self.count_label)
        check_layout.addLayout(count_layout)
        right_layout.addLayout(check_layout)

        # Set up the right layout with the student table and buttons
        self.students = self.util.select_all("마을원")
        self.header = ['uid'] + self.students[0][1:]
        self.student_table = StudentTableWidget(self.students, self.header, self.util)
        right_layout.addWidget(self.student_table)

        # Add buttons to the right layout
        self.button_layout = QHBoxLayout()
        self.save_button = QPushButton("저장")
        self.reset_button = QPushButton("초기화")
        self.save_button.setEnabled(False)
        self.reset_button.setEnabled(False)
        self.button_layout.addWidget(self.save_button)
        self.button_layout.addWidget(self.reset_button)
        right_layout.addLayout(self.button_layout)

        # Set layouts for the left and right widgets
        left_widget.setLayout(left_layout)
        right_widget.setLayout(right_layout)

        # Add widgets to the splitter
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)

        # Add the splitter to the main layout
        main_layout = QVBoxLayout(self.central_widget)
        main_layout.addWidget(splitter)

        # Set initial sizes of the splitter sections
        splitter.setSizes([600, 800])

        # Connect signals and slots
        self.student_table.cellChanged.connect(self.enable_buttons)
        self.save_button.clicked.connect(self.save_changes)
        self.reset_button.clicked.connect(self.reset_changes)
        self.student_table.cellClicked.connect(self.handle_cell_click)
        self.student_table.horizontalHeader().sectionClicked.connect(self.sort_by_column)
        self.details_windows = []

        # Connect file_submenu1 and file_submenu2 to actions
        meeting_submenu1.triggered.connect(self.open_add_meeting_window)
        meeting_submenu2.triggered.connect(self.open_set_meeting_window)
        self.setWindowIcon(QIcon('../asset/icon/icon.ico'))

    def toggle_absent_rows(self, state):
        """Toggle the visibility of rows where '장결' is marked."""
        exclude_absent = self.gender_장결_include.isChecked()
        exclude_graduated = self.gender_졸업_include.isChecked()
        count = self.student_table.hide_rows_with_absence(exclude_absent, exclude_graduated)
        self.graph_window.update_pies(exclude_absent, exclude_graduated)
        self.count_label.setText(f'총 {count}명')

    def open_add_meeting_window(self):
        self.add_meeting_window = AttendanceTable()
        self.add_meeting_window.show()

    def open_set_meeting_window(self):
        self.set_meeting_window = MeetingApp()
        self.set_meeting_window.show()

    def handle_cell_click(self, row, column):
        column_name = self.student_table.horizontalHeaderItem(column).text()
        if column_name == "이름":
            self.show_student_details(row, column)

    def enable_buttons(self):
        self.save_button.setEnabled(True)
        self.reset_button.setEnabled(True)

    def reset_changes(self):
        self.student_table.reset_changes()
        self.save_button.setEnabled(False)
        self.reset_button.setEnabled(False)

    def save_changes(self):
        changed_data = self.student_table.get_changed_data()
        print("Changed Data:", changed_data)
        self.save_button.setEnabled(False)
        self.reset_button.setEnabled(False)

    def sort_by_column(self, column_index):
        self.student_table.sort_by_column(column_index)

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

    # Load stylesheet from file
    with open('styles.qss', 'r', encoding='utf-8') as f:
        app.setStyleSheet(f.read())
    app.setWindowIcon(QIcon('../asset/icon/icon.ico'))
    font_path = '../asset/font/감탄로드바탕체 Regular.ttf'
    font_path = '../asset/font/감탄로드돋움체 Regular.ttf'
    font_id = QFontDatabase.addApplicationFont(font_path)
    font_family = QFontDatabase.applicationFontFamilies(font_id)[0]

    custom_font = QFont(font_family, 10)
    QToolTip.setFont(custom_font)
    app.setFont(custom_font)

    window = StudentListWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
