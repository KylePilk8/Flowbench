from dependecies import *

def createDatabase():
    conn = sqlite3.connect('aerofoils.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                      (Userid INTEGER PRIMARY KEY AUTOINCREMENT,
                      Username TEXT NOT NULL,
                      Password TEXT NOT NULL,
                      Type TEXT NOT NULL,
                      Comments TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS aerofoils
                      (AerofoilID INTEGER PRIMARY KEY AUTOINCREMENT,
                      Userid INTEGER NOT NULL,
                      NACAcode TEXT NOT NULL,
                      alpha REAL NOT NULL,
                        FOREIGN KEY(Userid) REFERENCES users(Userid))''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS simulations
                      (SimulationID INTEGER PRIMARY KEY AUTOINCREMENT,
                        AerofoilID INTEGER NOT NULL,
                        Speed REAL NOT NULL,
                        Fluid TEXT NOT NULL,
                        Temperature REAL NOT NULL,
                        Altitude REAL NOT NULL,
                        AdvancedMode Boolean NOT NULL,
                        Fluidviscosity REAL NOT NULL,
                        Fluiddensity REAL NOT NULL,
                        Controlmode Boolean NOT NULL,
                        FOREIGN KEY(AerofoilID) REFERENCES aerofoils(AerofoilID))''')
    conn.commit()
    conn.close()

def addUser(username,password):
    password = hashPassword(password)
    if not username.isText() or not password.isText():
        return("Data type error")
        breakpoint
    conn = sqlite3.connect('aerofoils.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (Username, Password, Type) VALUES (?, ?, ?)", (username, password, "user"))
    conn.commit()
    conn.close()

def hashPassword(password):
    password=list(password)
    hashkey = 0
    hashkey2 = 0
    hashed_password = [''] * 20
    length=len(password)
    remaining=20-length
    for i in range(0,length):
        hashkey=abs(hashkey+((-1)**i * (ord(password[i])/length)))
    if hashkey==0:
        hashkey=1
  
    for i in range(0,remaining):
        hashkey2=abs(hashkey+((-1)**i * (ord(password[i])/length)))
    if hashkey2==0:
        hashkey2=1
    
    for i in range(0,length):
        hashed_password[i]=chr(int(161+(ord(password[i])*hashkey*(i+1))%128))
    for i in range(0,remaining):
        hashed_password[19-i]=chr(int(161+(ord(password[i])*hashkey2*(i+1))%128))
    
    while len(hashed_password) < 20:
          hashed_password.append(0)

    return ''.join(hashed_password)


def addAerofoil(userid, naca_code, alpha):
    if not userid.isInt() or not naca_code.isText() or not alpha.isFloat():
        return("Data type error")
        breakpoint
    conn = sqlite3.connect('aerofoils.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO aerofoils (Userid, NACAcode, alpha) VALUES (?, ?, ?)", (userid, naca_code, alpha))
    conn.commit()
    conn.close()

def addSimulation(aerofoil_id, speed, fluid, temperature, altitude, advanced_mode, fluid_viscosity, fluid_density, control_mode):
    if not aerofoil_id.isInt() or not speed.isFloat() or not fluid.isText() or not temperature.isFloat() or not altitude.isFloat() or not advanced_mode.isBoolean() or not fluid_viscosity.isFloat() or not fluid_density.isFloat() or not control_mode.isBoolean():
        return("Data type error")
        breakpoint
    conn = sqlite3.connect('aerofoils.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO simulations (AerofoilID, Speed, Fluid, Temperature, Altitude, AdvancedMode, Fluidviscosity, Fluiddensity, Controlmode) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                   (aerofoil_id, speed, fluid, temperature, altitude, advanced_mode, fluid_viscosity, fluid_density, control_mode))
    conn.commit()
    conn.close()

def deleteUser(userid):
    conn = sqlite3.connect('aerofoils.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE Userid = ?", (userid,))
    conn.commit()
    conn.close()

def deleteAerofoil(aerofoil_id):
    conn = sqlite3.connect('aerofoils.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM aerofoils WHERE AerofoilID = ?", (aerofoil_id,))
    conn.commit()
    conn.close()

def deleteSimulation(simulation_id):
    conn = sqlite3.connect('aerofoils.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM simulations WHERE SimulationID = ?", (simulation_id,))
    conn.commit()
    conn.close()


