class Match(object):
    """Represents a face detected in a certain image"""
    def __init__(self, face_id, rectangle, image):
        self.face_id = str(face_id)
        self.rectangle = rectangle
        self.image = image

    def _match_size(self):
        return self.rectangle['width'] * self.rectangle['height']

    def __lt__(self, other):
        return (float(self._match_size()) / self.image.size) < (float(other._match_size()) / self.image.size)
