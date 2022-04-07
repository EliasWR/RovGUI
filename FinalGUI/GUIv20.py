import cv2
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, QThread, pyqtSignal,pyqtSlot
from PyQt5.QtGui import QImage,QPixmap
import numpy as np
restrictedSector=1
runZone = -1
SonarMode="CA"
CollisionZone=""
TempValue=5.31
DepthValue= 58
SalinityValue=30
AvgTemp=6.51
AvgDepth=59.5
AvgSalinity=31.33




class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1910, 957)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet("background-color: rgb(93, 93, 93);\n""")

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 680, 141, 21))
        self.label.setStyleSheet("\n""background-color: rgb(134, 134, 134);")
        self.label.setFrameShape(QtWidgets.QFrame.Panel)
        self.label.setObjectName("label")

        self.Temp = QtWidgets.QLCDNumber(self.centralwidget)
        self.Temp.setGeometry(QtCore.QRect(30, 710, 141, 31))
        self.Temp.setStyleSheet("background-color: rgb(134, 134, 134);")
        self.Temp.setFrameShadow(QtWidgets.QFrame.Plain)
        self.Temp.setSmallDecimalPoint(True)
        self.Temp.setDigitCount(8)
        self.Temp.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.Temp.setProperty("value", 0.0)
        self.Temp.setObjectName("Temp")
        self.Temp.display(TempValue)

        self.Depth = QtWidgets.QLCDNumber(self.centralwidget)
        self.Depth.setGeometry(QtCore.QRect(30, 790, 141, 31))
        self.Depth.setStyleSheet("background-color: rgb(134, 134, 134);")
        self.Depth.setFrameShadow(QtWidgets.QFrame.Plain)
        self.Depth.setSmallDecimalPoint(True)
        self.Depth.setDigitCount(8)
        self.Depth.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.Depth.setObjectName("Depth")
        self.Depth.display(DepthValue)

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(30, 760, 141, 21))
        self.label_2.setStyleSheet("\n""background-color: rgb(134, 134, 134);")
        self.label_2.setFrameShape(QtWidgets.QFrame.Panel)
        self.label_2.setObjectName("label_2")

        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(30, 840, 141, 21))
        self.label_3.setStyleSheet("\n""background-color: rgb(134, 134, 134);")
        self.label_3.setFrameShape(QtWidgets.QFrame.Panel)
        self.label_3.setObjectName("label_3")

        self.Salinity = QtWidgets.QLCDNumber(self.centralwidget)
        self.Salinity.setGeometry(QtCore.QRect(30, 870, 141, 31))
        self.Salinity.setStyleSheet("background-color: rgb(134, 134, 134);")
        self.Salinity.setFrameShadow(QtWidgets.QFrame.Plain)
        self.Salinity.setSmallDecimalPoint(True)
        self.Salinity.setDigitCount(8)
        self.Salinity.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.Salinity.setObjectName("Salinity")
        self.Salinity.display(SalinityValue)

        self.Avg_Temp = QtWidgets.QLCDNumber(self.centralwidget)
        self.Avg_Temp.setGeometry(QtCore.QRect(210, 710, 171, 31))
        self.Avg_Temp.setStyleSheet("background-color: rgb(134, 134, 134);")
        self.Avg_Temp.setFrameShadow(QtWidgets.QFrame.Plain)
        self.Avg_Temp.setSmallDecimalPoint(True)
        self.Avg_Temp.setDigitCount(8)
        self.Avg_Temp.setMode(QtWidgets.QLCDNumber.Dec)
        self.Avg_Temp.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.Avg_Temp.setProperty("value", 0.0)
        self.Avg_Temp.setObjectName("Avg_Temp")
        self.Avg_Temp.display(AvgTemp)

        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(210, 680, 171, 21))
        self.label_4.setStyleSheet("\n""background-color: rgb(134, 134, 134);")
        self.label_4.setFrameShape(QtWidgets.QFrame.Panel)
        self.label_4.setObjectName("label_4")

        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(210, 840, 171, 21))
        self.label_5.setStyleSheet("\n""background-color: rgb(134, 134, 134);")
        self.label_5.setFrameShape(QtWidgets.QFrame.Panel)
        self.label_5.setObjectName("label_5")

        self.Avg_Salinity = QtWidgets.QLCDNumber(self.centralwidget)
        self.Avg_Salinity.setGeometry(QtCore.QRect(210, 870, 171, 31))
        self.Avg_Salinity.setStyleSheet("background-color: rgb(134, 134, 134);")
        self.Avg_Salinity.setFrameShadow(QtWidgets.QFrame.Plain)
        self.Avg_Salinity.setSmallDecimalPoint(True)
        self.Avg_Salinity.setDigitCount(8)
        self.Avg_Salinity.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.Avg_Salinity.setObjectName("Avg_Salinity")
        self.Avg_Salinity.display(AvgSalinity)

        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(210, 760, 171, 21))
        self.label_6.setStyleSheet("\n""background-color: rgb(134, 134, 134);")
        self.label_6.setFrameShape(QtWidgets.QFrame.Panel)
        self.label_6.setObjectName("label_6")

        self.Avg_Depth = QtWidgets.QLCDNumber(self.centralwidget)
        self.Avg_Depth.setGeometry(QtCore.QRect(210, 790, 171, 31))
        self.Avg_Depth.setStyleSheet("background-color: rgb(134, 134, 134);")
        self.Avg_Depth.setFrameShadow(QtWidgets.QFrame.Plain)
        self.Avg_Depth.setSmallDecimalPoint(True)
        self.Avg_Depth.setDigitCount(8)
        self.Avg_Depth.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.Avg_Depth.setObjectName("Avg_Depth")
        self.Avg_Depth.display(AvgDepth)

        self.Forward = QtWidgets.QToolButton(self.centralwidget)
        self.Forward.setGeometry(QtCore.QRect(1280, 770, 51, 41))
        self.Forward.setStyleSheet("background-color: rgb(134, 134, 134);")
        icon = (QtGui.QIcon('icons8-up-100.png'))
        self.Forward.setIcon(icon)
        self.Forward.setIconSize(QtCore.QSize(32, 32))
        self.Forward.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self.Forward.setArrowType(QtCore.Qt.NoArrow)
        self.Forward.setObjectName("Forward")
        self.Forward.pressed.connect(self.forward1)
        self.Forward.released.connect(self.release)

        self.Reverse = QtWidgets.QToolButton(self.centralwidget)
        self.Reverse.setGeometry(QtCore.QRect(1280, 870, 51, 41))
        self.Reverse.setStyleSheet("background-color: rgb(134, 134, 134);")
        icon1 = (QtGui.QIcon('icons8-down-100.png'))
        self.Reverse.setIcon(icon1)
        self.Reverse.setIconSize(QtCore.QSize(32, 32))
        self.Reverse.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self.Reverse.setArrowType(QtCore.Qt.NoArrow)
        self.Reverse.setObjectName("Reverse")
        self.Reverse.pressed.connect(self.reverse)
        self.Reverse.released.connect(self.release)

        self.Left = QtWidgets.QToolButton(self.centralwidget)
        self.Left.setGeometry(QtCore.QRect(1210, 820, 51, 41))
        self.Left.setStyleSheet("background-color: rgb(134, 134, 134);")
        icon2 = (QtGui.QIcon('icons8-left-100.png'))
        self.Left.setIcon(icon2)
        self.Left.setIconSize(QtCore.QSize(32, 32))
        self.Left.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self.Left.setArrowType(QtCore.Qt.NoArrow)
        self.Left.setObjectName("Left")
        self.Left.pressed.connect(self.left)
        self.Left.released.connect(self.release)

        self.Right = QtWidgets.QToolButton(self.centralwidget)
        self.Right.setGeometry(QtCore.QRect(1350, 820, 51, 41))
        self.Right.setStyleSheet("background-color: rgb(134, 134, 134);")
        icon3 = (QtGui.QIcon('icons8-right-100.png'))
        self.Right.setIcon(icon3)
        self.Right.setIconSize(QtCore.QSize(32, 32))
        self.Right.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self.Right.setArrowType(QtCore.Qt.NoArrow)
        self.Right.setObjectName("Right")
        self.Right.pressed.connect(self.right)
        self.Right.released.connect(self.release)

        self.RightForward = QtWidgets.QToolButton(self.centralwidget)
        self.RightForward.setGeometry(QtCore.QRect(1350, 770, 51, 41))
        self.RightForward.setStyleSheet("background-color: rgb(134, 134, 134);")
        icon4 = (QtGui.QIcon('icons8-up-right-100.png'))
        self.RightForward.setIcon(icon4)
        self.RightForward.setIconSize(QtCore.QSize(32, 32))
        self.RightForward.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self.RightForward.setObjectName("RightForward")
        self.RightForward.pressed.connect(self.forwardRight)
        self.RightForward.released.connect(self.release)

        self.LeftForward = QtWidgets.QToolButton(self.centralwidget)
        self.LeftForward.setGeometry(QtCore.QRect(1210, 770, 51, 41))
        self.LeftForward.setStyleSheet("background-color: rgb(134, 134, 134);")
        icon5 = (QtGui.QIcon('icons8-up-left-100.png'))
        self.LeftForward.setIcon(icon5)
        self.LeftForward.setIconSize(QtCore.QSize(32, 32))
        self.LeftForward.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self.LeftForward.setObjectName("LeftForward")
        self.LeftForward.pressed.connect(self.forwardLeft)
        self.LeftForward.released.connect(self.release)

        self.ReverseLeft = QtWidgets.QToolButton(self.centralwidget)
        self.ReverseLeft.setGeometry(QtCore.QRect(1210, 870, 51, 41))
        self.ReverseLeft.setStyleSheet("background-color: rgb(134, 134, 134);")
        icon6 = (QtGui.QIcon('icons8-down-left-arrow-100.png'))
        self.ReverseLeft.setIcon(icon6)
        self.ReverseLeft.setIconSize(QtCore.QSize(32, 32))
        self.ReverseLeft.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self.ReverseLeft.setObjectName("ReverseLeft")
        self.ReverseLeft.pressed.connect(self.reverseLeft)
        self.ReverseLeft.released.connect(self.release)

        self.ReverseRight = QtWidgets.QToolButton(self.centralwidget)
        self.ReverseRight.setGeometry(QtCore.QRect(1350, 870, 51, 41))
        self.ReverseRight.setStyleSheet("background-color: rgb(134, 134, 134);")
        icon7 = (QtGui.QIcon('icons8-down-right-100.png'))
        self.ReverseRight.setIcon(icon7)
        self.ReverseRight.setIconSize(QtCore.QSize(32, 32))
        self.ReverseRight.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self.ReverseRight.setObjectName("ReverseRight")
        self.ReverseRight.pressed.connect(self.reverseRight)
        self.ReverseRight.released.connect(self.release)

        self.Light_Value_Slider = QtWidgets.QSlider(self.centralwidget)
        self.Light_Value_Slider.setGeometry(QtCore.QRect(920, 710, 61, 201))
        self.Light_Value_Slider.setStyleSheet("background-color: rgb(134, 134, 134);")
        self.Light_Value_Slider.setOrientation(QtCore.Qt.Vertical)
        self.Light_Value_Slider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.Light_Value_Slider.setObjectName("Light_Value_Slider")
        self.Light_Value_Slider.setMaximum(255)
        self.Light_Value_Slider.setMinimum(0)
        self.Light_Value_Slider.valueChanged.connect(self.valuechangeLS)

        self.CounterClockwise = QtWidgets.QToolButton(self.centralwidget)
        self.CounterClockwise.setGeometry(QtCore.QRect(1210, 710, 51, 41))
        self.CounterClockwise.setStyleSheet("background-color: rgb(134, 134, 134);")
        icon8 = (QtGui.QIcon('icons8-reply-arrow-100.png'))
        self.CounterClockwise.setIcon(icon8)
        self.CounterClockwise.setIconSize(QtCore.QSize(32, 32))
        self.CounterClockwise.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self.CounterClockwise.setObjectName("CounterClockwise")
        self.CounterClockwise.pressed.connect(self.RotationCC)
        self.CounterClockwise.released.connect(self.release)

        self.Clockwise = QtWidgets.QToolButton(self.centralwidget)
        self.Clockwise.setGeometry(QtCore.QRect(1350, 710, 51, 41))
        self.Clockwise.setStyleSheet("background-color: rgb(134, 134, 134);")
        icon9 = (QtGui.QIcon('icons8-forward-arrow-100.png'))
        self.Clockwise.setIcon(icon9)
        self.Clockwise.setIconSize(QtCore.QSize(32, 32))
        self.Clockwise.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self.Clockwise.setObjectName("Clockwise")
        self.Clockwise.pressed.connect(self.RotationCW)
        self.Clockwise.released.connect(self.release)

        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(900, 680, 101, 21))
        self.label_7.setStyleSheet("background-color: rgb(134, 134, 134);")
        self.label_7.setFrameShape(QtWidgets.QFrame.Box)
        self.label_7.setFrameShadow(QtWidgets.QFrame.Plain)
        self.label_7.setObjectName("label_7")

        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(1260, 680, 91, 20))
        self.label_8.setStyleSheet("background-color: rgb(134, 134, 134);")
        self.label_8.setFrameShape(QtWidgets.QFrame.Box)
        self.label_8.setObjectName("label_8")

        self.WarningLable = QtWidgets.QLabel(self.centralwidget)
        self.WarningLable.setGeometry(QtCore.QRect(1550, 740, 231, 31))
        self.WarningLable.setStyleSheet("background-color: rgb(134, 134, 134);")
        self.WarningLable.setFrameShape(QtWidgets.QFrame.Box)
        self.WarningLable.setObjectName("WarningLable")

        self.ResetButton = QtWidgets.QPushButton(self.centralwidget)
        self.ResetButton.setGeometry(QtCore.QRect(1580, 800, 171, 61))
        self.ResetButton.setStyleSheet("\n""background-color: rgb(134, 134, 134);")
        self.ResetButton.setObjectName("ResetButton")
        self.ResetButton.clicked.connect(self.Resetbutton)

        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        self.label_11.setGeometry(QtCore.QRect(750, 680, 101, 21))
        self.label_11.setStyleSheet("background-color: rgb(134, 134, 134);")
        self.label_11.setFrameShape(QtWidgets.QFrame.Box)
        self.label_11.setFrameShadow(QtWidgets.QFrame.Plain)
        self.label_11.setObjectName("label_11")

        self.Motor_Speed_Slider = QtWidgets.QSlider(self.centralwidget)
        self.Motor_Speed_Slider.setGeometry(QtCore.QRect(770, 710, 61, 201))
        self.Motor_Speed_Slider.setStyleSheet("background-color: rgb(134, 134, 134);")
        self.Motor_Speed_Slider.setOrientation(QtCore.Qt.Vertical)
        self.Motor_Speed_Slider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.Motor_Speed_Slider.setObjectName("Motor_Speed_Slider")
        self.Motor_Speed_Slider.setMaximum(255)
        self.Motor_Speed_Slider.setMinimum(0)
        self.Motor_Speed_Slider.valueChanged.connect(self.valuechangeMS)


        self.SonarScreen = QtWidgets.QLabel(self.centralwidget)
        self.SonarScreen.setGeometry(QtCore.QRect(10, 0, 671, 671))
        self.SonarScreen.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.SonarScreen.setFrameShadow(QtWidgets.QFrame.Plain)
        self.SonarScreen.setText("")
        self.SonarScreen.setObjectName("SonarScreen")

        self.VideoFeed = QtWidgets.QLabel(self.centralwidget)
        self.VideoFeed.setGeometry(QtCore.QRect(690, 0, 1211, 671))
        self.VideoFeed.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.VideoFeed.setText("")
        self.VideoFeed.setObjectName("VideoFeed")

        self.SonarMode = QtWidgets.QLabel(self.centralwidget)
        self.SonarMode.setGeometry(QtCore.QRect(440, 680, 211, 21))
        self.SonarMode.setStyleSheet("background-color: rgb(134, 134, 134);")
        self.SonarMode.setFrameShape(QtWidgets.QFrame.Box)
        self.SonarMode.setObjectName("SonarMode")

        self.ScanModeB = QtWidgets.QPushButton(self.centralwidget)
        self.ScanModeB.setGeometry(QtCore.QRect(470, 720, 161, 71))
        self.ScanModeB.setStyleSheet("background-color: rgb(134, 134, 134);")
        self.ScanModeB.setObjectName("ScanModeB")
        self.ScanModeB.clicked.connect(self.SonarM2)

        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(1540, 680, 251, 31))
        self.label_9.setStyleSheet("background-color: rgb(134, 134, 134);")
        self.label_9.setFrameShape(QtWidgets.QFrame.Box)
        self.label_9.setObjectName("label_9")

        self.CollisionAvoidB = QtWidgets.QPushButton(self.centralwidget)
        self.CollisionAvoidB.setGeometry(QtCore.QRect(470, 830, 161, 71))
        self.CollisionAvoidB.setStyleSheet("background-color: rgb(134, 134, 134);")
        self.CollisionAvoidB.setObjectName("CollisionAvoidB")
        self.CollisionAvoidB.clicked.connect(self.SonarM1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1910, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)


        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Temperature(°C):"))
        self.label_2.setText(_translate("MainWindow", "Depth(m):"))
        self.label_3.setText(_translate("MainWindow", "Salinity(ppm):"))
        self.label_4.setText(_translate("MainWindow", "Average Temp(°C):"))
        self.label_5.setText(_translate("MainWindow", "Average Salinity(ppm):"))
        self.label_6.setText(_translate("MainWindow", "Average Depth(m):"))
        self.Forward.setText(_translate("MainWindow", "Forward"))
        self.Reverse.setText(_translate("MainWindow", "..."))
        self.Left.setText(_translate("MainWindow", "..."))
        self.Right.setText(_translate("MainWindow", "..."))
        self.RightForward.setText(_translate("MainWindow", "..."))
        self.LeftForward.setText(_translate("MainWindow", "..."))
        self.ReverseLeft.setText(_translate("MainWindow", "..."))
        self.ReverseRight.setText(_translate("MainWindow", "..."))
        self.CounterClockwise.setText(_translate("MainWindow", "..."))
        self.Clockwise.setText(_translate("MainWindow", "..."))
        self.label_7.setText(_translate("MainWindow", " Light Value"))
        self.label_8.setText(_translate("MainWindow", "  Controls"))
        self.WarningLable.setText(_translate("MainWindow", "Warning in Zone: "))
        self.ResetButton.setText(_translate("MainWindow", "Reset"))
        self.label_11.setText(_translate("MainWindow", "Motor Speed"))
        self.SonarMode.setText(_translate("MainWindow", "Current Sonar Mode: "))
        self.ScanModeB.setText(_translate("MainWindow", "Scan Mode"))
        self.label_9.setText(_translate("MainWindow", "     Collision Avoidance Reset"))
        self.CollisionAvoidB.setText(_translate("MainWindow", "Collision Avoidance"))

        # Button Release
    def release(self):
        global runZone
        runZone = -1
        print(runZone)

    def forward1(self):
        global runZone
        runZone = 1
        print(runZone)

    def forwardRight(self):
        global runZone
        runZone = 2
        print(runZone)

    def right(self):
        global runZone
        runZone = 3
        print(runZone)

    def reverseRight(self):
        global runZone
        runZone = 4
        print(runZone)

    def reverse(self):
        global runZone
        runZone = 5
        print(runZone)

    def reverseLeft(self):
        global runZone
        runZone = 6
        print(runZone)

    def left(self):
        global runZone
        runZone = 7
        print(runZone)

    def forwardLeft(self):
        global runZone
        runZone = 8
        print(runZone)

    def RotationCW(self):
        global runZone
        runZone = 9
        print(runZone)

    def RotationCC(self):
        global runZone
        runZone = 10
        print(runZone)

    #Collision Avoid Button
    def SonarM1(self):
        self.SonarMode.setText("Current Sonar Mode: Avoid")
        global SonarMode
        SonarMode = "Avoid"
        print(SonarMode)

    #Sonar Scan Button
    def SonarM2(self):
        self.SonarMode.setText("Current Sonar Mode: Scan")
        global SonarMode
        SonarMode = "Scan"
        print(SonarMode)

    def valuechangeMS(self):
        global MotorSpeed
        MotorSpeed = self.Motor_Speed_Slider.value()
        print(MotorSpeed)

    def valuechangeLS(self):
        global LightStrength
        LightStrength = self.Light_Value_Slider.value()
        print(LightStrength)

    def Resetbutton(self):
        global CollisionZone
        CollisionZone="None"
        self.WarningLable.setText("Warning in Zone:None")



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
