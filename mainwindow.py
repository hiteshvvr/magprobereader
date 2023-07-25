from PyQt5.QtWidgets import QPushButton, QWidget
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QHBoxLayout
from PyQt5.QtWidgets import QLineEdit, QFileDialog, QComboBox
from PyQt5.QtWidgets import QPlainTextEdit #SRW
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem #SRW
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore
import numpy as np



class MainWindow(QWidget):
    # def __init__(self, parent) -> None:
    def __init__(self, data):
        super(QWidget, self).__init__()
        self.layout = QVBoxLayout(self)
        pg.setConfigOption('background', 'w')

        # Initialize DATA
        self.data = data
        # Initialize Tab
        self.maintab = QWidget()

        # self.height
        self.width = 100
        self.unit = "Gauss"

        # Create First Tab
        # self.tab1.layout = QVBoxLayout(self)
        self.mainlayout = QVBoxLayout()
        self.in1layout = QHBoxLayout()
        self.in2layout = QHBoxLayout()
        self.in3layout = QHBoxLayout()
        self.in4layout = QHBoxLayout()
        self.in5layout = QHBoxLayout()
        self.in6layout = QHBoxLayout()
        self.in7layout = QHBoxLayout()
        # self.r1layout = QHBoxLayout()
        # self.r2layout = QHBoxLayout()
        
        
        self.devname = '/dev/ttyUSB0'
        self.button_connect = QPushButton('Connect Device')
        self.button_connect.clicked.connect(self.connectdevice)
        self.field_devname = QLineEdit(self.devname)
        
        self.foldname = "Select folder to record data"
        self.field_foldname = QLineEdit(self.foldname)
        
        self.button_foldname = QPushButton('Select Folder')
        self.button_foldname.clicked.connect(self.dialog)
        # self.filename = "filetoreadinfutute"
        
        self.filename = "Enter filename to save data"
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
        
        self.x = '0'
        self.Bx = '0'
        self.xlabel = QLabel("x") 
        self.dis_x= QLineEdit(self.x)
        self.field_x= QLineEdit(self.Bx)
        
        self.y = '0'
        self.By = '0'
        self.ylabel = QLabel("y") 
        self.dis_y= QLineEdit(self.y)
        self.field_y= QLineEdit(self.By)
        
        self.z = '0'
        self.Bz = '0'
        self.zlabel = QLabel("z") 
        self.dis_z= QLineEdit(self.z)
        self.field_z= QLineEdit(self.Bz)
        
        self.fieldtotal = '0' 
        self.field_total= QLineEdit(self.fieldtotal)
        
        self.button_readfield = QPushButton("ReadData")
        self.button_readfield.clicked.connect(self.readfields)

        # self.field_runno = QLineEdit(str(self.runno))
        
              
        # self.mainlayout.addLayout(self.in5layout)
        # self.mainlayout.addLayout(self.r1layout)
        # self.mainlayout.addLayout(self.r2layout)
        
        # self.alayout.addWidget(self.pw1)
        # self.alayout.addWidget(self.pw2)

#******************************FUNCTIONS *******************************************************#
        # self.noisedata = np.random.random(20)
        # self.disax = np.arange(20)
        
        self.pw1 = pg.PlotWidget(title="Plot Bx")
        self.pl1 = self.pw1.plot()
        self.pw1.setLabel('left', 'Value', units='G/T')
        self.pw1.setLabel('bottom', 'distance', units='mm/cm/inch')
        self.pl1.setPen(color=(0, 0, 0), width=5)
        self.pw1.showGrid(x=True, y=True)
        self.pl1.setData(x = np.arange(30),y = self.data.getrandomdata(30))
        
        
        self.pw2 = pg.PlotWidget(title="Plot By")
        self.pl2 = self.pw2.plot()
        self.pw2.setLabel('left', 'Value', units='G/T')
        self.pw2.setLabel('bottom', 'distance', units='mm/cm/inch')
        self.pl2.setPen(color=(0, 0, 0), width=5)
        self.pw2.showGrid(x=True, y=True)
        self.pl2.setData(x = np.arange(30),y = self.data.getrandomdata(30))
        
        self.pw3 = pg.PlotWidget(title="Plot Bz")
        self.pl3 = self.pw3.plot()
        self.pw3.setLabel('left', 'Value', units='G/T')
        self.pw3.setLabel('bottom', 'distance', units='mm/cm/inch')
        self.pl3.setPen(color=(0, 0, 0), width=5)
        self.pw3.showGrid(x=True, y=True)
        self.pl3.setData(x = np.arange(20),y = self.data.getrandomdata(20))
        
        self.pw4 = pg.PlotWidget(title="Plot Bm")
        self.pl4 = self.pw4.plot()
        self.pw4.setLabel('left', 'Value', units='G/T')
        self.pw4.setLabel('bottom', 'distance', units='mm/cm/inch')
        self.pl4.setPen(color=(0, 0, 0), width=5)
        self.pw4.showGrid(x=True, y=True)
        self.pl4.setData(x = np.arange(20),y = self.data.getrandomdata(20))
        
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
        self.in5layout.addWidget(self.field_total)   
        
        self.in6layout.addWidget(self.pw1)
        self.in6layout.addWidget(self.pw2)
        self.in7layout.addWidget(self.pw3)
        self.in7layout.addWidget(self.pw4)



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
            self.data.foldname = self.foldname
        else:
            self.field_foldname.setText= "folder not found!!"
    
    def updatefilename(self):
        self.filename = self.field_filename.text()
        self.data.filename = self.filename
        self.field_filename.setText(self.data.foldname+self.data.filename)        
    
    def connectdevice(self):
        """
        Get the data in the data class
        """
        self.filename = self.field_filename.text()
        msg = self.data.connectdev(self.devname)
        self.field_devname.setText(msg)
        print("pressed")
        return
    
    def selectunits(self):
        self.unit = self.sel_units.currentText()
        print(self.data.setunits(self.unit))
        self.fieldunitlabel.setText(self.unit)
        
    def selectrange(self):
        self.range = self.sel_range.currentText()
        print(self.data.setrange(self.range))
        
    def readfields(self):
        msg,self.Bx,self.By,self.Bz,self.Bmod = self.data.readalldata()
        print(msg)
        self.field_x.setText("Bx  : " + self.Bx)
        self.field_y.setText("By  : " + self.By)
        self.field_z.setText("Bz  : " + self.Bz)
        return 0
    
    def selectdisunit(self):
        return 0
    
   