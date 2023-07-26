import numpy as np
import pandas as pd
import serial as ser
import os

class MData():
    def __init__(self) -> None:
        self.sd = None # serial device object
        self.data = None
        self.filepath= None
        self.mdata = None
        tzero = str(0.0)
        self.field = {'x':tzero, 'y':tzero, 'z':tzero, 'Bx':tzero, 'By':tzero, 'Bz':tzero, 'Bmod':tzero }
        
    def readsd(self):
        tdata = ""
        if self.sd is None:
            return(str(np.random.randint(99)))
        while True: 
            achar = self.sd.read()
            achar = achar.decode('utf-8')
            # print(achar)
            if achar =='\r' or achar ==',':
                return tdata 
            tdata += str(achar)
                        
    def writesd(self,msg):
        try:
            self.sd.flushInput()
            self.sd.flushOutput()
            self.sd.write(msg)
            msg = 'written'
        except:
            msg = 'could not write to serial device'
        
        return(msg)
    
    def connectdev(self, devname):
        print(devname)
        try:
            self.sd = ser.Serial(devname, baudrate=9600, bytesize=ser.SEVENBITS, parity=ser.PARITY_ODD, stopbits=ser.STOPBITS_ONE, timeout=0.1)
            msg = "connected to " + devname
        except:
            msg = "did not connect"
        return(msg)
    
    def setunits(self,units):
        if units == "Gauss":
            msg = self.writesd(b"UNIT G\r")
        else:
            msg = self.writesd(b"UNIT T\r")
        return(msg)
    
    def setrange(self,range):
        if range == "30000":
            print("setting range 30000")
            msg = self.writesd(b"RANGE 0\r")
        elif range == "3000":
            msg = self.writesd(b"RANGE 1\r")
        elif range == "300":
            msg = self.writesd(b"RANGE 2\r")
        else:
            msg = self.writesd(b"RANGE 3\r")
        return(msg)
    
    def readalldata(self):
        msg = self.writesd(b"ALLF?\r")
        self.field['Bx'] = self.readsd()
        self.field['By'] = self.readsd()
        self.field['Bz'] = self.readsd()
        self.field['Bmod'] = self.readsd()
        return(msg)
    
    def getrandomdata(self,num):
        tdata = np.random.random(num)
        xaxis = np.arange(num)
        return(tdata)
    
    def getfielddata(self,axis = 'all', field = 'Bmod'):
        df = pd.read_csv(self.filepath, header=None, skiprows=2)
        df.columns = ['x','y','z','Bx','By','Bz','Bmod']
        if axis == 'all':
            x = df['x'].to_numpy()
            y = df['y'].to_numpy()
            z = df['z'].to_numpy()
            Bmod = df['Bmod'].to_numpy()
            return(x,y,z,Bmod)
        else:
            axis = df[axis].to_numpy()
            field = df[field].to_numpy()
            return(axis,field)
    
