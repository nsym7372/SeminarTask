import argparse
import logging
import time
import os

import cv2
import numpy as np
import matplotlib.pyplot as plt

from tf_pose import common
from tf_pose.estimator import TfPoseEstimator
from tf_pose.networks import get_graph_path, model_wh

# movie_name = 'climbing2'

img_outdir = './img'
os.makedirs(img_outdir, exist_ok=True)

# 動画作成
fourcc = cv2.VideoWriter_fourcc('m','p','4', 'v')
#video  = cv2.VideoWriter('ImgVideo2.mov', fourcc, 30.0, (540, 960))
video  = cv2.VideoWriter('ImgVideo2.mp4', fourcc, 10.0, (640, 360))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='tf-pose-estimation Video')

    outimg_files = []
    count = 0
    #w = 544 
    #h = 960
    w = 640 
    h = 368
    e = TfPoseEstimator(get_graph_path('mobilenet_thin'), target_size=(w, h))

    # 動画読み込み
    cap = cv2.VideoCapture('videoplayback01_10.mp4')

    # 動画用の画像作成
    while True:
        ret, image = cap.read()

        if ret == True:
            # １フレームずつ処理
            count += 1
            if count % 100 == 0:
                print('Image No.：{0}'.format(count))

            humans = e.inference(image, resize_to_default=(w > 0 and h > 0), upsample_size=4)
            image = TfPoseEstimator.draw_humans(image, humans, imgcopy=False)

            # 画像出力
            outimg_file = '{}/{:05d}.jpg'.format(img_outdir, count)
            cv2.imwrite(outimg_file, image)
            video.write(image)       

        else:
            break
    video.release()
    print("done")