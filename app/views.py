import requests
from models.image import Image

MAX_FACES = 1000
MIN_IMAGES_AMOUNT = 2

def group_matches(matches):
    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': '4b768946680148ff9935e53f375f36ce',
    }

    ids = [match.face_id for match in matches]
    data = {"faceIds": ids}

    url = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/group'
    response = requests.post(url, data=str(data), headers=headers)

    groups = response.json()['groups']
    if not groups:
        raise Exception("Not a single face match.")

    most_common_face = filter(lambda match: match.face_id in groups[0], matches)
    best_face = sorted(most_common_face)[0]

    return {'rectangle': best_face.rectangle, 'path': best_face.image.path}


def parse_images(images_paths):
    if len(images_paths) < MIN_IMAGES_AMOUNT:
        raise Exception("Must specify at least 2 images.")

    detected_faces = []
    for image_path in images_paths:
        detected_faces += Image(image_path).detect_faces()

    if len(detected_faces) > MAX_FACES:
        raise Exception("Can't process more than 1000 faces, current: {}".format(len(detected_faces)))

    return group_matches(detected_faces)
