from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QComboBox, QPushButton, QTableWidget,
    QTableWidgetItem, QMessageBox, QHBoxLayout, QWidget
)
from PyQt5.QtCore import Qt


class ListManager(QDialog):
    def __init__(self, parent, separate_list, companion_list, members):
        super().__init__(parent)
        self.setWindowTitle("명단 관리")
        self.separate_list = separate_list
        self.companion_list = companion_list
        self.members = members

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Separate and companion list display table
        self.table = QTableWidget(self)
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["마을원1 ID", "마을원1 이름", "마을원2 ID", "마을원2 이름", "카테고리"])
        self.table.setColumnWidth(0, 80)
        self.table.setColumnWidth(1, 150)
        self.table.setColumnWidth(2, 80)
        self.table.setColumnWidth(3, 150)
        self.table.setColumnWidth(4, 100)
        layout.addWidget(self.table)

        # Load initial data
        self.loadListData()

        # Two dropdown boxes
        dropdown_layout = QHBoxLayout()
        self.member1_dropdown = QComboBox(self)
        self.member2_dropdown = QComboBox(self)

        # Add member names to dropdown boxes
        for uid, name, _, _ in self.members:
            self.member1_dropdown.addItem(name, uid)
            self.member2_dropdown.addItem(name, uid)

        dropdown_layout.addWidget(self.member1_dropdown)
        dropdown_layout.addWidget(self.member2_dropdown)
        layout.addLayout(dropdown_layout)

        # Button layout
        button_layout = QHBoxLayout()

        # Button to add to the separate list
        add_separate_button = QPushButton("분리 명단에 추가", self)
        add_separate_button.clicked.connect(lambda: self.addToList("분리"))

        # Button to add to the companion list
        add_companion_button = QPushButton("동반 명단에 추가", self)
        add_companion_button.clicked.connect(lambda: self.addToList("동반"))

        # Remove button
        remove_button = QPushButton("명단에서 삭제", self)
        remove_button.clicked.connect(self.removeSelected)

        # Save button
        save_button = QPushButton("저장", self)
        save_button.clicked.connect(self.saveChanges)

        button_layout.addWidget(add_separate_button)
        button_layout.addWidget(add_companion_button)
        button_layout.addWidget(remove_button)
        button_layout.addWidget(save_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def loadListData(self):
        # Load data into the table
        self.table.setRowCount(0)  # Reset table

        # Add separate list data
        for pair in self.separate_list:
            self.addRow(pair, "분리")

        # Add companion list data
        for pair in self.companion_list:
            self.addRow(pair, "동반")

    def addRow(self, pair, category):
        # Add a new row to the table
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)

        # Set each item in the row
        self.table.setItem(row_position, 0, QTableWidgetItem(str(pair[0][0])))  # Member 1 UID
        self.table.setItem(row_position, 1, QTableWidgetItem(pair[0][1]))       # Member 1 Name
        self.table.setItem(row_position, 2, QTableWidgetItem(str(pair[1][0])))  # Member 2 UID
        self.table.setItem(row_position, 3, QTableWidgetItem(pair[1][1]))       # Member 2 Name
        self.table.setItem(row_position, 4, QTableWidgetItem(category))         # Category

    def addToList(self, category):
        # Add the selected member pair to the list
        member1_index = self.member1_dropdown.currentIndex()
        member2_index = self.member2_dropdown.currentIndex()

        # Get member information as tuples
        member1 = self.members[member1_index]
        member2 = self.members[member2_index]

        # Ensure the same person is not selected twice
        if member1 == member2:
            QMessageBox.warning(self, "오류", "같은 팀원을 두 번 선택할 수 없습니다.")
            return

        # Check for duplicates and add to the appropriate list
        if category == "분리":
            if (member1, member2) in self.separate_list or (member2, member1) in self.separate_list:
                QMessageBox.warning(self, "오류", "이미 분리 명단에 존재합니다.")
                return
            self.separate_list.append((member1, member2))
        else:
            if (member1, member2) in self.companion_list or (member2, member1) in self.companion_list:
                QMessageBox.warning(self, "오류", "이미 동반 명단에 존재합니다.")
                return
            self.companion_list.append((member1, member2))

        # Add the new pair to the table
        self.addRow((member1, member2), category)

    def removeSelected(self):
        # Remove the selected member pair from the list
        selected_items = self.table.selectedItems()

        if not selected_items:
            QMessageBox.warning(self, "오류", "삭제할 행을 선택하세요.")
            return

        for item in selected_items:
            row = item.row()
            member1_uid = int(self.table.item(row, 0).text())
            member2_uid = int(self.table.item(row, 2).text())
            category = self.table.item(row, 4).text()

            # Find member tuples based on UID
            member1 = next((m for m in self.members if m[0] == member1_uid), None)
            member2 = next((m for m in self.members if m[0] == member2_uid), None)

            if category == "분리":
                if (member1, member2) in self.separate_list:
                    self.separate_list.remove((member1, member2))
                elif (member2, member1) in self.separate_list:
                    self.separate_list.remove((member2, member1))
            elif category == "동반":
                if (member1, member2) in self.companion_list:
                    self.companion_list.remove((member1, member2))
                elif (member2, member1) in self.companion_list:
                    self.companion_list.remove((member2, member1))

            self.table.removeRow(row)

        QMessageBox.information(self, "성공", "선택된 조합이 삭제되었습니다.")

    def saveChanges(self):
        # Save changes (currently prints to console)
        print(f"Updated Separate List: {self.separate_list}")
        print(f"Updated Companion List: {self.companion_list}")
        QMessageBox.information(self, "저장 완료", "변경사항이 저장되었습니다.")
