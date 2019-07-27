from app.views import parse_images

if __name__ == "__main__":
    res = parse_images([r'C:/temp/images/family.jpg', 'C:/temp/images/family_girls.jpg'])
    print res