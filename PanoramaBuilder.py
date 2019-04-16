import cv2
import os
import numpy as np
from Image import Image
from ImagesMatch import ImagesMatch
from utils import load_image, apply_homography, crop, resize_image, \
    src_keypoints_to_points, dst_keypoints_to_points


class PanoramaBuilder(object):
    def __init__(self, data_path):
        self.data_path = data_path

    
    def build_panorama(self, images_path):
        images = self._load_images(images_path)
    
        while len(images) > 1:
            images = self._perform_sift(images)
            images_match = self._match_images(images)
            images_match = self._get_matches_homography(images_match)
            images_match = self._apply_matches_homography(images_match)

            new_images = []
            for image_match in images_match:
                new_image = image_match.result_image
                new_image = crop(new_image)
                new_images.append(
                    Image(new_image, cv2.cvtColor(new_image, cv2.COLOR_BGR2GRAY))
                )

            images = new_images

        image = images[0].image_rgb
        image = resize_image(image)

        return image

    
    def _load_images(self, images_path):
        images = []
        for path in images_path:
            img, img_gray = load_image(os.path.join(self.data_path, path))
            images.append(Image(img, img_gray))
        
        return images


    def _perform_sift(self, images):
        sift = cv2.xfeatures2d.SIFT_create()

        for image in images:
            image.keypoints, image.descriptors = sift.detectAndCompute(image.image_gray, None)
            
        return images


    def _match_images(self, images, distance_coeff=0.16):
        match = cv2.BFMatcher()
        matches = []

        for i in range(len(images) - 1):
            descriptors_matches = match.knnMatch(
                images[i].descriptors, 
                images[i+1].descriptors,
                k=2
            )

            best_matches = []
            for m, n in descriptors_matches:
                if m.distance < distance_coeff*n.distance:
                    best_matches.append(m)

            matches.append(ImagesMatch(images[i], images[i+1], best_matches))

        return matches
        

    def _get_matches_homography(self, images_match, min_match_count = 4):
        for image_match in images_match:
            if len(image_match.matches) > min_match_count:
                image_right = image_match.image_right
                image_left = image_match.image_left
                src_pts = src_keypoints_to_points(image_right.keypoints, image_match.matches)
                dst_pts = dst_keypoints_to_points(image_left.keypoints, image_match.matches)
                image_match.homography, _ = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

        return images_match


    def _apply_matches_homography(self, images_match):
        for image_match in images_match:
            image_match.result_image = apply_homography(
                image_match.image_right.image_rgb, 
                image_match.image_left.image_rgb,
                image_match.homography
            )

        return images_match