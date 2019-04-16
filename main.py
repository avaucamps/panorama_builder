import os
import cv2
from PanoramaBuilder import PanoramaBuilder


DATA_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")


def show_panorama(image):
    cv2.imshow("Panorama", image)
    cv2.waitKey(0)


if __name__ == "__main__":
    panorama_builder = PanoramaBuilder(DATA_PATH)

    images_path = ["goldengate-05.png", "goldengate-04.png", "goldengate-03.png", 
     "goldengate-02.png", "goldengate-01.png", "goldengate-00.png"]
    image = panorama_builder.build_panorama(images_path)
    show_panorama(panorama_builder.build_panorama(images_path))

    images_path = ["sea_right.jpg", "sea_center.jpg", "sea_left.jpg"]
    show_panorama(panorama_builder.build_panorama(images_path))

    images_path = ["building_right.jpg", "building_left.jpg"]
    show_panorama(panorama_builder.build_panorama(images_path))