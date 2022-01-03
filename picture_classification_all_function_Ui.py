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
        self.ui.pushButton.clicked.connect(self.process_canny)
        self.ui.pushButton_2.clicked.connect(self.process_black_screen)
        self.ui.pushButton_3.clicked.connect(self.process_Brightness)
        self.ui.pushButton_4.clicked.connect(self.process_mp4_to_img)

    def process_canny(self):
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
                destination = folder_path_B
                shutil.move(source, destination)
                #self.ui.textEdit_final.setText("圖片為模糊圖", output_File)
                print("圖片為模糊圖")
            else:
                #self.ui.textEdit_final.setText("圖片不為模糊圖", output_File)
                print("圖片不為模糊圖")
            #####之後要完成部分擬定，加入if value<自訂數值則移動檔案or進行標記

        self.ui.label_3.setText('模糊化照片分類完成')
        while (1):
            if (cv.waitKey(100) == 27):
                break

    def process_black_screen(self):
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

        fileList = output_File

        for f in fileList:
            imag = cv.imread(f)  # 依序讀圖
            grayImag = cv.cvtColor(imag, cv.COLOR_BGR2GRAY)  # 灰階
            # grayImag = cv.GaussianBlur(grayImag, (3, 3), 0)
            print("成功讀取模式2，開始分類黑畫面照片")

            r, c = grayImag.shape[:2]
            piexs_sum = r * c  # 整個弧度圖的像素個數為r*c

            # 獲取偏暗的像素(表示0-19的灰度值為暗)此處的值可修改
            dark_points = (grayImag < 20)
            target_array = grayImag[dark_points]
            dark_sum = target_array.size
            # 判斷灰度值為暗百分比
            dark_prop = dark_sum / ((piexs_sum))

            print('dark_prop : ' + str(dark_prop))  # 顯示值
            if dark_prop >= 0.85:
                source = f
                destination = folder_path_B
                shutil.move(source, destination)
                print("圖片為黑畫面")
                # 如果不是黑畫面積繼續處理
            else:
                print("圖片不為黑畫面")

            self.ui.label_3.setText('黑畫面照片分類完成')
            while (1):
                if (cv.waitKey(100) == 27):
                    break

    def process_Brightness(self):
        folder_path_A = QFileDialog.getExistingDirectory(self, "Open_folder_A", "./")  # start path
        print(folder_path_A)
        self.ui.show_file_path.setText(folder_path_A)

        folder_path_B = QFileDialog.getExistingDirectory(self, "Open_folder_B", "./")  # start path
        print(folder_path_B)
        self.ui.show_folder_path.setText(folder_path_B)

        output_File = []

        for root, dirs, files in os.walk(folder_path_A):
            for name in files:
                print(os.path.join(root, name))
                if os.path.splitext(name)[1] == '.jpg':
                    output_File.append(os.path.join(root, name))
        #self.ui.textEdit_final.setText('取得.jpg的檔案路徑: ', output_File)
        fileList = output_File

        for f in fileList:
            imag = cv.imread(f)  # 依序讀圖
            grayImag = cv.cvtColor(imag, cv.COLOR_BGR2GRAY)  # 灰階

            # 獲取形狀以及長寬
            img_shape = grayImag.shape
            height, width = img_shape[0], img_shape[1]
            size = grayImag.size
            # 灰度圖的直方圖
            hist = cv.calcHist([grayImag], [0], None, [256], [0, 256])

            # 计算灰度图像素点偏离均值(128)程序
            a = 0
            ma = 0
            reduce_matrix = np.full((height, width), 128)
            shift_value = grayImag - reduce_matrix
            shift_sum = sum(map(sum, shift_value))

            da = shift_sum / size

            # 计算偏离128的平均偏差
            for i in range(256):
                ma += (abs(i - 128 - da) * hist[i])
            m = abs(ma / size)
            # 亮度系数
            k = abs(da) / m
            # print(k)
            if k[0] > 1:
                # 过亮
                if da > 0:
                    destination = folder_path_B
                    shutil.move(source, destination)
                    print("亮度過亮")
                else:
                    destination = folder_path_B
                    shutil.move(source, destination)
                    print("亮度過暗")
            else:
                print("亮度正常")

            self.ui.label_3.setText('亮度過亮、過暗照片分類完成')
            while (1):
                if (cv.waitKey(100) == 27):
                    break

    def process_mp4_to_img(self):
        filename,filetype  = QFileDialog.getOpenFileName(self,"Open file","./")  # start path
        print(filename, filetype)
        self.ui.show_file_path.setText(filename)

        folder_path_B = QFileDialog.getExistingDirectory(self,"Open_folder_B","./")  # start path
        print(folder_path_B)
        self.ui.show_folder_path.setText(folder_path_B)

        #self.ui.textEdit_final.setText('讀取影片轉照片完成 ', output_File)

        videoFile = filename
        outputFile = folder_path_B
        timeF = 100
        vc = cv.VideoCapture(videoFile)
        c = 1
        if vc.isOpened():
            rval, frame = vc.read()
        else:
            print('openerror!')
            rval = False

        while rval:
            # print(rval)
            rval, frame = vc.read()
            if c % timeF == 0:
                print("!")
                cv.imwrite(outputFile + "/" + str(int(c / timeF)) + '.jpg', frame)

            c += 1
            cv.waitKey(1)
        vc.release()

        self.ui.label_3.setText('影片轉換照片完成')
        while (1):
            if (cv.waitKey(100) == 27):
                break



class Ui_MainWindow(object):#ui介面
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(549, 532)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(190, 10, 151, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(190, 100, 151, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.show_file_path = QtWidgets.QTextEdit(Form)
        self.show_file_path.setGeometry(QtCore.QRect(50, 50, 421, 41))
        self.show_file_path.setObjectName("show_file_path")
        self.show_folder_path = QtWidgets.QTextEdit(Form)
        self.show_folder_path.setGeometry(QtCore.QRect(50, 140, 421, 41))
        self.show_folder_path.setObjectName("show_folder_path")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(50, 190, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.textEdit_final = QtWidgets.QTextEdit(Form)
        self.textEdit_final.setGeometry(QtCore.QRect(20, 360, 511, 161))
        self.textEdit_final.setObjectName("textEdit_final")
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(50, 230, 191, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(50, 270, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(Form)
        self.pushButton_4.setGeometry(QtCore.QRect(50, 310, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setObjectName("pushButton_4")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(30, 370, 271, 31))
        self.label_3.setObjectName("label_3")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("MainWindow", "Form"))
        self.label.setText(_translate("MainWindow", "folder_A"))
        self.label_2.setText(_translate("MainWindow", "folder_B"))
        self.pushButton.setText(_translate("MainWindow", "process_canny"))
        self.pushButton_2.setText(_translate("MainWindow", "process_black_screen"))
        self.pushButton_3.setText(_translate("MainWindow", "process_Brightness"))
        self.pushButton_4.setText(_translate("MainWindow", "process_mp4_to_img"))
        self.label_3.setText(_translate("MainWindow", ""))

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())