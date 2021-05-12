from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
    help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
    help="max buffer size")
args = vars(ap.parse_args())
match_score = (0, 0)
greenLower = (36, 25, 25)
greenUpper = (70, 255,255)
pts = deque(maxlen=args["buffer"])
x=0
y=0

if not args.get("video", False):
    vs = VideoStream(src=0).start()
else:
    vs = cv2.VideoCapture(args["video"])
time.sleep(2.0)
while True:
    frame = vs.read()
    frame = frame[1] if args.get("video", False) else frame
    if frame is None:
        break
    frame = imutils.resize(frame, width=640, height=480)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, greenLower, greenUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = None
    cv2.rectangle(frame,(0,0),(640,360),(0,255,255),7)
    cv2.rectangle(frame,(8,135),(14,225),(255,0,0),2)
    cv2.rectangle(frame,(623,140),(630,230),(255,0,0),2)
    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        if radius > 5:
            cv2.circle(frame, (int(x), int(y)), int(radius),
                (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
    pts.appendleft(center)
    for i in range(1, len(pts)):
        if pts[i - 1] is None or pts[i] is None:
            continue
        thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
        cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)
    '''
    for i in range(1, len(pts)):

        if (8 < x < 14 and 135 < y < 225) :
            cv2.putText(frame,"Goal!" , (300, 200), cv2.FONT_HERSHEY_SIMPLEX, 3, (120, 255, 50), 10)

    for i in range(1, len(pts)):
        if (623 < x < 630 and 140 < y < 230) :
            cv2.putText(frame,"Goal!" , (100, 200), cv2.FONT_HERSHEY_SIMPLEX, 3, (120, 255, 50), 10)
    '''
    for i in range(1, len(pts)):
        #if pts[i - 1] == pts[i] :
        if (8 < x < 14 and 135 < y < 225) :
            match_score = (match_score[0] + 1, match_score[1])
            break
        if (623 < x < 630 and 140 < y < 230) :
            match_score = (match_score[0], match_score[1] + 1)
            break

    cv2.putText(frame, str(x) + " , " + str(y),
        (10, frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX,
        0.5, (0, 0, 255), 1)

    cv2.putText(frame, str(match_score[0]) + " - " + str(match_score[1]), (260, 60), 
        cv2.FONT_HERSHEY_SIMPLEX, 1, (120, 255, 50), 2)
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    counter += 1
    if key == ord("q"):
        break
if not args.get("video", False):
    vs.stop()
else:
    vs.release()
cv2.destroyAllWindows()