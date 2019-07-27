import urllib
import requests
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
        self.face_id = str(face_id)
        self.rectangle = rectangle
        self.image = image

    def _match_size(self):
        return self.rectangle['width'] * self.rectangle['height']

    def __lt__(self, other):
        return (self._match_size() / self.image.size) < (other._match_size() / self.image.size)


def group_matches(matches):
    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': '4b768946680148ff9935e53f375f36ce',
    }

    ids = [match.face_id for match in matches]
    data = {"faceIds": ids}

    url = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/group'
    response = requests.post(url, data=str(data), headers=headers)

    most_common_face = filter(lambda match: match.face_id in response.json()['groups'][0], matches)
    best_face = sorted(most_common_face)[0]

    return {'rectangle': best_face.rectangle, 'path': best_face.image.path}


def parse_images(images_paths):
    detected_faces = []
    for image_path in images_paths:
        detected_faces += Image(image_path).detect_faces()

    return group_matches(detected_faces)



if __name__ == "__main__":
    pass