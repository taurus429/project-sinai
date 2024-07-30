import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QLabel, QMainWindow


# A Widget
class AWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Label to show current data
        self.label = QLabel("Current Data: None", self)
        layout.addWidget(self.label)

        # Button to simulate data change
        self.change_data_btn = QPushButton("Change Data", self)
        layout.addWidget(self.change_data_btn)

        self.setLayout(layout)
        self.setWindowTitle("A Widget")

    def change_data(self):
        # Simulate data change
        new_data = "New Data"
        self.label.setText(f"Current Data: {new_data}")

        # Return new data to be used by B widget
        return new_data


# B Widget
class BWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Table widget to show data
        self.table = QTableWidget(1, 1, self)
        self.table.setItem(0, 0, QTableWidgetItem("No Data"))
        layout.addWidget(self.table)

        self.setLayout(layout)
        self.setWindowTitle("B Widget")

    def update_data(self, data):
        # Update the table with the new data
        self.table.setItem(0, 0, QTableWidgetItem(data))


# Main Window
class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Create buttons to open A and B widgets
        self.open_a_widget_btn = QPushButton("Open A Widget", self)
        self.open_a_widget_btn.clicked.connect(self.open_a_widget)

        self.open_b_widget_btn = QPushButton("Open B Widget", self)
        self.open_b_widget_btn.clicked.connect(self.open_b_widget)

        # Add buttons to layout
        layout.addWidget(self.open_a_widget_btn)
        layout.addWidget(self.open_b_widget_btn)

        # Create a central widget and set the layout
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.a_widget = None
        self.b_widget = None

        self.setWindowTitle('Main Window')
        self.setGeometry(100, 100, 300, 200)
        self.show()

    def open_a_widget(self):
        if self.a_widget is None:
            self.a_widget = AWidget()

            # Connect button click to a lambda function
            self.a_widget.change_data_btn.clicked.connect(lambda: self.handle_change_data())

            self.a_widget.show()
        else:
            self.a_widget.activateWindow()
            self.a_widget.raise_()

    def open_b_widget(self):
        if self.b_widget is None:
            self.b_widget = BWidget()
            self.b_widget.show()
        else:
            self.b_widget.activateWindow()
            self.b_widget.raise_()

    def handle_change_data(self):
        # Call AWidget's change_data method
        if self.a_widget is not None:
            new_data = self.a_widget.change_data()

            # Directly call BWidget's update_data method
            if self.b_widget is not None:
                self.b_widget.update_data(new_data)


# Main execution
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())
