from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QComboBox, QPushButton, QTableWidget,
    QTableWidgetItem, QMessageBox, QHBoxLayout
)
from PyQt5.QtCore import Qt
import sys

from src import util


class ListManager(QDialog):
    def __init__(self, parent=None, members=None):
        super().__init__(parent)
        self.setWindowTitle("명단 관리")
        self.separate_list = []
        self.companion_list = []

        self.util = util.Util()
        # Sample data with tuples (uid, name, age, phone number)
        self.members = []
        for b in self.util.마을원전체조회()[1:]:
            self.members.append((b[0], b[2], b[1], b[3], b[5]))
        self.members = sorted(self.members, key=lambda x: x[1])

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Create a table for displaying separate and companion lists
        self.table = QTableWidget(self)
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["마을원1 ID", "마을원", "마을원2 ID", "마을원", "설정"])
        self.table.setColumnWidth(0, 80)
        self.table.setColumnWidth(1, 120)
        self.table.setColumnWidth(2, 80)
        self.table.setColumnWidth(3, 120)
        self.table.setColumnWidth(4, 120)
        layout.addWidget(self.table)

        # Hide the UID columns
        self.table.hideColumn(0)
        self.table.hideColumn(2)

        # Load initial data
        self.loadListData()

        # Create two dropdown boxes
        dropdown_layout = QHBoxLayout()
        self.member1_dropdown = QComboBox(self)
        self.member2_dropdown = QComboBox(self)

        # Add default values to the dropdown boxes
        self.member1_dropdown.addItem("이름", -1)  # -1 is the default value
        self.member2_dropdown.addItem("이름", -1)

        # Add member names to the dropdown boxes
        for uid, name, _, _, _ in self.members:
            self.member1_dropdown.addItem(name, uid)
            self.member2_dropdown.addItem(name, uid)

        dropdown_layout.addWidget(self.member1_dropdown)
        dropdown_layout.addWidget(self.member2_dropdown)
        layout.addLayout(dropdown_layout)

        # Create button layout
        button_layout = QHBoxLayout()

        # Button to add to the separate list
        add_separate_button = QPushButton("분리 명단에 추가", self)
        add_separate_button.clicked.connect(lambda: self.addToList("분리"))

        # Button to add to the companion list
        add_companion_button = QPushButton("동반 명단에 추가", self)
        add_companion_button.clicked.connect(lambda: self.addToList("동반"))

        # Button to remove from the list
        remove_button = QPushButton("명단에서 삭제", self)
        remove_button.clicked.connect(self.removeSelected)

        # Button to save changes
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
        self.table.setRowCount(0)  # Clear the table
        배치관계 = self.util.배치관계조회()[1:]
        uid_to_name = {person[0]: person for person in self.members}

        # Initialize lists for results
        self.companion_list = []
        self.separate_list = []

        # Iterate over the relationship list and add information to each list
        for uid1, uid2, relation in 배치관계:
            # Find names corresponding to the two UIDs
            person1 = uid_to_name.get(uid1, ("Unknown",))
            person2 = uid_to_name.get(uid2, ("Unknown",))

            # Add to the correct list based on conditions
            if relation == '동반':
                self.companion_list.append((person1, person2))
            elif relation == '분리':
                self.separate_list.append((person1, person2))

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
        item1_uid = QTableWidgetItem(str(pair[0][0]))  # Member 1 UID
        item1_name = QTableWidgetItem(pair[0][1])  # Member 1 Name
        item2_uid = QTableWidgetItem(str(pair[1][0]))  # Member 2 UID
        item2_name = QTableWidgetItem(pair[1][1])  # Member 2 Name
        item_category = QTableWidgetItem(category)  # Category

        # Set the items as non-editable
        for item in [item1_uid, item1_name, item2_uid, item2_name, item_category]:
            item.setFlags(item.flags() ^ Qt.ItemIsEditable)
            item.setTextAlignment(Qt.AlignCenter)  # Center-align the text

        # Set background color based on category
        if category == "분리":
            color = "#FFC8C8"
        else:
            color = "#C8FFC8"

        # Apply color to the category item
        item_category.setBackground(QColor(color))

        self.table.setItem(row_position, 0, item1_uid)
        self.table.setItem(row_position, 1, item1_name)
        self.table.setItem(row_position, 2, item2_uid)
        self.table.setItem(row_position, 3, item2_name)
        self.table.setItem(row_position, 4, item_category)

    def addToList(self, category):
        # Add the selected member pair to the list
        member1_index = self.member1_dropdown.currentIndex()
        member2_index = self.member2_dropdown.currentIndex()

        # Check if the dropdown is still set to the default value
        if self.member1_dropdown.currentData() == -1 or self.member2_dropdown.currentData() == -1:
            QMessageBox.warning(self, "오류", "두 명의 마을원을 모두 선택하세요.")
            return

        # Retrieve member info as tuples
        member1 = self.members[member1_index - 1]  # Adjust index for default item
        member2 = self.members[member2_index - 1]

        # Ensure the same person is not selected twice
        if member1 == member2:
            QMessageBox.warning(self, "오류", "같은 마을원을 두 번 선택할 수 없습니다.")
            return

        # Check for duplicates and add to the appropriate list
        if category == "분리":
            if (member1, member2) in self.separate_list or (member2, member1) in self.separate_list:
                QMessageBox.warning(self, "오류", "이미 분리 명단에 존재합니다.")
                return

            # Do not add if it exists in the companion list
            if (member1, member2) in self.companion_list or (member2, member1) in self.companion_list:
                QMessageBox.warning(self, "오류", "해당 조합은 이미 동반 명단에 존재합니다.")
                return

            self.separate_list.append((member1, member2))
        else:
            if (member1, member2) in self.companion_list or (member2, member1) in self.companion_list:
                QMessageBox.warning(self, "오류", "이미 동반 명단에 존재합니다.")
                return

            # Do not add if it exists in the separate list
            if (member1, member2) in self.separate_list or (member2, member1) in self.separate_list:
                QMessageBox.warning(self, "오류", "해당 조합은 이미 분리 명단에 존재합니다.")
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

        # Process items in reverse order to avoid index issues
        selected_rows = set(item.row() for item in selected_items)

        for row in sorted(selected_rows, reverse=True):
            member1_uid = int(self.table.item(row, 0).text())
            member2_uid = int(self.table.item(row, 2).text())
            category = self.table.item(row, 4).text()

            # Find member tuples by UID
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
        # Save changes (currently just prints to console)
        res = []
        for s in self.separate_list:
            uids = (s[0][0], s[1][0])
            sorted_uids = tuple(sorted(uids))
            res.append((*sorted_uids, '분리'))
        for c in self.companion_list:
            uids = (c[0][0], c[1][0])
            sorted_uids = tuple(sorted(uids))
            res.append((*sorted_uids, '동반'))
        self.util.업데이트_배치관계(res)
        QMessageBox.information(self, "저장 완료", "변경사항이 저장되었습니다.")


def main():
    app = QApplication(sys.argv)

    # Example data
    members = [
        (1, "김철수", "", "", ""),
        (2, "박영희", "", "", ""),
        (3, "이민수", "", "", ""),
        (4, "정하나", "", "", ""),
    ]

    window = ListManager(None, members)
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
