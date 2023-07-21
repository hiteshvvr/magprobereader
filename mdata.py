import numpy as np
import pandas as pd
import serial as ser

class MData():
    def __init__(self) -> None:
        self.sd = None # serial device object
        self.data = None
        self.foldname = None
        self.filename = None
        self.mdata = None
        
    def readsd(self):
        tdata = ""
        while True: 
            achar = self.sd.read()
            if achar =='\r' or achar ==',':
                return tdata 
            tdata += achar
                        
    def writesd(self,msg):
        try:
            self.sd.flushInput()
            self.sd.flushOutput()
            self.sd.write(msg)
            msg = 'written'
        except:
            msg = 'could not write'
        
        return(msg)
    
    def connectdev(self, devname):
        try:
            self.sd = ser.Serial(devname, baudrate=9600, bytesize=serial.SEVENBITS, parity=serial.PARITY_ODD, stopbits=serial.STOPBITS_ONE, timeout=0.1)
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
        Bx = self.readsd()
        By = self.readsd()
        Bz = self.readsd()
        Bmod = self.readsd()
        
        return(msg, Bx, By, Bz, Bmod)
    
    def getrandomdata(self,num):
        tdata = np.random.random(num)
        xaxis = np.arange(num)
        return(tdata)

    
