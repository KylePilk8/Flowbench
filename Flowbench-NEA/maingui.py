from dependecies import *
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        screen: QScreen=app.primaryScreen()
        size=screen.size()
        width=size.width()
        height=size.height()
        self.setWindowTitle("Test")
        
        button=QPushButton("Press")
        button.setCheckable(True)
        button.clicked.connect(self.wasclicked)

        
        self.setFixedSize(width,height)
        self.setCentralWidget(button)
        
    def wasclicked(self):
        return 1
        

app = QApplication(sys.argv)
window = MainWindow()

window.show()
app.exec()