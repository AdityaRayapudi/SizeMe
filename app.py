# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, make_response, render_template, request, Response
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
cap = cv2.VideoCapture(0)

cap.release()


# The route() function of the Flask class is a decorator, 
# which tells the application which URL should call 
# the associated function.
@app.route('/')
def index():
    return render_template('index.html', data = data)
@app.route('/doc/')
def doc():
    return render_template('doc.html', data = data)
@app.route('/demo/')
def demo():
    return render_template('demo.html', data = data)
@app.route('/camera/')
def camera():
    return render_template('camera.html', data = data)
'''''
@app.route('/video_feed/')
def genframes():
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            pTime = 0
            fullTime = 100000000000000
            startCountdown = False
            newTime = 0
            startTime = time.time()
            detector = pm.PoseDetector()
            buttonPress = 0
            success, img = cap.read()
            img = detector.findPose(img)
            lmList = detector.getPosition(img)
            print(lmList)
            cTime = time.time()
            fps = 1 / (cTime - pTime)
            pTime = cTime
            if startCountdown:
                newTime = time.time()
                cv2.putText(img, str(int(10-(newTime-startTime))), (250, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
            if cv2.waitKey(1) & 0xFF == ord(' '):
                if buttonPress == 0:
                    startTime = time.time()
                    buttonPress = 1
                startCountdown = True
                fullTime = cTime + 10
                newTime = startTime
                time.process_time()
            if cTime >= fullTime:
                break
            cv2.imshow("Image", img)
            if not cap.isOpened():
                print("error: could not open with cap index {cap_index}")
                capIndex += 1
                continue
            else:
                print("opened")
        success, frame = cap.read()
        ret, buffer = cv2.imencode('.jpg', img)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    cap.release()
    cv2.destroyAllWindows()
    return render_template('/camera/', data = data)
'''



def getFrames(img):
    pass

@app.route('/video', methods=['POST', 'GET'])
def video():
    if request.method == 'PUT':
        load = json.loads(request.json)
        imdata = base64.b64decode(load['image'])
        respose = make_response(imdata.tobytes())
        return respose

@app.route('/cmd')
def cmd():
    pass
# main driver function
if __name__ == '__main__':

    # run() method of Flask class runs the application 
    # on the local development server.
    app.run(debug=True)