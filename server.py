import json
import urllib
import requests

from pprint import pprint
from os.path import expanduser
import PIL.Image as image

class Image(object):
    def __init__(self, path):
        self.path = path
        with image.open(path) as pil_image:
            self.size = pil_image.size[0] * pil_image.size[1]

    def detect_faces(self):
        headers = {
            'Content-Type': 'application/octet-stream',
            'Ocp-Apim-Subscription-Key': '4b768946680148ff9935e53f375f36ce',
        }

        params = urllib.urlencode({
            'returnFaceId': 'true',
            'returnFaceLandmarks': 'false',
            'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses',
        })

        url = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect?%s' % params

        image = open(self.path, 'rb')
        response = requests.post(url, data=image, headers=headers)

        matches = []
        for match in response.json():
            matches.append(Match(match['faceId'], match['faceRectangle'], self))

        return matches


class Match(object):
    def __init__(self, face_id, rectangle, image):
        self.face_id = face_id
        self.rectangle = rectangle
        self.image = image

    def _match_size(self):
        return self.rectangle['width'] * self.rectangle['height']

    def __lt__(self, other):
        return (self._match_size() / self.image.size) < (other._match_size() / self.image.size)


class Face(object):
    def __init__(self, face_id, rectangle, image_path):
        self.matches = [Match(face_id, rectangle, image_path)]

    def __eq__(self, other):
        if not isinstance(other, Face):
            return False
        # Verify for all the matches

    def __iadd__(self, other):
        self.matches += other.matches


def main():
    pass

if __name__ == "__main__":
    main()