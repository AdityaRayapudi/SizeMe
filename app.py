# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, make_response, render_template, jsonify, request, Response
import cv2
import time
import numpy
import PoseModule as pm
import base64
import json

data=[
    {
        'name':'Audrin',
        'place': 'kaka',
        'mob': '7736'
    },
    {
        'name': 'Stuvard',
        'place': 'Goa',
        'mob' : '546464'
    }
]
# Flask constructor takes the name of 
# current module (__name__) as argument.
app = Flask(__name__)

def gen_frames():
    cap = cv2.VideoCapture(0)

    global out, capture,rec_frame
    detector = pm.PoseDetector()

    while True:
        success, img = cap.read()
        if success:
            img = detector.findPose(img)
            lmList = detector.getPosition(img)

            try:
                ret, buffer = cv2.imencode('.jpg', cv2.flip(img,1))
                img = buffer.tobytes()
                yield (b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')
                
            except Exception as e:
                pass

    else:
        pass
        # cv2.imshow("Image", img)

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# The route() function of the Flask class is a decorator, 
# which tells the application which URL should call 
# the associated function.
@app.route('/')
def index():
    return render_template('index.html', data = data)

@app.route('/doc')
def doc():
    return render_template('doc.html', data = data)

@app.route('/demo')
def demo():
    return render_template('demo.html', data = data)

@app.route('/camera')
def camera():
    return render_template('camera.html', data = data)

@app.route('/button', methods=['GET', 'POST'])
def button():
    if request.method == 'POST':
        data = request.form
        return 'Data received successfully'
    return '''
        <form method="post">
            <input type="text" name="data">
            <input type="submit" value="Submit">
        </form>
    '''


cv2.destroyAllWindows()

# main driver function
if __name__ == '__main__':

    # run() method of Flask class runs the application 
    # on the local development server.
    app.run(debug=True)