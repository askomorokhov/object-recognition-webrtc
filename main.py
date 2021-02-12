import json
from typing import Optional

import uvicorn
from fastapi import Body, FastAPI, File, Form, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from PIL import Image

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get('/', response_class=HTMLResponse)
async def index():
    return '''
<html>
    <head>
        <title>Object Detection Statistics</title>
        <link rel="stylesheet" 
              href="https://unpkg.com/purecss@2.0.5/build/pure-min.css"
              integrity="sha384-LTIDeidl25h2dPxrB2Ekgc9c7sEC3CWGM6HeFmuDNUjX76Ert4Z4IY714dhZHPLd"
              crossorigin="anonymous">
    </head>
    <body>
        <center>
            <a class="pure-button pure-button-primary" href="/video">Video</a>
            <a class="pure-button pure-button-primary" href="/stats">Stats</a>
        </center>
    </body>
</html>
'''

@app.get('/stats', response_class=HTMLResponse)
async def stats():
    return '''
<html>
    <head>
        <title>Object Detection Statistics</title>
        <link rel="stylesheet" 
              href="https://unpkg.com/purecss@2.0.5/build/pure-min.css"
              integrity="sha384-LTIDeidl25h2dPxrB2Ekgc9c7sEC3CWGM6HeFmuDNUjX76Ert4Z4IY714dhZHPLd"
              crossorigin="anonymous">
    </head>
    <body>
    <center>
    <a class="pure-button pure-button-primary" href="/">Video</a>
    <a class="pure-button pure-button-primary" href="/stats">Stats</a>
    <table class="pure-table pure-table-horizontal">
    <thead>
        <tr>
            <th>#</th>
            <th>Object</th>
            <th>Count</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>1</td>
            <td>Book</td>
            <td>5</td>
        </tr>
        <tr>
            <td>2</td>
            <td>Person</td>
            <td>5</td>
        </tr>
        <tr>
            <td>3</td>
            <td>Plant Pot</td>
            <td>3</td>
        </tr>
    </tbody>
    </table>
    </center>
    </body>
</html>
'''


@app.get('/video', response_class=HTMLResponse)
async def video():
    return '''
<html>
    <head>
        <title>TensorFlow Object Detection</title>
        <link rel="stylesheet" 
              href="https://unpkg.com/purecss@2.0.5/build/pure-min.css"
              integrity="sha384-LTIDeidl25h2dPxrB2Ekgc9c7sEC3CWGM6HeFmuDNUjX76Ert4Z4IY714dhZHPLd"
              crossorigin="anonymous">
        <style>
            video {
                position: absolute;
                top: 0;
                left: 0;
                z-index: -1;
                /* Mirror the local video */
                transform: scale(-1, 1);            /* For Firefox (& IE) */
                -webkit-transform: scale(-1, 1);     /* For Chrome & Opera (& Safari) */
            }
            canvas{
                position: absolute;
                top: 0;
                left: 0;
                z-index:1
            }
        </style>
        <script src="https://webrtc.github.io/adapter/adapter-latest.js"></script>
    </head>
    <body>
        <video id="myVideo" autoplay></video>
    </body>
    <script id="objDetect" src="/static/objDetect.js" data-source="myVideo" data-mirror="true" data-uploadWidth="1280" data-scoreThreshold="0.40"></script>
</html>
'''


@app.post('/image')
async def image(threshold: float = Form(float), image: UploadFile = File(...)):
    image_object = Image.open(image.file)
    print(f'>>>>>> request, image size: {image_object.size}')
    obj_above_thresh = 0

    responce = []

    # Add some metadata to the output
    item = {
        'version': '0.0.1',
        'numObjects': int(obj_above_thresh),
        'threshold': threshold
    }
    responce.append(item)

    print(f'>>>>>> responce: {responce}')
    return {'resp': responce}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8008)
