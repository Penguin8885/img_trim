import sys
import os
import cv2
import numpy as np

def trim(img, lower, upper, size=None):
    #閾値判定, グレイスケール化
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    gray = cv2.inRange(
        gray,
        np.array(lower, np.uint8),
        np.array(upper, np.uint8)
    )
    gray = cv2.bitwise_not(gray)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)

    #輪郭抽出
    _, cnts, _ = cv2.findContours(gray, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE) #輪郭抽出

    ###元画像そのままのサイズでトリミングすることを回避
    img_size = img.shape[0]*img.shape[1]
    for i, cnt in enumerate(cnts[:]):
        if cv2.contourArea(cnt) / img_size > 0.99:
            cnts.pop(i)

    cnt = sorted(cnts, key=cv2.contourArea, reverse=True)[0]   #面積昇順ソート,最大を選択
    arclen = cv2.arcLength(cnt, True)                          #輪郭の長さを計算
    approx = cv2.approxPolyDP(cnt, 0.02*arclen, True)          #輪郭の近似を計算

    #4つの角の座標を計算
    points = approx[:,0,:]                                        #近似点を抽出
    points = sorted(points, key=lambda x: x[1])                   #y座標でソート
    top = sorted(points[:2], key=lambda x: x[0])                  #y座標が小さい上2つをx座標でソート
    bottom = sorted(points[2:], key=lambda x:x[0], reverse=True)  #y座標が大きい上2つをx座標でソート
    points = np.array(top + bottom, dtype='float32')              #左上, 右上, 右下, 左下の順で再格納

    print(points)

    #縦幅, 横幅を計算
    if size is None:
        height = max(
                np.sqrt(((points[0][1]-points[2][1])**2)*2),
                np.sqrt(((points[1][1]-points[3][1])**2)*2)
            )
        width = max(
                np.sqrt(((points[0][0]-points[2][0])**2)*2),
                np.sqrt(((points[1][0]-points[3][0])**2)*2)
            )
    else:
        height = size[0]
        width = size[1]

    #変換後の4つの角の座標を計算
    dst = np.array(
            [
                np.array([0, 0]),
                np.array([width-1, 0]),
                np.array([width-1, height-1]),
                np.array([0, height-1]),
			],
            np.float32
        )

    #4点からトリミング
    trans = cv2.getPerspectiveTransform(points, dst)  #透視変換行列を作成
    trim_img = cv2.warpPerspective(img, trans, (int(width), int(height)))
    return trim_img

if __name__ == '__main__':
    flag = False
    args = sys.argv
    if len(args) == 4:
        flag = True
        height = args[1]
        width = args[2]

    #resultディレクトリの中のファイルを全削除
    file_names = os.listdir("./result/")
    for file_name in file_names:
        if file_name == ".gitkeep":
            continue
        os.remove("./result/"+file_name)

    #dataディレクトリの画像を読み込み，トリム，resultディレクトリに保存
    file_names = os.listdir("./data/")
    for file_name in file_names:
        if file_name == ".gitkeep":
            continue
        print(file_name)

        img = cv2.imread("./data/"+file_name)   #画像読み込み

        #トリミング
        if flag:
            trimming_img = trim(img, [0, 0, 150], [255, 255, 255], size=(height, width))
        else:
            trimming_img = trim(img, [0, 0, 150], [255, 255, 255])

        print(trimming_img)

        cv2.imwrite("./result/"+file_name, trimming_img)  #画像保存
