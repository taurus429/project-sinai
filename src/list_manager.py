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

        # 분리 및 동반 명단 표시 테이블
        self.table = QTableWidget(self)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["마을원1", "마을원2", "카테고리"])
        self.table.setColumnWidth(0, 150)
        self.table.setColumnWidth(1, 150)
        self.table.setColumnWidth(2, 100)
        layout.addWidget(self.table)

        # 초기 데이터 로드
        self.loadListData()

        # 드롭다운 박스 두 개
        dropdown_layout = QHBoxLayout()
        self.member1_dropdown = QComboBox(self)
        self.member2_dropdown = QComboBox(self)

        # 드롭다운 박스에 팀원 이름 추가
        self.member1_dropdown.addItems(self.members)
        self.member2_dropdown.addItems(self.members)

        dropdown_layout.addWidget(self.member1_dropdown)
        dropdown_layout.addWidget(self.member2_dropdown)
        layout.addLayout(dropdown_layout)

        # 버튼 레이아웃
        button_layout = QHBoxLayout()

        # 분리 명단 추가 버튼
        add_separate_button = QPushButton("분리 명단에 추가", self)
        add_separate_button.clicked.connect(lambda: self.addToList("분리"))

        # 동반 명단 추가 버튼
        add_companion_button = QPushButton("동반 명단에 추가", self)
        add_companion_button.clicked.connect(lambda: self.addToList("동반"))

        # 삭제 버튼
        remove_button = QPushButton("명단에서 삭제", self)
        remove_button.clicked.connect(self.removeSelected)

        # 저장 버튼
        save_button = QPushButton("저장", self)
        save_button.clicked.connect(self.saveChanges)

        button_layout.addWidget(add_separate_button)
        button_layout.addWidget(add_companion_button)
        button_layout.addWidget(remove_button)
        button_layout.addWidget(save_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def loadListData(self):
        # 테이블에 데이터 로드
        self.table.setRowCount(0)  # 초기화

        # 분리 명단 데이터 추가
        for pair in self.separate_list:
            self.addRow(pair, "분리")

        # 동반 명단 데이터 추가
        for pair in self.companion_list:
            self.addRow(pair, "동반")

    def addRow(self, pair, category):
        # 테이블에 새 행 추가
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)

        self.table.setItem(row_position, 0, QTableWidgetItem(pair[0]))
        self.table.setItem(row_position, 1, QTableWidgetItem(pair[1]))
        self.table.setItem(row_position, 2, QTableWidgetItem(category))

    def addToList(self, category):
        # 선택된 팀원 조합을 명단에 추가
        member1 = self.member1_dropdown.currentText()
        member2 = self.member2_dropdown.currentText()

        # 같은 사람을 두 번 선택하지 않도록 함
        if member1 == member2:
            QMessageBox.warning(self, "오류", "같은 팀원을 두 번 선택할 수 없습니다.")
            return

        # 중복 체크 및 추가
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

        self.addRow((member1, member2), category)

    def removeSelected(self):
        # 선택된 팀원 조합을 명단에서 삭제
        selected_items = self.table.selectedItems()

        if not selected_items:
            QMessageBox.warning(self, "오류", "삭제할 행을 선택하세요.")
            return

        for item in selected_items:
            row = item.row()
            member1 = self.table.item(row, 0).text()
            member2 = self.table.item(row, 1).text()
            category = self.table.item(row, 2).text()

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
        # 변경사항 저장 (현재는 콘솔에 출력)
        print(f"Updated Separate List: {self.separate_list}")
        print(f"Updated Companion List: {self.companion_list}")
        QMessageBox.information(self, "저장 완료", "변경사항이 저장되었습니다.")
