import argparse
import logging
import sys
import time

from tf_pose import common
import cv2
import numpy as np
from tf_pose.estimator import TfPoseEstimator
from tf_pose.networks import get_graph_path, model_wh

logger = logging.getLogger('TfPoseEstimatorRun')
logger.handlers.clear()
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


def resize(size):
    p = 0 if (size % 16 == 0) else (16 - size % 16)
    return size + p


if __name__ == '__main__':
    print("start run_SeminarTask.py")

    parser = argparse.ArgumentParser(description='tf-pose-estimation run')
    parser.add_argument('--image', type=str,
                        default='./images/150415022548_TP_V.jpg')
    parser.add_argument('--model', type=str, default='cmu',
                        help='cmu / mobilenet_thin / mobilenet_v2_large / mobilenet_v2_small')
    parser.add_argument('--resize', type=str, default='432x368',
                        help='if provided, resize images before they are processed. '
                        'default=0x0, Recommends : 432x368 or 656x368 or 1312x736 ')
    parser.add_argument('--resize-out-ratio', type=float, default=4.0,
                        help='if provided, resize heatmaps before they are post-processed. default=1.0')

    args = parser.parse_args()

    w, h = model_wh(args.resize)

    # estimate human poses from a single image !
    image = common.read_imgfile(args.image, None, None)
    print(type(image))
     print(image.shape)
      # sys.exit()
      e = TfPoseEstimator(get_graph_path(args.model), target_size=(w, h))

       if image is None:
            logger.error('Image can not be read, path=%s' % args.image)
            sys.exit(-1)

        t = time.time()
        humans = e.inference(image, resize_to_default=(
            w > 0 and h > 0), upsample_size=args.resize_out_ratio)
        # print(type(humans))
        # print(len(humans))
        # print(type(humans[0]))

        elapsed = time.time() - t

        logger.info('inference image: %s in %.4f seconds.' %
                    (args.image, elapsed))

        image = TfPoseEstimator.draw_humans(image, humans, imgcopy=False)
        cv2.imwrite('out.jpg', image)
