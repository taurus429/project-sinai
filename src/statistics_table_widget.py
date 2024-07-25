import sys
import util
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView, QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor  # Import QColor for color manipulation

class StatisticsTableWidget(QTableWidget):
    def __init__(self, 마을원_uid, util, parent=None):
        super().__init__(parent)

        # 통계 데이터 가져오기
        self.statis = util.참석통계(마을원_uid)[1:]
        print(self.statis)
        code, _ = util.모임코드조회()
        stats = []
        for s in self.statis:
            if len(s) == 2:
                stats.append((code[s[0][0]][1], f"{s[0][1]}회", f"{s[0][2]}위", f"{round(s[1][0])}%", f"{s[1][1]}위"))

        # 테이블 초기 설정
        self.setColumnCount(5)  # 통계를 위한 5개의 열 설정
        self.setHorizontalHeaderLabels(["모임", "참석횟수", "순위", "출석률", "순위"])  # 열 헤더 설정

        # Adjust the width of the "모임" column (first column)
        self.setColumnWidth(0, 100)  # Set width to 150 pixels

        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)  # Second column stretching
        self.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)  # Third column stretching
        self.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)  # Fourth column stretching
        self.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)  # Fifth column stretching

        # 왼쪽의 index 숨기기
        self.verticalHeader().setVisible(False)  # 인덱스가 보이지 않도록 설정

        # Set header background color
        self.horizontalHeader().setStyleSheet("QHeaderView::section { background-color: #f0f0f0; }")

        self.populate_stats_table(stats)  # 통계 테이블 채우기

    def populate_stats_table(self, stats):
        self.setRowCount(len(stats))  # 행의 수를 설정합니다
        for row, (모임, 참석횟수, 순위1, 출석률, 순위2) in enumerate(stats):
            # Create items for each column
            모임_item = self.create_non_editable_item(모임)
            참석횟수_item = self.create_non_editable_item(참석횟수)
            순위1_item = self.create_non_editable_item(순위1)
            출석률_item = self.create_non_editable_item(출석률)
            순위2_item = self.create_non_editable_item(순위2)

            # Extract numeric rank from "N위"
            rank_number = int(출석률.replace("%", ""))

            # Get color based on rank
            color = self.get_color_based_on_rank(rank_number)

            # Set background color for the entire row
            모임_item.setBackground(color)
            참석횟수_item.setBackground(color)
            순위1_item.setBackground(color)
            출석률_item.setBackground(color)
            순위2_item.setBackground(color)

            # Add items to the table
            self.setItem(row, 0, 모임_item)
            self.setItem(row, 1, 참석횟수_item)
            self.setItem(row, 2, 순위1_item)
            self.setItem(row, 3, 출석률_item)
            self.setItem(row, 4, 순위2_item)

    def create_non_editable_item(self, text):
        item = QTableWidgetItem(text)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # Make the item non-editable
        item.setTextAlignment(Qt.AlignCenter)  # Center-align the text
        return item

    def get_color_based_on_rank(self, rank):
        """Calculate the color based on the rank. 1위 is green, 70위 is pink."""
        # Define start and end colors
        start_color = QColor(204, 255, 204)  # Light green (#ccffcc)
        end_color = QColor(255, 204, 204)    # Light pink (#ffcccc)

        # Normalize the rank to a 0-1 range
        min_rank = 100
        max_rank = 0
        normalized_rank = (rank - min_rank) / (max_rank - min_rank)

        # Calculate the interpolated color
        red = start_color.red() + (end_color.red() - start_color.red()) * normalized_rank
        green = start_color.green() + (end_color.green() - start_color.green()) * normalized_rank
        blue = start_color.blue() + (end_color.blue() - start_color.blue()) * normalized_rank

        return QColor(int(red), int(green), int(blue))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    util = util.Util()
    window = StatisticsTableWidget(21, util)
    window.show()
    sys.exit(app.exec_())
