import sys
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QApplication, QStyledItemDelegate, QComboBox
from PyQt5.QtGui import QColor, QCursor
from PyQt5.QtCore import Qt

class ComboBoxDelegate(QStyledItemDelegate):
    def __init__(self, items, parent=None):
        super().__init__(parent)
        self.items = items

    def createEditor(self, parent, option, index):
        editor = QComboBox(parent)
        editor.addItems(self.items)
        return editor

    def setEditorData(self, editor, index):
        value = index.data()
        if value in self.items:
            editor.setCurrentText(value)

    def setModelData(self, editor, model, index):
        model.setData(index, editor.currentText())

class StudentTableWidget(QTableWidget):
    def __init__(self, students, header, util):
        super().__init__()
        self.util = util
        self.students = students

        self.header = [col if col != '장결여부' else '장결' for col in header]
        self.header = [col if col != '졸업여부' else '졸업' for col in self.header]
        self.header = [col if col != '리더여부' else '리더' for col in self.header]
        self.header = [col if col != '빠른여부' else '빠른' for col in self.header]

        self.original_data = [row[:] for row in students]

        self.setColumnCount(len(self.header))
        self.setHorizontalHeaderLabels(self.header)
        self.populate_table()

        self.setColumnHidden(0, True)  # uid 컬럼 숨기기

        self.setColumnWidth(1, 40)
        self.setColumnWidth(2, 60)
        self.setColumnWidth(3, 40)
        self.setColumnWidth(4, 70)
        self.setColumnWidth(5, 30)
        self.setColumnWidth(6, 120)
        self.setColumnWidth(7, 60)
        self.setColumnWidth(8, 40)
        self.setColumnWidth(9, 40)
        self.setColumnWidth(10, 40)
        self.setColumnWidth(11, 40)
        self.setColumnWidth(12, 40)

        self.sort_states = {col: 0 for col in range(len(self.header))}
        self.last_clicked_column = None

        self.horizontalHeader().sectionClicked.connect(self.handle_header_click)
        self.horizontalHeader().installEventFilter(self)
        self.verticalHeader().hide()

        self.setStyleSheet("QHeaderView::section { background-color: '#F0F0F0'; }")

        # 드롭다운 설정
        self.setItemDelegateForColumn(self.header.index('구분'), ComboBoxDelegate(['A', 'B', 'C', 'D', 'L'], self))

    def populate_table(self):
        self.setRowCount(len(self.students) - 1)
        for row, student in enumerate(self.students[1:]):
            for col, data in enumerate(student):
                if self.header[col] in ('장결', '졸업', '리더', '빠른', '또래장'):
                    data = '✅' if data == 1 else '❌'
                elif self.header[col] == '사랑장':
                    data = '' if data is None else data

                item = QTableWidgetItem(str(data))
                item.setTextAlignment(Qt.AlignCenter)

                if self.header[col] == '성별':
                    if data == "남":
                        item.setBackground(QColor(173, 216, 230))
                    else:
                        item.setBackground(QColor(255, 182, 193))

                self.setItem(row, col, item)

    def handle_header_click(self, column_index):
        if self.last_clicked_column is not None and self.last_clicked_column != column_index:
            self.sort_states[self.last_clicked_column] = 0

        self.sort_states[column_index] = (self.sort_states[column_index] + 1) % 2
        self.last_clicked_column = column_index

        if self.sort_states[column_index] == 1:
            self.sortItems(column_index, Qt.AscendingOrder)
            self.horizontalHeader().setSortIndicator(column_index, Qt.AscendingOrder)
        elif self.sort_states[column_index] == 0:
            self.sortItems(column_index, Qt.DescendingOrder)
            self.horizontalHeader().setSortIndicator(column_index, Qt.DescendingOrder)

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

    def eventFilter(self, obj, event):
        if obj == self.horizontalHeader() and event.type() == event.MouseMove:
            pos = event.pos()
            index = self.horizontalHeader().logicalIndexAt(pos)

            if index == 1:
                self.setCursor(QCursor(Qt.PointingHandCursor))
            else:
                self.setCursor(QCursor(Qt.ArrowCursor))

            return True
        return super().eventFilter(obj, event)

    def hide_rows_with_absence(self, 장결제외, 졸업제외):
        absence_col_index = self.header.index('장결')  # Find the index of the "장결" column
        graduated_col_index = self.header.index('졸업')  # Find the index of the "졸업" column

        # Loop through each row to hide or show based on the criteria
        for row in range(self.rowCount()):
            # Get the items in the "장결" and "졸업" columns
            absence_item = self.item(row, absence_col_index)
            graduated_item = self.item(row, graduated_col_index)

            # Determine if the row should be hidden based on the flags
            hide_row = False

            if 장결제외 and 졸업제외:
                # Hide if either "장결" or "졸업" is "✅"
                hide_row = (absence_item and absence_item.text() == '✅') or \
                           (graduated_item and graduated_item.text() == '✅')
            elif 장결제외:
                # Hide if only "장결" is "✅"
                hide_row = absence_item and absence_item.text() == '✅'
            elif 졸업제외:
                # Hide if only "졸업" is "✅"
                hide_row = graduated_item and graduated_item.text() == '✅'

            # Set the row visibility based on the computed flag
            self.setRowHidden(row, hide_row)

        # Now renumber the visible rows
        visible_row_number = 0
        for row in range(self.rowCount()):
            if not self.isRowHidden(row):  # Check if the row is visible
                visible_row_number += 1
                # Optionally, update the visible row number in the first column
                # self.setItem(row, 0, QTableWidgetItem(str(visible_row_number)))

        return visible_row_number

if __name__ == "__main__":
    import util
    util = util.Util()
    students = util.select_all("마을원")
    header = ['uid'] + students[0][1:]

    app = QApplication(sys.argv)
    window = StudentTableWidget(students, header, util)

    window.resize(600, 400)
    window.show()
    sys.exit(app.exec_())
