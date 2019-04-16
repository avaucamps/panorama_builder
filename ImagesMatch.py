class ImagesMatch(object):
    def __init__(self, image_right, image_left, matches):
        self.image_right = image_right
        self.image_left = image_left
        self.matches = matches 

    
    @property
    def image_right(self):
        return self._image_right


    @image_right.setter
    def image_right(self, value):
        self._image_right = value

    
    @property
    def image_left(self):
        return self._image_left


    @image_left.setter
    def image_left(self, value):
        self._image_left = value

    
    @property
    def matches(self):
        return self._matches

    
    @matches.setter
    def matches(self, value):
        self._matches = value

    
    @property
    def homography(self):
        return self._homography

    
    @homography.setter
    def homography(self, value):
        self._homography = value


    @property
    def result_image(self):
        return self._result_image

    
    @result_image.setter
    def result_image(self, value):
        self._result_image = value