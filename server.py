from app.views import parse_images
from flask import Flask

app = Flask(__name__)


@app.route('/group')
def group_route():
    return parse_images([r'C:/temp/images/family.jpg', 'C:/temp/images/family_girls.jpg'])


if __name__ == "__main__":
    app.run(port=8080)
