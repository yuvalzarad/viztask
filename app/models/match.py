class Match(object):
    def __init__(self, face_id, rectangle, image):
        self.face_id = str(face_id)
        self.rectangle = rectangle
        self.image = image

    def _match_size(self):
        return self.rectangle['width'] * self.rectangle['height']

    def __lt__(self, other):
        return (self._match_size() / self.image.size) < (other._match_size() / self.image.size)
