import cv2
import mediapipe as mp
import time
import math

class PoseDetector:

    def __init__(self, mode = False, upBody = False, smooth=True, detectionCon = 0.5, trackCon = 0.5):

        self.mode = mode
        self.upBody = upBody
        self.smooth = smooth
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(static_image_mode=self.mode, 
            smooth_landmarks=self.smooth, 
            min_detection_confidence=self.detectionCon, 
            min_tracking_confidence=self.trackCon)

    def findPose(self, img, draw=True):
        #imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(img)
        #print(self.results.pose_landmarks)
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)

        return img

    def getPosition(self, img, draw=True):
        lmList= []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                #print(id, lm)
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
            if draw:
                cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
        return lmList
    
def Points(Points):
    shoulderWidth = math.dist([Points[11][1], 0], [Points[12][1], 0])
    rightArm = math.dist(Points[12][1:], Points[14][1:])+math.dist(Points[14][1:], Points[16][1:])
    height = Points[32][2]-Points[0][2]
    shoulderToWaist = math.dist([0, Points[11][2]], [0, Points[23][2]])
    print("Shoulder Width: ", shoulderWidth)
    print("Shoulder to Waist Length: ", shoulderToWaist)
    print("Right Arm: ", rightArm)
    print("Height: ", height)
    return [shoulderWidth,rightArm,shoulderToWaist,height]