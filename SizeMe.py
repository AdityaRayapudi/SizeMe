import cv2
import time
import PoseModule as pm

cap = cv2.VideoCapture(0)
pTime = 0
fullTime = 100000000000000
startCountdown = False
newTime = 0
detector = pm.PoseDetector()
buttonPress = 0
while True:
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
        finalPoints = lmList
        break
    
    cv2.imshow("Image", img)
cap.release()
cv2.destroyAllWindows()
measurements = pm.Points(finalPoints)
print(measurements)