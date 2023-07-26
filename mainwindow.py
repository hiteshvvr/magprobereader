from PyQt5.QtWidgets import QPushButton, QWidget
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QHBoxLayout
from PyQt5.QtWidgets import QLineEdit, QFileDialog, QComboBox
from PyQt5.QtWidgets import QPlainTextEdit 
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem 
from PyQt5.QtCore import QSettings
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore
import numpy as np
import pandas as pd



class MainWindow(QWidget):
    # def __init__(self, parent) -> None:
    def __init__(self, data):
        super(QWidget, self).__init__()
        self.layout = QVBoxLayout(self)
        pg.setConfigOption('background', 'w')
        
        #Last Values
        self.settings = QSettings("./magsettingts.ini", QSettings.IniFormat)
        try:
            self.foldname = self.settings.value('folder')
            self.devname = self.settings.value('device')
        except:
            self.foldname = "Select folder to record data"
            self.devname = "select device"

        # Initialize DATA
        self.data = data
        # Initialize Tab
        self.maintab = QWidget()

        # self.height
        self.width = 100
        self.unit = "Gauss"

        # Create Layouts
        self.mainlayout = QVBoxLayout()
        self.in1layout = QHBoxLayout()
        self.in2layout = QHBoxLayout()
        self.in3layout = QHBoxLayout()
        self.in4layout = QHBoxLayout()
        self.in5layout = QHBoxLayout()
        self.in6layout = QHBoxLayout()
        self.in7layout = QHBoxLayout()
        
        
        self.button_connect = QPushButton('Connect Device')
        self.button_connect.clicked.connect(self.connectdevice)
        self.field_devname = QLineEdit(self.devname)
        
       
        self.field_foldname = QLineEdit(self.foldname)
        
        self.button_foldname = QPushButton('Select Folder')
        self.button_foldname.clicked.connect(self.dialog)
        # self.filename = "filetoreadinfutute"
        
        self.filename = "change_filename_to_save.txt"
        self.button_filename = QPushButton("Set filename")
        self.button_filename.clicked.connect(self.updatefilename)
        self.field_filename = QLineEdit(self.filename)
        
        self.sel_units = QComboBox() 
        self.sel_units.addItems([str('Gauss'), str('Tesla')])
        self.sel_units.currentIndexChanged.connect(self.selectunits)
        self.fieldunitlabel = QLabel(self.unit)
        
        self.sel_range = QComboBox() 
        self.sel_range.addItems([str('30000'), str('3000'), str('300'), str('30')])
        self.sel_range.currentIndexChanged.connect(self.selectrange)
 
        self.sel_disunit = QComboBox() 
        self.sel_disunit.addItems([str('mm'), str('cm'), str('inch')])
        self.sel_disunit.currentIndexChanged.connect(self.selectdisunit)
        
        self.xlabel = QLabel("x") 
        self.dis_x= QLineEdit(self.data.field['x'])
        self.field_x= QLineEdit(self.data.field['Bx'])
        
        self.ylabel = QLabel("y") 
        self.dis_y= QLineEdit(self.data.field['y'])
        self.field_y= QLineEdit(self.data.field['By'])
        
        self.zlabel = QLabel("z") 
        self.dis_z= QLineEdit(self.data.field['z'])
        self.field_z= QLineEdit(self.data.field['Bz'])
        
        self.field_mod= QLineEdit(self.data.field['Bmod'])
        
        self.button_readfield = QPushButton("ReadData")
        self.button_readfield.clicked.connect(self.readfields)

#******************************FUNCTIONS *******************************************************#
        # self.noisedata = np.random.random(20)
        # self.disax = np.arange(20)
        
        self.pwx = pg.PlotWidget(title="Plot Bx")
        self.plx = self.pwx.plot()
        self.initiateplot(self.pwx, self.plx)
                
        self.pwy = pg.PlotWidget(title="Plot By")
        self.ply = self.pwy.plot()
        self.initiateplot(self.pwy, self.ply)
        
        self.pwz = pg.PlotWidget(title="Plot Bz")
        self.plz = self.pwz.plot()
        self.initiateplot(self.pwz, self.plz)
        
        self.pwm = pg.PlotWidget(title="Plot Bm")
        self.plm = self.pwm.plot()
        self.initiateplot(self.pwm, self.plm)
        
    ################ADD EVERYTING TO LAYOUT ############################
    
    
        self.maintab.setLayout(self.mainlayout)
        # self.tab1.setLayout(self.alayout)

        # Add tabs to Widget
        self.layout.addWidget(self.maintab)
        self.setLayout(self.layout)


        self.in1layout.addWidget(self.button_connect)
        self.in1layout.addWidget(self.field_devname)
        
        self.in2layout.addWidget(self.button_foldname)
        self.in2layout.addWidget(self.field_foldname)
        self.in2layout.addWidget(self.button_filename)
        self.in2layout.addWidget(self.field_filename)

        self.in3layout.addWidget(self.sel_units)
        self.in3layout.addWidget(self.sel_range)

        self.in4layout.addWidget(self.sel_disunit)
        self.in4layout.addWidget(self.xlabel)
        self.in4layout.addWidget(self.dis_x)
        self.in4layout.addWidget(self.ylabel)
        self.in4layout.addWidget(self.dis_y)
        self.in4layout.addWidget(self.zlabel)
        self.in4layout.addWidget(self.dis_z)
        self.in4layout.addWidget(self.button_readfield)
     
        self.in5layout.addWidget(self.fieldunitlabel)
        self.in5layout.addWidget(self.xlabel)
        self.in5layout.addWidget(self.field_x)
        self.in5layout.addWidget(self.ylabel)
        self.in5layout.addWidget(self.field_y)
        self.in5layout.addWidget(self.zlabel)
        self.in5layout.addWidget(self.field_z)
        self.in5layout.addWidget(self.field_mod)   
        
        self.in6layout.addWidget(self.pwx)
        self.in6layout.addWidget(self.pwy)
        self.in7layout.addWidget(self.pwz)
        self.in7layout.addWidget(self.pwm)



        self.mainlayout.addLayout(self.in1layout)
        self.mainlayout.addLayout(self.in2layout)
        self.mainlayout.addLayout(self.in3layout)
        self.mainlayout.addLayout(self.in4layout)
        self.mainlayout.addLayout(self.in5layout)
        self.mainlayout.addLayout(self.in6layout)
        self.mainlayout.addLayout(self.in7layout)
  
#***************Functions for loading Data *****************************************************#
   
    def dialog(self):
        self.foldname = QFileDialog.getExistingDirectory(
            None, "OpenDirectorytosavefiles")
        if self.foldname:
            self.field_foldname.setText(self.foldname)
            self.settings.setValue("folder", self.foldname)
        else:
            self.field_foldname.setText= "folder not found!!"
    
    def updatefilename(self):
        self.filename = self.field_filename.text()
        self.data.filepath = str(self.foldname+ "/" + self.filename)
        try:
            f = open(self.data.filepath,'a+')
            f.write('x,y,z,Bx,By,Bz,Bmod\n')
            f.close()
            self.writeunits()
            self.field_filename.setText(self.filename + "\t\t opened")        
        except:
            self.field_filename.setText("Couldn't open file")
            
    def writeunits(self):
        a = self.sel_units.currentText() + ','
        b = self.sel_disunit.currentText() + ','
        units = b + b + b + a + a + a + a[:-1] + '\n'
        print(a,b)
        try:
            f = open(self.data.filepath,'a+')
            f.write(units)
            f.close()
        except:
            print("could not write the units")
    
    def connectdevice(self):
        self.devname = self.field_devname.text()
        self.settings.setValue("device", self.devname)
        msg = self.data.connectdev(self.devname)
        self.field_devname.setText(msg)
        return
    
    def selectunits(self):
        self.unit = self.sel_units.currentText()
        # print(self.data.setunits(self.unit))
        self.fieldunitlabel.setText(self.unit)
        self.writeunits()
        
    def selectrange(self):
        self.range = self.sel_range.currentText()
        print(self.data.setrange(self.range))
    
    def setposition(self):
        self.x = self.dis_x.text()
        self.y = self.dis_y.text()
        self.z = self.dis_z.text()
        self.data.field['x'] = self.dis_x.text()
        self.data.field['y'] = self.dis_y.text()
        self.data.field['z'] = self.dis_z.text()
        
        
    def readfields(self):
        self.setposition()
        msg = self.data.readalldata()
        print(msg)
        self.field_x.setText("Bx  : " + self.data.field['Bx'])
        self.field_y.setText("By  : " + self.data.field['By'])
        self.field_z.setText("By  : " + self.data.field['Bz'])
        self.field_mod.setText("Bmod  : " + self.data.field['Bmod'])
        
        msg = ''
        for key in self.data.field:
            msg = msg + self.data.field[key] + ','
        msg = msg[:-1] + '\n'
        print(msg[:-1])   
        
        self.writefields(msg)
        self.updateplots()
       
        return 0
    
    def writefields(self, msg):
        try:
            f = open(self.data.filepath,'a+')
            f.write(msg)
            f.close()
        except:
            print("file does not exist!")
        
    def selectdisunit(self):
        self.writeunits()
        return 0
    
    def updateplots(self):
        loc,field = self.data.getfielddata('x','Bx')
        self.updateplot(self.pwx,self.plx,loc,field)
        loc,field = self.data.getfielddata('y','By')
        self.updateplot(self.pwy,self.ply,loc,field)
        loc,field = self.data.getfielddata('z','Bz')
        self.updateplot(self.pwz,self.plz,loc,field)
        x,y,z,field = self.data.getfielddata()
        
    
    def updateplot(self,pw,pl,x,f):
        pw.setLabel('left', 'Value', units=self.sel_units.currentText())
        pw.setLabel('bottom', 'distance', units=self.sel_disunit.currentText())
        pl.setData(x = x,y = f)
        
         
    def initiateplot(self,pw,pl):
        pw.setLabel('left', 'Value', units=self.sel_units.currentText())
        pw.setLabel('bottom', 'distance', units=self.sel_disunit.currentText())
        pw.showGrid(x=True, y=True)
        pl.setPen(color=(0, 0, 0), width=5)
        pl.setData(x = np.arange(30),y = self.data.getrandomdata(30))
        
        
   