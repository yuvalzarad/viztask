import urllib
import requests
from PIL import Image as image
from app.models.match import Match
from app.config import AzureConfig


class Image(object):
    """Represents an input image to be parsed"""
    DETECT_URL = AzureConfig.REGION_URL + '/face/v1.0/detect?%s'

    def __init__(self, path):
        self.path = path
        with image.open(path) as opened_image:
            self.size = opened_image.size[0] * opened_image.size[1]

    def detect_faces(self):
        headers = {
            'Content-Type': 'application/octet-stream',
            'Ocp-Apim-Subscription-Key': AzureConfig.KEY,
        }

        params = urllib.urlencode({
            'returnFaceId': 'true',
            'returnFaceLandmarks': 'false',
        })

        # Sending a post request to obtain all of the face ids and face rectangles in the image
        image = open(self.path, 'rb')
        response = requests.post(Image.DETECT_URL % params, data=image, headers=headers)

        # Constructing all of the image's matches'
        matches = []
        for match in response.json():
            matches.append(Match(match['faceId'], match['faceRectangle'], self))

        return matches
