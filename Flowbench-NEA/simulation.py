from dependecies import *
import database
import aerofoilplotter
import simulationPlotter

class Aerofoil:
    def __init__(self,NACA,AOA):
        self.NACA=NACA
        self.AOA=AOA

    def plotAerofoil(self,scalex,scaley):
        aerofoilplotter.plotFoil(self.NACA,scaley,self.AOA,scalex)

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




id=input("Enter aerofoil ID: ")
conn = sqlite3.connect('aerofoils.db')
cursor = conn.cursor()
NACAcode = cursor.execute("SELECT NACAcode FROM aerofoils WHERE AerofoilID=?", (id,))
AOA = cursor.execute("SELECT alpha FROM aerofoils WHERE AerofoilID=?", (id,))
NACAcode = NACAcode.fetchone()[0]
AOA = AOA.fetchone()[0]
cursor.close()
conn.close()

aerofoil=Aerofoil(NACAcode, AOA)
aerofoil.plotAerofoil(0,0)
