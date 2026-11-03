from dependecies import *
import database
import aerofoilplotter
import simulationPlotter
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Simulation and Aerofoil Plotter")

        layout = QVBoxLayout()


        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("Enter NACA code")
        layout.addWidget(self.input_box)

        self.input_box2=QLineEdit()
        self.input_box2.setPlaceholderText("Enter scale y/nothing for auto")
        layout.addWidget(self.input_box2)

        self.input_box3=QLineEdit()
        self.input_box3.setPlaceholderText("Enter scale x/nothing for auto")
        layout.addWidget(self.input_box3)

        self.input_box4=QLineEdit()
        self.input_box4.setPlaceholderText("Enter AOA")
        layout.addWidget(self.input_box4)

        self.input_box5=QLineEdit()
        self.input_box5.setPlaceholderText("Enter ID")
        layout.addWidget(self.input_box5)

        self.button = QPushButton("Plot Aerofoil")
        self.button.clicked.connect(self.on_button_click)
        layout.addWidget(self.button)

        self.checkbox = QCheckBox("From ID")
        self.checkbox.setTristate(False)  
        self.checkbox.stateChanged.connect(self.on_state_changed)
        layout.addWidget(self.checkbox)

        self.output_label = QLabel("")
        layout.addWidget(self.output_label)

        self.setLayout(layout)

    def on_state_changed(self, state):
        if state == 2:
            self.input_box.setDisabled(True)
            self.input_box2.setDisabled(False)
            self.input_box3.setDisabled(False)
            self.input_box4.setDisabled(True)
            self.input_box5.setDisabled(False)
        elif state == 0:
            self.input_box.setDisabled(False)
            self.input_box2.setDisabled(False)
            self.input_box3.setDisabled(False)
            self.input_box4.setDisabled(False)
            self.input_box5.setDisabled(True)

    def on_button_click(self):
        if self.checkbox.checkState() == 2:
            aerofoil_id=self.input_box5.text()
            connection=sqlite3.connect("flowbench.db")
            cursor=connection.cursor()
            cursor.execute("SELECT NACA FROM aerofoils WHERE id=?", (aerofoil_id,))
            NACA=str(cursor.fetchone()[0])
            cursor.execute("SELECT AOA FROM aerofoils WHERE id=?", (aerofoil_id,))
            AOA=float(cursor.fetchone()[0])
            scaley=(self.input_box2.text())
            scalex=(self.input_box3.text())
            if scalex=="":
                scalex=0
                scalex=float(scalex)
            if scaley=="":
                scaley=0
                scaley=float(scaley)

            p1=multiprocessing.Process(target=aerofoilplotter.plotFoil(NACA,scaley,scalex,AOA))
            

        if self.checkbox.checkState() == 0:
            NACA=self.input_box.text()
            scaley=(self.input_box2.text())
            scalex=(self.input_box3.text())
            AOA=(self.input_box4.text())
            if scalex=="":
                scalex=0
            scalex=float(scalex)
            if scaley=="":
                scaley=0
            scaley=float(scaley)
            if AOA=="":
                AOA=0 
            AOA=float(AOA)
            p1=multiprocessing.Process(target=aerofoilplotter.plotFoil(NACA,scaley,scalex,AOA))

        




class Aerofoil:
    def __init__(self,NACA,AOA):
        self.NACA=NACA
        self.AOA=AOA

    def plotAerofoil(self,scalex,scaley):
        aerofoilplotter.plotFoil(self.NACA,scaley,scalex,self.AOA)

    def saveAerofoil(self,userid):
        database.addAerofoil(userid,self.NACA,self.AOA)


class Simulation:
    def __init__(self,NACA,AOA,velocity,altitude,temperature,fluid,advanced_mode,fluid_viscosity,fluid_density,control_mode):
        self.NACA=NACA
        self.AOA=AOA
        self.speed=velocity
        self.altitude=altitude
        self.advanced_mode=advanced_mode
        if advanced_mode==True:
            self.temperature=temperature
            self.fluid="custom"
            self.fluid_viscosity=fluid_viscosity
            self.fluid_density=fluid_density
            self.control_mode=control_mode
        else:
            if fluid=="air":
                self.fluid="air"
                R=287.05
                P_0=101325
                T_0=288.15
                self.temperature=T_0-0.0065*altitude
                self.fluid_density=1.24062*(0.898411**(altitude/1000))
                self.pressure=self.fluid_density*R*self.temperature
                self.viscosity=1.458e-6*(self.temperature**(3/2))/(self.temperature+110.4)

                

            elif fluid=="water":
                self.fluid="water"
                self.fluid_density=1000
                self.fluid_viscosity=0.001
                R=461.5
                P_0=101325
                T_0=288.15
                self.pressure=9.81*1000*altitude+P_0

        def runSimulation(self):
            simulationPlotter.plotSimulation(self.NACA,self.AOA,self.speed)

        def saveSimulation(self,userid):
            database.addSimulation(userid,self.NACA,self.AOA,self.speed,self.altitude,self.temperature,self.fluid,self.advanced_mode,self.fluid_viscosity,self.fluid_density,self.control_mode)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
