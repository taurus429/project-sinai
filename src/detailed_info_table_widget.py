# detailed_info_table_widget.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem


class DetailedInfoTableWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Layout for the detailed info table
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Create a QTableWidget for detailed info
        self.table = QTableWidget()
        self.table.setColumnCount(4)  # 4 columns
        self.table.setHorizontalHeaderLabels(["컬럼명1", "데이터1", "컬럼명2", "데이터2"])
        self.table.horizontalHeader().setStretchLastSection(True)

        # Set header background color
        self.table.horizontalHeader().setStyleSheet("QHeaderView::section { background-color: #f0f0f0; }")

        # Hide row and column headers
        self.table.verticalHeader().setVisible(False)

        layout.addWidget(self.table)
        self.setLayout(layout)

        # Populate table with data
        self.populate_table()

    def populate_table(self):
        data = [
            ("Name", "John Doe", "Age", "30"),
            ("Address", "1234 Main St", "Phone", "123-456-7890")
        ]

        self.table.setRowCount(len(data))
        for row_index, (col1, val1, col2, val2) in enumerate(data):
            self.table.setItem(row_index, 0, QTableWidgetItem(col1))
            self.table.setItem(row_index, 1, QTableWidgetItem(val1))
            self.table.setItem(row_index, 2, QTableWidgetItem(col2))
            self.table.setItem(row_index, 3, QTableWidgetItem(val2))
