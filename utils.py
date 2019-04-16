import cv2
import numpy as np
from win32api import GetSystemMetrics


def load_image(path):
    image = cv2.imread(path)
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    return image, image_gray


def src_keypoints_to_points(keypoints, matches):
    return np.float32([ keypoints[m.queryIdx].pt for m in matches ]).reshape(-1,1,2)


def dst_keypoints_to_points(keypoints, matches):
    return np.float32([ keypoints[m.trainIdx].pt for m in matches ]).reshape(-1,1,2)


def apply_homography(img_right, img_left, homography):
    dst = cv2.warpPerspective(
        src=img_right,
        M=homography,
        dsize=(img_left.shape[1] + img_right.shape[1], img_left.shape[0])
    )
    dst[0:img_left.shape[0], 0:img_left.shape[1]] = img_left

    return dst


def crop(image):
    gray = cv2.cvtColor(image ,cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray,1,255,cv2.THRESH_BINARY)
    contours = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    x,y,w,h = cv2.boundingRect(contours[0])
    crop = image[y:y+h,x:x+w]

    return crop


def resize_image(image):
    screen_width = GetSystemMetrics(0)
    screen_height = GetSystemMetrics(1)

    if image.shape[1] <= screen_width and image.shape[0] <= screen_height:
        return image

    resize_ratio = min(screen_width/image.shape[1], screen_height/image.shape[0])
    new_width = int(image.shape[1] * resize_ratio)
    new_height = int(image.shape[0] * resize_ratio)
    image = cv2.resize(image, (new_width, new_height))

    return image