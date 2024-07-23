import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QScrollBar, QAction, QMenu
from PyQt5.QtCore import Qt
import util
from 날짜유틸 import format_datetime
from addMeeting import AddMeetingWindow


class AttendanceTable(QMainWindow):
    def __init__(self):
        super().__init__()
        self.util = util.Util()

        # Window setup
        self.setWindowTitle("Attendance Table")

        # Table widget
        self.table_widget = QTableWidget()
        self.setCentralWidget(self.table_widget)

        # Set table column count (excluding UID)
        self.table_widget.setColumnCount(4)

        # Fetch column headers from util.모임조회()
        모임목록 = self.util.모임조회()
        code2desc, desc2code = self.util.모임코드조회()
        print(code2desc)
        self.table_widget.setHorizontalHeaderLabels(모임목록[0][1:])

        # Sample data excluding UID
        self.data = 모임목록[1:]

        # Set table row count
        self.table_widget.setRowCount(len(self.data))

        # Populate the table
        for row_idx, row_data in enumerate(self.data):
            for col_idx, item in enumerate(row_data[1:]):
                table_item = QTableWidgetItem()
                if col_idx == 0:
                    # Format datetime for the first column
                    table_item.setText(format_datetime(item))
                elif col_idx == 1:
                    table_item.setText(code2desc[item][1])
                elif isinstance(item, float):
                    # Handle float values
                    table_item.setText(f"{item:.2f}")
                else:
                    # Handle other values (int, str, etc.)
                    table_item.setText(str(item))

                self.table_widget.setItem(row_idx, col_idx, table_item)

        # Resize window based on table width
        self.resize_to_table_width()

        # Create menu
        self.create_menu()

    def resize_to_table_width(self):
        total_width = 0
        for col in range(self.table_widget.columnCount()):
            total_width += self.table_widget.columnWidth(col)

        # Add a bit of extra width
        total_width += self.table_widget.verticalHeader().width()
        total_width += 2 * self.table_widget.frameWidth()

        # Check if total width exceeds current screen width
        screen_width = QApplication.desktop().screenGeometry().width()
        if total_width > screen_width:
            total_width = screen_width

        self.resize(total_width, self.height())

    def create_menu(self):
        # Create a menu bar
        menubar = self.menuBar()

        # Create "등록" menu
        register_menu = menubar.addMenu("등록")

        # Create "신규 모임 등록" action
        new_meeting_action = QAction("신규 모임 등록", self)
        new_meeting_action.triggered.connect(self.open_add_meeting_window)

        # Add action to "등록" menu
        register_menu.addAction(new_meeting_action)

    def open_add_meeting_window(self):
        self.add_meeting_window = AddMeetingWindow()
        self.add_meeting_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AttendanceTable()
    window.show()
    sys.exit(app.exec_())
