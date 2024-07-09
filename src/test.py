import sys
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
import util

class StudentDetailsWindow(QWidget):
    def __init__(self, student_name):
        super().__init__()
        self.setWindowTitle("Student Details")
        self.setGeometry(150, 150, 200, 100)
        layout = QVBoxLayout()
        self.label = QLabel(f"Selected Student: {student_name}", self)
        layout.addWidget(self.label)
        self.setLayout(layout)


class StudentListWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.util = util.Util
        self.setWindowTitle("Student List")
        self.setGeometry(100, 100, 400, 500)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.student_table = QTableWidget()
        self.student_table.setColumnCount(3)
        self.student_table.setHorizontalHeaderLabels(["Name", "Age", "Gender"])
        self.layout.addWidget(self.student_table)

        self.populate_student_table()

        self.student_table.cellClicked.connect(self.show_student_details)
        self.student_table.horizontalHeader().sectionClicked.connect(self.sort_by_column)

        self.current_highlighted_row = -1
        self.sort_order = Qt.AscendingOrder
        self.details_windows = []  # List to keep track of detail windows

    def populate_student_table(self):
        self.students = [
            {"name": f"Student {i + 1}", "age": random.randint(18, 25), "gender": random.choice(["Male", "Female"])}
            for i in range(70)
        ]
        res = self.util.select_all(self, "학생")
        print(res)
        self.student_table.setRowCount(len(self.students))

        for row, student in enumerate(self.students):
            self.student_table.setItem(row, 0, QTableWidgetItem(student["name"]))
            self.student_table.setItem(row, 1, QTableWidgetItem(str(student["age"])))

            gender_item = QTableWidgetItem(student["gender"])
            if student["gender"] == "Male":
                gender_item.setBackground(QColor(173, 216, 230))  # Light blue for male
            else:
                gender_item.setBackground(QColor(255, 182, 193))  # Light pink for female
            self.student_table.setItem(row, 2, gender_item)

    def sort_by_column(self, column_index):
        if self.student_table.horizontalHeader().sortIndicatorOrder() == Qt.AscendingOrder:
            self.student_table.sortItems(column_index, Qt.AscendingOrder)
            self.student_table.horizontalHeader().setSortIndicator(column_index, Qt.DescendingOrder)
        else:
            self.student_table.sortItems(column_index, Qt.DescendingOrder)
            self.student_table.horizontalHeader().setSortIndicator(column_index, Qt.AscendingOrder)

    def show_student_details(self, row, column):
        student_name = self.student_table.item(row, 0).text()
        details_window = StudentDetailsWindow(student_name)
        details_window.show()
        self.details_windows.append(details_window)


def main():
    app = QApplication(sys.argv)
    window = StudentListWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
