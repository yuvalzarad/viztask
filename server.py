from app.views import parse_images
from flask import Flask, request

app = Flask(__name__)


@app.route('/group', methods=['POST'])
def group_route():
    content = request.get_json()
    return parse_images(content['images'])


if __name__ == "__main__":
    app.run(port=8080)
