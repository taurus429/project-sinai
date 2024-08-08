import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QProgressBar
from PyQt5.QtGui import QColor

class ProgressBarExample(QWidget):
    def __init__(self):
        super().__init__()

        # Create a QVBoxLayout
        layout = QVBoxLayout()

        # Create a QProgressBar
        self.progressBar = QProgressBar(self)

        # Set the value of the progress bar to 80%
        self.progressBar.setValue(10)

        # Remove the animation effect by setting the text visible property
        self.progressBar.setTextVisible(False)

        # Set custom styles for the progress bar
        self.updateProgressBarColor()

        # Add the progress bar to the layout
        layout.addWidget(self.progressBar)

        # Set the layout for the main window
        self.setLayout(layout)

        # Set the title and size of the main window
        self.setWindowTitle('Progress Bar Example')
        self.resize(300, 100)

    def updateProgressBarColor(self):
        # Define start and end colors
        start_color = QColor(204, 255, 204)  # Light green
        end_color = QColor(255, 204, 204)    # Light pink

        # Get the value of the progress bar
        value = self.progressBar.value()

        # Normalize the value to a 0-1 range
        min_value = 0
        max_value = 100
        normalized_value = (value - min_value) / (max_value - min_value)

        # Calculate the interpolated color
        red = int(start_color.red() + (end_color.red() - start_color.red()) * normalized_value)
        green = int(start_color.green() + (end_color.green() - start_color.green()) * normalized_value)
        blue = int(start_color.blue() + (end_color.blue() - start_color.blue()) * normalized_value)

        # Create the color in hex format
        color = QColor(red, green, blue).name()

        # Set the style sheet to change the progress bar color
        self.progressBar.setStyleSheet(f"""
            QProgressBar {{
                border: 2px solid #555555;
                border-radius: 5px;
                text-align: center;
            }}
            QProgressBar::chunk {{
                background: {color};
                width: 20px; /* Set the chunk width */
            }}
        """)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ProgressBarExample()
    window.show()
    sys.exit(app.exec_())
