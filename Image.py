class Image(object):
    def __init__(self, image_rgb, image_gray):
        self.image_rgb = image_rgb
        self.image_gray = image_gray


    @property
    def image_rgb(self):
        return self._image_rgb


    @image_rgb.setter
    def image_rgb(self, value):
        self._image_rgb = value

    
    @property
    def image_gray(self):
        return self._image_gray


    @image_gray.setter
    def image_gray(self, value):
        self._image_gray = value

    
    @property
    def keypoints(self):
        return self._keypoints

    
    @keypoints.setter
    def keypoints(self, value):
        self._keypoints = value

    
    @property
    def descriptors(self):
        return self._descriptors

    
    @descriptors.setter
    def descriptors(self, value):
        self._descriptors = value