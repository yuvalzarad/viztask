# viztask
The server recieves in a post request a list of local paths to images.
Then, it searches for the most common face out of the photos.
It returns the path to the image for the face apearse the best, and the face rectangle in it.

## How to run?

```
pip install -r requirements.txt
python server.py
curl -i -X POST -H "Content-Type: application/json" -d "{\"images\": [\"images\\img (1).jpg\", \"images\\img (2).jpg\"]}" http://127.0.0.1:8080/group
```
