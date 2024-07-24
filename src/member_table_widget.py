from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHBoxLayout, QWidget, QVBoxLayout
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt


class StudentTableWidget(QTableWidget):
    def __init__(self, students, header, util):
        super().__init__()
        self.util = util
        self.students = students
        self.header = header
        self.original_data = [row[:] for row in students]  # Save original data

        self.setColumnCount(len(header))
        self.setHorizontalHeaderLabels(header)
        self.populate_table()

    def populate_table(self):
        self.setRowCount(len(self.students) - 1)  # Skip the header row
        for row, student in enumerate(self.students[1:]):
            for col, data in enumerate(student):
                item = QTableWidgetItem(str(data))
                if self.header[col] == '성별':  # Assuming '성별' is the gender column
                    if data == "남":
                        item.setBackground(QColor(173, 216, 230))  # Light blue for male
                    else:
                        item.setBackground(QColor(255, 182, 193))  # Light pink for female
                self.setItem(row, col, item)

    def get_changed_data(self):
        changed_data = []
        for row in range(self.rowCount()):
            row_data = []
            for col in range(self.columnCount()):
                item = self.item(row, col)
                row_data.append(item.text() if item else "")
            changed_data.append(row_data)
        return changed_data

    def reset_changes(self):
        self.students = [row[:] for row in self.original_data]
        self.populate_table()

    def sort_by_column(self, column_index):
        if self.horizontalHeader().sortIndicatorOrder() == Qt.AscendingOrder:
            self.sortItems(column_index, Qt.AscendingOrder)
            self.horizontalHeader().setSortIndicator(column_index, Qt.DescendingOrder)
        else:
            self.sortItems(column_index, Qt.DescendingOrder)
            self.horizontalHeader().setSortIndicator(column_index, Qt.AscendingOrder)
