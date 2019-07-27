import requests
from models.image import Image
from config import AzureConfig

MAX_DETECTED_FACES = 1000
MIN_IMAGES_AMOUNT = 2
GROUP_URL = AzureConfig.REGION_URL + '/face/v1.0/group'


class ServerException(Exception):
    pass


def group_matches(matches):
    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': AzureConfig.KEY,
    }

    # Sending a post request to group all the faces according to their similarity
    ids = [match.face_id for match in matches]
    data = {"faceIds": ids}
    response = requests.post(GROUP_URL, data=str(data), headers=headers)

    groups = response.json()['groups']
    if not groups:
        raise ServerException("Not a single face match.")

    # 'groups' field is ordered by size, therefore the first group will contain the most common face.
    # Filtering it into a list of Matches where it appears, and sorting it according to face-to-image ratio.
    most_common_face = filter(lambda match: match.face_id in groups[0], matches)
    best_face = sorted(most_common_face)[0]

    return {'rectangle': best_face.rectangle, 'path': best_face.image.path}


def parse_images(images_paths):
    if len(images_paths) < MIN_IMAGES_AMOUNT:
        raise ServerException("Must specify at least {} images.".format(MIN_IMAGES_AMOUNT))

    # Parsing all of the images into a Match list
    detected_faces = []
    for image_path in images_paths:
        detected_faces += Image(image_path).detect_faces()

    if len(detected_faces) > MAX_DETECTED_FACES:
        raise ServerException("Can't process more than {} faces, current: {}".format(MAX_DETECTED_FACES,
                                                                                     len(detected_faces)))

    return group_matches(detected_faces)
