import cv2
import numpy as np 
import matplotlib.pyplot as plt 
from random import randrange
import os

BASE_PATH = os.path.dirname(os.path.realpath(__file__)) 

def load_image(path):
    image = cv2.imread(path)
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    return image, image_gray


def best_matches(descriptors_right, descriptors_left, distance_coeff=0.16):
    match = cv2.BFMatcher()
    matches = match.knnMatch(des1, des2, k=2)
    
    best_matches = []
    for m,n in matches:
        if m.distance < distance_coeff*n.distance:
            best_matches.append(m)

    return best_matches


def src_keypoints_to_points(keypoints, matches):
    return np.float32([ keypoints[m.queryIdx].pt for m in matches ]).reshape(-1,1,2)


def dst_keypoints_to_points(keypoints, matches):
    return np.float32([ keypoints[m.trainIdx].pt for m in matches ]).reshape(-1,1,2)


def get_homography(matches, keypoints_right, keypoints_left, min_match_count = 10):
    homography = None
    if len(matches) > min_match_count:
        src_pts = src_keypoints_to_points(keypoints_right, matches)
        dst_pts = dst_keypoints_to_points(keypoints_left, matches)
        homography, _ = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
    else:
        print("Not enought matches are found - %d/%d", (len(matches)/min_match_count))

    return homography


def apply_homography(img_right, img_left, homography):
    dst = cv2.warpPerspective(
        src=img_right, 
        M=homography, 
        dsize=(img_left.shape[1] + img_right.shape[1], img_left.shape[0])
    )
    dst[0:img_left.shape[0], 0:img_left.shape[1]] = img_left

    return dst


def trim(frame):
    #crop top
    if not np.sum(frame[0]):
        return trim(frame[1:])
    #crop bottom
    if not np.sum(frame[-1]):
        return trim(frame[:-2])
    #crop left
    if not np.sum(frame[:,0]):
        return trim(frame[:,1:])
    #crop right
    if not np.sum(frame[:,-1]):
        return trim(frame[:,:-2])

    return frame


if __name__ == "__main__":
    img_right, img_right_gray = load_image(os.path.join(BASE_PATH, '2.jpg'))
    img_left, img_left_gray = load_image(os.path.join(BASE_PATH, '1.jpg'))

    sift = cv2.xfeatures2d.SIFT_create()
    kp1, des1 = sift.detectAndCompute(img_right_gray, None)
    kp2, des2 = sift.detectAndCompute(img_left_gray, None)
    matches = best_matches(des1, des2)

    homography = get_homography(matches, kp1, kp2)
    image = apply_homography(img_right, img_left, homography)
    image = trim(image)
    cv2.imshow("original_image_stitched_crop.jpg", image)
    cv2.waitKey(0)