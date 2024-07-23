# statistics_table_widget.py
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView


class StatisticsTableWidget(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # 테이블 초기 설정
        self.setColumnCount(3)  # 통계를 위한 세 개의 열 설정
        self.setHorizontalHeaderLabels(["통계 항목", "값", "설명"])  # 열 헤더 설정
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 열 크기 조정

        # 왼쪽의 index 숨기기
        self.verticalHeader().setVisible(False)  # 인덱스가 보이지 않도록 설정

        self.populate_stats_table()  # 통계 테이블 채우기

    def populate_stats_table(self):
        """ 통계 테이블에 데이터를 채워 넣습니다. """
        stats = [
            ("참석 수", "10", "총 참석 횟수"),
            ("지각 횟수", "2", "총 지각 횟수"),
            ("결석 횟수", "1", "총 결석 횟수")
        ]
        self.setRowCount(len(stats))  # 행의 수를 설정합니다
        for row, (item, value, desc) in enumerate(stats):
            self.setItem(row, 0, QTableWidgetItem(item))  # 통계 항목
            self.setItem(row, 1, QTableWidgetItem(value))  # 값
            self.setItem(row, 2, QTableWidgetItem(desc))  # 설명

