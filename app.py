# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, make_response, render_template, jsonify, request, Response
import cv2
import time
import numpy
import PoseModule as pm
import base64
import json

global startTime, startCountdown, data
startCountdown = False
startTime = 0

data=[]
# Flask constructor takes the name of 
# current module (__name__) as argument.
app = Flask(__name__)

def gen_frames():
    cap = cv2.VideoCapture(0)

    global out, capture, rec_frame, startCountdown, startTime

    detector = pm.PoseDetector()

    while True:
        success, img = cap.read()
        if success:
            img = detector.findPose(img)
            lmList = detector.getPosition(img)

            newTime = time.time()

            if startCountdown == True:
                cv2.putText(img, str(int(10-(newTime-startTime))), (250, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

                if int(10-(newTime-startTime)) == 0:
                    startCountdown = False
                    break

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

def start_timer():
    global startTime, startCountdown

    print("Hi")

    startTime = time.time()
    startCountdown = True


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
    return render_template('documentation.html', data = data)

@app.route('/demo/', methods = ['POST', 'GET'])
def demo():
    if request.method == 'POST':
        start_timer()
        return render_template('demo.html')
        # print("HI")
    else:
        return render_template('demo.html')

@app.route('/results', methods = ['POST', 'GET'])
def results():
    global data
    if request.method == 'POST':
        height = request.form.get("height")
        category = request.form.get("category")
        data = [height, category]
        return render_template('results.html', data = data)


cv2.destroyAllWindows()

# main driver function
if __name__ == '__main__':

    # run() method of Flask class runs the application 
    # on the local development server.
    app.run(debug=True)