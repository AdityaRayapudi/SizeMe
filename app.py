# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, make_response, render_template, jsonify, request, Response
import cv2
import time
import numpy
import PoseModule as pm
import base64
import json
import torch
from torch import nn

class NeuralNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        # self.flatten = nn.Flatten()
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(5, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 2),
        )

    def forward(self, x):
        # x = self.flatten(x)
        logits = self.linear_relu_stack(x)
        return logits


global startTime, startCountdown, data, measurments, model
startCountdown = False
startTime = 0
data = []

model = NeuralNetwork()
model.load_state_dict(torch.load("model.pth", weights_only=True))

# Flask constructor takes the name of 
# current module (__name__) as argument.
app = Flask(__name__)

def gen_frames():
    cap = cv2.VideoCapture(0)

    global out, capture, rec_frame, startCountdown, startTime, measurments

    detector = pm.PoseDetector()

    while True:
        success, img = cap.read()
        cv2.flip(img,1)
        if success:
            img = detector.findPose(img)
            lmList = detector.getPosition(img)

            newTime = time.time()

            if startCountdown == True:
                cv2.putText(img,str(int(10-(newTime-startTime))),(180,150),cv2.FONT_HERSHEY_COMPLEX,3,(255,255,255),16,cv2.LINE_AA)
                cv2.putText(img,str(int(10-(newTime-startTime))),(180,150),cv2.FONT_HERSHEY_COMPLEX,3,(0,0,0),4,cv2.LINE_AA)
                if int(10-(newTime-startTime)) == 0:
                    measurments = pm.Points(lmList)
                    startCountdown = False
                    break
            try:
                ret, buffer = cv2.imencode('.jpg', img)
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


    startTime = time.time()
    startCountdown = True

def predict_measurements(measurements, height, gender):
    height = float(height)
    gender = float(gender)

    conversion_rate = height / measurements[3]
    data = [[i * conversion_rate for i in measurements]]

    data[0].insert(0, gender)
    data[0][3] = height

    x_data = torch.tensor(data, dtype=torch.float32)
    predictions = model(x_data)
    print(x_data)
    print(predictions)


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
    global data, measurments
    if request.method == 'POST':
        height = request.form.get("height")
        category = request.form.get("category")
        predict_measurements(measurments, height, category)
        data = [height, category]
        return render_template('results.html', data = data)


cv2.destroyAllWindows()

# main driver function
if __name__ == '__main__':

    # run() method of Flask class runs the application 
    # on the local development server.
    app.run(debug=True)