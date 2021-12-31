# coding=utf-8
# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
#"D:\move ori"
import cv2 as cv
import numpy as np
import shutil
import os

# 需要读取的路径
output_File = []

for root, dirs, files in os.walk(input("請輸入圖片檔案位置:")):
    for name in files:
        print(os.path.join(root, name))
        if os.path.splitext(name)[1] == '.jpg':
            output_File.append(os.path.join(root, name))
print('取得.jpg的檔案路徑: ', output_File)

fileList = output_File

# 需要放刪除檔案的路徑
destination = input("請輸入預刪除照片之資料夾:")

mod_choose = int(input("請輸入照片之處理方式，數字1為分類模糊化之照片，數字2為分類黑畫面照片，數字3為分類低亮度照片，數字4為分割影片為照片，數字0為結束程式""):"))
#destination = r"D:\"
#Canny_int = int(input("請輸入邊緣偵測數值，建議值為100:____"))
#value_int = int(input("請輸入分辨照片是否為模糊脂數值，建議值為450:____"))
print("讀取模式")

if mod_choose==2:
    for f in fileList:
        filename = (f.split('\\'))[-1]  # 取得檔案名稱
        imag = cv.imread(f)  # 依序讀圖
        grayImag = cv.cvtColor(imag, cv.COLOR_BGR2GRAY)  # 灰階
        # grayImag = cv.GaussianBlur(grayImag, (3, 3), 0)
        print("成功讀取模式1，開始分類模糊化之照片")

        canny = cv.Canny(grayImag, 100, 100)  # 邊緣處理

        # canny = cv.  Canny(grayImag, Canny_int, Canny_int) #邊緣處理
        lapla = cv.Laplacian(grayImag, cv.CV_8U)  # 邊緣處理
        value = canny.var()  # 定義邊緣化數值
        imageVar = lapla.var()  # 定義邊緣化數值
        if value < 450:
            source = f
            shutil.move(source, destination)
            print("圖片為模糊圖")
        else:
            print("圖片不為模糊圖")
    #####之後要完成部分擬定，加入if value<自訂數值則移動檔案or進行標記

        print('Canny : ' + str(value)) #顯示值
        print('Laplacian : ' + str(imageVar))  # 顯示值
    ####
if mod_choose==1:
    for f in fileList:
        filename = (f.split('\\'))[-1]  # 取得檔案名稱
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
            destination = r"D:\move"
            shutil.move(source, destination)
            print("圖片為黑畫面")
            # 如果不是黑畫面積繼續處理
        else:
            print("圖片不為黑畫面")

if mod_choose==3:
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
                print("亮度過亮")
            else:
                print("亮度過暗")
        else:
            print("亮度正常")

if mod_choose==4:
    videoFile = input("請輸入影片檔案位置:")
    outputFile = input("請輸入處理後圖片檔案位置:")
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

if mod_choose == 0:
    exit()

while(1):
    if(cv.waitKey(100)==27):
        break

