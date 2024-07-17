import sys
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QDateTimeEdit, QComboBox, QLineEdit, QPushButton, QDialogButtonBox, QTableWidget, QTableWidgetItem, QHeaderView, QCheckBox, QApplication
from PyQt5.QtCore import Qt, QDateTime
from PyQt5.QtGui import QColor, QStandardItem, QStandardItemModel
import util

class AddMeetingWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("신규 모임 등록")
        self.util = util.Util()

        # Layout
        layout = QVBoxLayout()

        # DateTime input
        self.datetime_label = QLabel("날짜 및 시간:")
        self.datetime_edit = QDateTimeEdit(calendarPopup=True)
        self.datetime_edit.setDateTime(QDateTime.currentDateTime())
        self.datetime_edit.setDisplayFormat("yyyy-MM-dd HH:00")
        layout.addWidget(self.datetime_label)
        layout.addWidget(self.datetime_edit)

        # Meeting type input
        self.meeting_type_label = QLabel("모임 구분:")
        self.meeting_type_combo = QComboBox()

        # Using QStandardItemModel to set colors
        model = QStandardItemModel()
        res = self.util.모임코드조회()[0]
        items = list()
        for r in res.values():
            items.append(r)
        for uid, text, color in items:
            item = QStandardItem(text)
            item.setForeground(QColor(color))
            model.appendRow(item)

        self.meeting_type_combo.setModel(model)
        layout.addWidget(self.meeting_type_label)
        layout.addWidget(self.meeting_type_combo)

        # Description input
        self.desc_label = QLabel("상세 설명:")
        self.desc_input = QLineEdit()
        layout.addWidget(self.desc_label)
        layout.addWidget(self.desc_input)

        # Attendees selection button
        self.select_attendees_button = QPushButton("참석 인원 선택")
        self.select_attendees_button.clicked.connect(self.select_attendees)
        layout.addWidget(self.select_attendees_button)

        # Label to show the number of selected attendees
        self.selected_attendees_label = QLabel("0명 선택됨")
        layout.addWidget(self.selected_attendees_label)

        # Save button
        self.save_button = QPushButton("저장")
        layout.addWidget(self.save_button)

        # Set layout
        self.setLayout(layout)

        # Store selected attendees
        self.selected_attendees = []

    def select_attendees(self):
        # Create a new dialog for selecting attendees
        self.attendees_dialog = QDialog(self)
        self.attendees_dialog.setWindowTitle("참석 인원 선택")
        dialog_layout = QVBoxLayout()

        # Search bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("이름 검색")
        self.search_bar.textChanged.connect(self.filter_attendees)
        dialog_layout.addWidget(self.search_bar)

        # Table for attendees
        self.attendees_table = QTableWidget()
        self.attendees_table.setColumnCount(5)
        self.attendees_table.setHorizontalHeaderLabels(["선택", "이름", "생년월일", "성별", "uid"])
        self.attendees_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        dialog_layout.addWidget(self.attendees_table)

        마을원 = self.util.마을원전체조회()
        # Sample attendees list (name, birthdate, gender)
        self.all_attendees = 마을원[1:]

        # Populate the table with all attendees
        self.populate_attendees_table(self.all_attendees)

        # Hide the UID column (column index 4)
        self.attendees_table.setColumnHidden(4, True)

        # Ok and Cancel buttons
        dialog_buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        dialog_buttons.accepted.connect(self.attendees_dialog.accept)
        dialog_buttons.rejected.connect(self.attendees_dialog.reject)
        dialog_layout.addWidget(dialog_buttons)

        self.attendees_dialog.setLayout(dialog_layout)

        # Show the dialog and store the selected attendees
        if self.attendees_dialog.exec_() == QDialog.Accepted:
            self.selected_attendees = []
            for row in range(self.attendees_table.rowCount()):
                checkbox = self.attendees_table.cellWidget(row, 0)
                if checkbox.isChecked():
                    uid = int(self.attendees_table.item(row, 4).text())
                    self.selected_attendees.append(uid)
            selected_count = len(self.selected_attendees)
            self.selected_attendees_label.setText(f"{selected_count}명 선택됨")

    def populate_attendees_table(self, attendees):
        self.attendees_table.setRowCount(len(attendees))
        for row, (uid, name, birthdate, gender, phone) in enumerate(attendees):
            checkbox = QCheckBox()
            if uid in self.selected_attendees:
                checkbox.setChecked(True)
            self.attendees_table.setCellWidget(row, 0, checkbox)
            self.attendees_table.setItem(row, 1, QTableWidgetItem(name))
            self.attendees_table.setItem(row, 2, QTableWidgetItem(str(birthdate)[:2]+"또래"))
            self.attendees_table.setItem(row, 3, QTableWidgetItem(gender))
            self.attendees_table.setItem(row, 4, QTableWidgetItem(str(uid)))

    def filter_attendees(self):
        search_text = self.search_bar.text().lower()
        filtered_attendees = [attendee for attendee in self.all_attendees if search_text in attendee[1].lower()]
        self.populate_attendees_table(filtered_attendees)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AddMeetingWindow()
    window.show()
    sys.exit(app.exec_())
