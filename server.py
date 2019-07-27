from app.views import parse_images
from flask import Flask, request
from app.views import ServerException


app = Flask(__name__)


@app.errorhandler(ServerException)
def error_handler(error):
    return {'message': error.message}, 400


@app.route('/group', methods=['POST'])
def group_route():
    content = request.get_json()
    return parse_images(content['images'])


if __name__ == "__main__":
    app.run(port=8080)
