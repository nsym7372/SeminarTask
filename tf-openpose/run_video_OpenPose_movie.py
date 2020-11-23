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
video_outdir = './output'
video_inputdir = './input'
os.makedirs(img_outdir, exist_ok=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='tf-pose-estimation Video')
    parser.add_argument('mp4file', type=str, default='')
    
    args = parser.parse_args()

    # 動画読み込み
    cap = cv2.VideoCapture('{0}/{1}'.format(video_inputdir, args.mp4file))
    
    w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    fps = cap.get(cv2.CAP_PROP_FPS)

    outimg_files = []
    count = 0

    # 処理サイズ、内部16の倍数
    inw = w + (16 - w % 16)
    inh = h + (16 - h % 16)   

    e = TfPoseEstimator(get_graph_path('mobilenet_thin'), target_size=(inw, inh))

    # 動画用の画像作成
    outfile = '{0}/{1}'.format(video_outdir, args.mp4file)
    fourcc = cv2.VideoWriter_fourcc('m','p','4', 'v')
    video  = cv2.VideoWriter(outfile, fourcc, fps, (w, h))

    while True:
        ret, image = cap.read()

        if ret == True:
            # １フレームずつ処理
            count += 1
            if count % 100 == 0:
                print('Image No.：{0}'.format(count))

            humans = e.inference(image, resize_to_default=(inw > 0 and inh > 0), upsample_size=4)
            image = TfPoseEstimator.draw_humans(image, humans, imgcopy=False)

            # 画像出力
            outimg_file = '{}/{:05d}.jpg'.format(img_outdir, count)
            cv2.imwrite(outimg_file, image)
            video.write(image)       

        else:
            break
    video.release()
    print("done")