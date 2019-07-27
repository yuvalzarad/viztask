from app.views import parse_images
from flask import Flask

app = Flask(__name__)


@app.route('/group')
def group_route():
    return parse_images([r'C:/temp/images/img (1).jpg', 'C:/temp/images/img (2).jpg'])


if __name__ == "__main__":
    app.run(port=8080)
