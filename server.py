import requests

from azure_face_api.image import Image


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
    res = parse_images([r'C:/temp/images/family.jpg', 'C:/temp/images/family_girls.jpg'])
    print res