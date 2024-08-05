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
        self.members = members if members is not None else []
        self.util = util.Util()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # 분리 및 동반 명단을 표시하는 테이블 생성
        self.table = QTableWidget(self)
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["마을원1 ID", "마을원", "마을원2 ID", "마을원", "설정"])
        self.table.setColumnWidth(0, 80)
        self.table.setColumnWidth(1, 120)
        self.table.setColumnWidth(2, 80)
        self.table.setColumnWidth(3, 120)
        self.table.setColumnWidth(4, 120)
        layout.addWidget(self.table)

        # UID 컬럼 숨기기
        self.table.hideColumn(0)
        self.table.hideColumn(2)

        # 초기 데이터 로드
        self.loadListData()

        # 두 개의 드롭다운 박스 생성
        dropdown_layout = QHBoxLayout()
        self.member1_dropdown = QComboBox(self)
        self.member2_dropdown = QComboBox(self)

        # 드롭다운 박스에 기본값 추가
        self.member1_dropdown.addItem("이름", -1)  # -1은 기본값 데이터
        self.member2_dropdown.addItem("이름", -1)

        # 드롭다운 박스에 회원 이름 추가
        for uid, name, _, _, _ in self.members:
            self.member1_dropdown.addItem(name, uid)
            self.member2_dropdown.addItem(name, uid)

        dropdown_layout.addWidget(self.member1_dropdown)
        dropdown_layout.addWidget(self.member2_dropdown)
        layout.addLayout(dropdown_layout)

        # 버튼 레이아웃 생성
        button_layout = QHBoxLayout()

        # 분리 명단에 추가 버튼
        add_separate_button = QPushButton("분리 명단에 추가", self)
        add_separate_button.clicked.connect(lambda: self.addToList("분리"))

        # 동반 명단에 추가 버튼
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
        self.table.setRowCount(0)  # 테이블 초기화
        배치관계 = self.util.배치관계조회()[1:]
        uid_to_name = {person[0]: person for person in self.members}

        # 결과를 저장할 리스트 초기화
        companion_list = []
        separate_list = []

        # 관계 리스트를 순회하며 필요한 정보를 각 리스트에 추가
        for uid1, uid2, relation in 배치관계:
            # 두 uid에 해당하는 이름을 찾음
            person1 = uid_to_name.get(uid1, "Unknown")
            person2 = uid_to_name.get(uid2, "Unknown")

            # 조건에 따라 올바른 리스트에 추가
            if relation == '동반':
                self.companion_list.append((person1, person2))
            elif relation == '분리':
                self.separate_list.append((person1, person2))


        # 분리 명단 데이터 추가
        for pair in self.separate_list:
            self.addRow(pair, "분리")

        # 동반 명단 데이터 추가
        for pair in self.companion_list:
            self.addRow(pair, "동반")

    def addRow(self, pair, category):
        # 테이블에 새로운 행 추가
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)

        # 행의 각 항목 설정
        self.table.setItem(row_position, 0, QTableWidgetItem(str(pair[0][0])))  # 회원 1 UID
        self.table.setItem(row_position, 1, QTableWidgetItem(pair[0][1]))  # 회원 1 이름
        self.table.setItem(row_position, 2, QTableWidgetItem(str(pair[1][0])))  # 회원 2 UID
        self.table.setItem(row_position, 3, QTableWidgetItem(pair[1][1]))  # 회원 2 이름
        self.table.setItem(row_position, 4, QTableWidgetItem(category))  # 카테고리

    def addToList(self, category):
        # 선택된 회원 쌍을 목록에 추가
        member1_index = self.member1_dropdown.currentIndex()
        member2_index = self.member2_dropdown.currentIndex()

        # 드롭다운이 여전히 기본값으로 설정되어 있는지 확인
        if self.member1_dropdown.currentData() == -1 or self.member2_dropdown.currentData() == -1:
            QMessageBox.warning(self, "오류", "두 명의 마을원을 모두 선택하세요.")
            return

        # 회원 정보를 튜플로 가져오기
        member1 = self.members[member1_index - 1]  # 기본 항목을 위한 인덱스 조정
        member2 = self.members[member2_index - 1]

        # 같은 사람을 두 번 선택하지 않도록 확인
        if member1 == member2:
            QMessageBox.warning(self, "오류", "같은 마을원을 두 번 선택할 수 없습니다.")
            return

        # 중복 확인 및 적절한 목록에 추가
        if category == "분리":
            if (member1, member2) in self.separate_list or (member2, member1) in self.separate_list:
                QMessageBox.warning(self, "오류", "이미 분리 명단에 존재합니다.")
                return

            # 동반 명단에 있는 경우 분리 명단에 추가하지 않음
            if (member1, member2) in self.companion_list or (member2, member1) in self.companion_list:
                QMessageBox.warning(self, "오류", "해당 조합은 이미 동반 명단에 존재합니다.")
                return

            self.separate_list.append((member1, member2))
        else:
            if (member1, member2) in self.companion_list or (member2, member1) in self.companion_list:
                QMessageBox.warning(self, "오류", "이미 동반 명단에 존재합니다.")
                return

            # 분리 명단에 있는 경우 동반 명단에 추가하지 않음
            if (member1, member2) in self.separate_list or (member2, member1) in self.separate_list:
                QMessageBox.warning(self, "오류", "해당 조합은 이미 분리 명단에 존재합니다.")
                return

            self.companion_list.append((member1, member2))

        # 테이블에 새로운 쌍 추가
        self.addRow((member1, member2), category)

    def removeSelected(self):
        # 선택된 회원 쌍을 목록에서 삭제
        selected_items = self.table.selectedItems()

        if not selected_items:
            QMessageBox.warning(self, "오류", "삭제할 행을 선택하세요.")
            return

        # 행 인덱스를 기준으로 항목을 삭제하므로 역순으로 처리해야 함
        # 이렇게 하면 항목을 삭제할 때 다른 항목의 인덱스가 엉키지 않음
        selected_rows = set(item.row() for item in selected_items)

        for row in sorted(selected_rows, reverse=True):
            member1_uid = int(self.table.item(row, 0).text())
            member2_uid = int(self.table.item(row, 2).text())
            category = self.table.item(row, 4).text()

            # UID를 기준으로 회원 튜플 찾기
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
        # 변경사항 저장 (현재는 콘솔에 출력)
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

    # 예제 데이터
    separate_list = [((1, "김철수"), (2, "박영희"))]
    companion_list = [((3, "이민수"), (4, "정하나"))]
    members = [
        (1, "김철수", "", "", ""),
        (2, "박영희", "", "", ""),
        (3, "이민수", "", "", ""),
        (4, "정하나", "", "", ""),
    ]

    window = ListManager(None, separate_list, companion_list, members)
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
