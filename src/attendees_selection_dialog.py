# attendees_selection_dialog.py
import sys
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QApplication, QLineEdit, QTableWidget, QTableWidgetItem, QHeaderView, \
    QCheckBox, QDialogButtonBox, QComboBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
import util


class AttendeesSelectionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("참석 인원 선택")
        self.util = util.Util()

        # Initialize the checked state dictionary
        self.checked_state = {}

        # Layout
        dialog_layout = QVBoxLayout()

        # Horizontal layout for search bar and dropdown
        search_layout = QHBoxLayout()

        self.all_attendees = self.util.마을원전체조회()[1:]
        # Search bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("이름 검색")
        self.search_bar.textChanged.connect(self.filter_attendees)
        search_layout.addWidget(self.search_bar)

        # Dropdown for birth year filtering
        self.birthyear_combo = QComboBox()
        self.birthyear_combo.addItem("없음")  # Initial value
        self.birthyear_combo.addItems(self.get_unique_birth_years())
        self.birthyear_combo.currentIndexChanged.connect(self.filter_attendees)
        search_layout.addWidget(self.birthyear_combo)

        dialog_layout.addLayout(search_layout)

        # Table for attendees
        self.attendees_table = QTableWidget()
        self.attendees_table.setColumnCount(5)
        self.attendees_table.setHorizontalHeaderLabels(["선택", "이름", "생년월일", "성별", "uid"])
        self.attendees_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        dialog_layout.addWidget(self.attendees_table)

        # Populate the table with attendees
        self.all_attendees = self.util.마을원전체조회()[1:]
        self.populate_attendees_table(self.all_attendees)

        # Hide the UID column
        self.attendees_table.setColumnHidden(4, True)

        # Ok and Cancel buttons
        dialog_buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        dialog_buttons.accepted.connect(self.accept)
        dialog_buttons.rejected.connect(self.reject)
        dialog_layout.addWidget(dialog_buttons)

        self.setLayout(dialog_layout)

    def populate_attendees_table(self, attendees):
        self.attendees_table.setRowCount(len(attendees))
        for row, (uid, name, birthdate, gender, phone) in enumerate(attendees):
            checkbox = QCheckBox()
            # Restore the checkbox state if it was previously saved
            if uid in self.checked_state:
                checkbox.setChecked(self.checked_state[uid])
            self.attendees_table.setCellWidget(row, 0, checkbox)
            self.attendees_table.setItem(row, 1, QTableWidgetItem(name))
            self.attendees_table.setItem(row, 2, QTableWidgetItem(str(birthdate)[:2] + "또래"))
            self.attendees_table.setItem(row, 3, QTableWidgetItem(gender))
            self.attendees_table.setItem(row, 4, QTableWidgetItem(str(uid)))

    def filter_attendees(self):
        # Save the current checked state
        self.save_checked_state()

        search_text = self.search_bar.text().lower()
        selected_year = self.birthyear_combo.currentText()

        filtered_attendees = [attendee for attendee in self.all_attendees
                              if (search_text in attendee[1].lower()) and
                              (selected_year == "없음" or str(attendee[2]).startswith(selected_year))]

        self.populate_attendees_table(filtered_attendees)

    def save_checked_state(self):
        """ Save the current state of all checkboxes. """
        self.checked_state = {}
        for row in range(self.attendees_table.rowCount()):
            checkbox = self.attendees_table.cellWidget(row, 0)
            uid = int(self.attendees_table.item(row, 4).text())
            self.checked_state[uid] = checkbox.isChecked()

    def get_unique_birth_years(self):
        years = set()
        for _, _, birthdate, _, _ in self.all_attendees:
            year = str(birthdate)[:2]
            years.add(year)
        return sorted(years)

    def get_selected_attendees(self):
        selected_attendees = []
        for row in range(self.attendees_table.rowCount()):
            checkbox = self.attendees_table.cellWidget(row, 0)
            if checkbox.isChecked():
                uid = int(self.attendees_table.item(row, 4).text())
                selected_attendees.append(uid)
        return selected_attendees


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AttendeesSelectionDialog()
    window.show()
    sys.exit(app.exec_())
