import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QApplication
import matplotlib


class SpiderChartWidget(QWidget):
    def __init__(self, data, labels, parent=None):
        super().__init__(parent)

        # Path to your local font file
        font_path = '../asset/font/감탄로드바탕체 Regular.ttf'

        # Add the font to matplotlib
        font_prop = matplotlib.font_manager.FontProperties(fname=font_path)
        matplotlib.rcParams['font.family'] = font_prop.get_name()

        # Ensure that minus signs are correctly displayed
        matplotlib.rcParams['axes.unicode_minus'] = False

        # Create a matplotlib figure and axis
        self.figure, self.ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

        # Create the radar chart
        self.plot_spider_chart(data, labels)

        # Create a canvas to display the plot
        self.canvas = FigureCanvas(self.figure)

        # Create a layout and add the canvas to the layout
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def plot_spider_chart(self, data, labels):
        # Number of variables
        num_vars = len(labels)

        # Compute angle for each axis
        angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

        # Make the plot circular by appending the start value to the end
        data += data[:1]
        angles += angles[:1]

        # Draw the radar chart
        self.ax.fill(angles, data, color='blue', alpha=0.25)
        self.ax.plot(angles, data, color='blue', linewidth=2)

        # Set the labels for each axis
        self.ax.set_yticklabels([])
        self.ax.set_xticks(angles[:-1])
        self.ax.set_xticklabels(labels)

        # Adjust the plot to fit within the layout
        self.ax.set_ylim(0, 100)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Example data and labels
    data = [4, 30, 2, 50, 100]  # Example values for the radar chart
    labels = ['대예배', '더원', '자체예배', '금철', '소울']

    widget = SpiderChartWidget(data, labels)
    widget.setWindowTitle("Spider Chart Example")
    widget.resize(320, 240)
    widget.show()

    sys.exit(app.exec_())
