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

ssasd = int(input("請輸入照片之處理方式，數字1為分類模糊化之照片，數字2為分類黑畫面照片):"))
#destination = r"D:\"
#Canny_int = int(input("請輸入邊緣偵測數值，建議值為100:____"))
#value_int = int(input("請輸入分辨照片是否為模糊脂數值，建議值為450:____"))
print("讀取模式")
if ssasd<2:
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
if ssasd>1:
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


    # 文字擺放位置

    #lapla = cv.cvtColor(lapla, cv.COLOR_GRAY2BGR)
    #cv.putText(lapla, str(int(imageVar)), (0, 40), cv.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255), 2)
    # 文字擺放位置

    #grayImag = cv.cvtColor(grayImag, cv.COLOR_GRAY2BGR)
    #canny = cv.cvtColor(canny, cv.COLOR_GRAY2BGR)
    #cv.putText(canny, str(int(value)), (0, 40), cv.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255), 2)

    #longimag = np.hstack((imag, canny))  # 水平串
    #cv.namedWindow(f, 0)  # 顯示相片圖檔
    #cv.imshow(f, longimag)




while(1):
    if(cv.waitKey(100)==27):
        break

