# add_meeting_window.py
import sys
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QDateTimeEdit, QComboBox, QLineEdit, QPushButton, QApplication
from PyQt5.QtGui import QColor, QStandardItem, QStandardItemModel
from PyQt5.QtCore import QDateTime
import util
from attendees_selection_dialog import AttendeesSelectionDialog

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
        for uid, text, bg_color, ft_color in items:
            item = QStandardItem(text)
            item.setForeground(QColor(bg_color))
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
        self.select_attendees_button.clicked.connect(self.open_attendees_dialog)
        layout.addWidget(self.select_attendees_button)

        # Label to show the number of selected attendees
        self.selected_attendees_label = QLabel("0명 선택됨")
        layout.addWidget(self.selected_attendees_label)

        # Save button
        self.save_button = QPushButton("저장")
        layout.addWidget(self.save_button)

        # Set layout
        self.setLayout(layout)

    def open_attendees_dialog(self):
        dialog = AttendeesSelectionDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            selected_attendees = dialog.get_selected_attendees()
            selected_count = len(selected_attendees)
            self.selected_attendees_label.setText(f"{selected_count}명 선택됨")
            # You can use `selected_attendees` as needed

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AddMeetingWindow()
    window.show()
    sys.exit(app.exec_())
