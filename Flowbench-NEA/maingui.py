import aerofoilplotter
from dependecies import *

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Aerofoil plotter")

        # Layout
        layout = QVBoxLayout()

        # Input field
        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("Enter NACA code")
        layout.addWidget(self.input_box)

        self.input_box2=QLineEdit()
        self.input_box2.setPlaceholderText("Enter scale or 0")
        layout.addWidget(self.input_box2)

        # Button
        self.button = QPushButton("Submit")
        self.button.clicked.connect(self.on_button_click)
        layout.addWidget(self.button)

        # Output label
        self.output_label = QLabel("")
        layout.addWidget(self.output_label)

        self.setLayout(layout)

    def on_button_click(self):
        user_text = self.input_box.text()
        scale=(self.input_box2.text())
        if scale=="":
            scale=0
        scale=float(scale)

        p1=multiprocessing.Process(target=aerofoilplotter.plotFoil(user_text,scale))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
