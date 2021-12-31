from PyQt5 import QtWidgets, QtGui, QtCore
#from test import Ui_MainWindow
import sys
from PyQt5.QtWidgets import QFileDialog
import cv2 as cv
import shutil
import os

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__() # in python3, super(Class, self).xxx = super().xxx
        self.ui = Ui_MainWindow()

        self.ui.setupUi(self)
        self.setup_control()



    def setup_control(self):#控制所選擇按鍵
        self.ui.pushButton.clicked.connect(self.process)

    def process(self):
        folder_path_A = QFileDialog.getExistingDirectory(self,"Open_folder_A","./")  # start path
        print(folder_path_A)
        self.ui.show_file_path.setText(folder_path_A)

        folder_path_B = QFileDialog.getExistingDirectory(self,"Open_folder_B","./")  # start path
        print(folder_path_B)
        self.ui.show_folder_path.setText(folder_path_B)

        output_File = []

        for root, dirs, files in os.walk(folder_path_A):
            for name in files:
                print(os.path.join(root, name))
                if os.path.splitext(name)[1] == '.jpg':
                    output_File.append(os.path.join(root, name))
        #self.ui.textEdit.setText('取得.jpg的檔案路徑: ', output_File)
        fileList = output_File

        for f in fileList:

            imag = cv.imread(f)  # 依序讀圖
            grayImag = cv.cvtColor(imag, cv.COLOR_BGR2GRAY)  # 灰階
            # grayImag = cv.GaussianBlur(grayImag, (3, 3), 0)
            canny = cv.Canny(grayImag, 100, 100)  # 邊緣處理
            # canny = cv.  Canny(grayImag, Canny_int, Canny_int) #邊緣處理
            value = canny.var()  # 定義邊緣化數值
            print('Canny : ' + str(value))  # 顯示值
            ####
            if value < 450:
                source = f
                # 需要放刪除檔案的路徑
                #destination = "D:\move delete"
                destination = folder_path_B
                shutil.move(source, destination)
                #self.ui.textEdit.setText("圖片為模糊圖")
                print("圖片為模糊圖")
            else:
                #self.ui.textEdit.setText("圖片不為模糊圖", output_File)
                print("圖片不為模糊圖")
            #####之後要完成部分擬定，加入if value<自訂數值則移動檔案or進行標記







        while (1):
            if (cv.waitKey(100) == 27):
                break

class Ui_MainWindow(object):#ui介面
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(800, 599)
        self.centralwidget = QtWidgets.QWidget(Form)
        self.centralwidget.setObjectName("centralwidget")
        self.show_file_path = QtWidgets.QTextEdit(self.centralwidget)
        self.show_file_path.setGeometry(QtCore.QRect(160, 180, 451, 81))
        self.show_file_path.setObjectName("show_file_path")
        self.show_folder_path = QtWidgets.QTextEdit(self.centralwidget)
        self.show_folder_path.setGeometry(QtCore.QRect(160, 300, 451, 81))
        self.show_folder_path.setObjectName("show_folder_path")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(310, 390, 131, 41))
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(310, 140, 131, 31))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(310, 270, 131, 21))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        Form.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Form)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 25))
        self.menubar.setObjectName("menubar")
        Form.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Form)
        self.statusbar.setObjectName("statusbar")
        Form.setStatusBar(self.statusbar)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("MainWindow", "Form"))
        self.pushButton.setText(_translate("MainWindow", "process"))
        self.label.setText(_translate("MainWindow", "folder_A"))
        self.label_2.setText(_translate("MainWindow", " folder_B"))

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())