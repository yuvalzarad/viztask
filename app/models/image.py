import urllib
import requests
from PIL import Image as image
from app.models.match import Match


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
