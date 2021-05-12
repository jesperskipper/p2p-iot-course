
import cv2
import time
import math

from math import trunc 

TIME_THRESHOLD = 2.05

class DetectOpenCV(object):
    def __init__(self):
        self.vs = cv2.VideoCapture("./beertwhitetop.h264")
        self.t = 200
        self.mainLoop = True

    def stopMainLoop(self):
        self.mainLoop = False
        
    def runMainLoop(self, callback):
        cupPos = []
        ballPos = []
        time.sleep(2.0)
        start = time.time()
        while self.mainLoop:
            # Take each frame
            _, frame = self.vs.read()
            if frame is None:
                print("frame is none!")
                break
            gray = cv2.cvtColor(src = frame, code = cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(src = gray, 
                ksize = (5, 5), 
                sigmaX = 0)
            (t, binary) = cv2.threshold(src = blur,
                thresh = self.t, 
                maxval = 255, 
                type = cv2.THRESH_BINARY)
            (contours, _) = cv2.findContours(image = binary, 
                mode = cv2.RETR_TREE,
                method = cv2.CHAIN_APPROX_SIMPLE)
            # draw contours over original image
            cv2.drawContours(image = frame, 
                contours = contours, 
                contourIdx = -1, 
                color = (0, 255, 0), 
                thickness = 5)
            for (i, c) in enumerate(contours):
                ((x1, y1), radius1) = cv2.minEnclosingCircle(c)
                # print("\tSize of contour %d: %d" % (i, len(c)))
                # print("\tRadious of contour %d: %d" % (i,radius1))

                if (170 <= radius1 * 2 <= 280):
                    # print("\t-->Cup detected!")
                    cupPos.insert(0,[x1, y1, radius1])

                    cv2.circle(frame, (int(x1), int(y1)), int(radius1),
                    (138,43,226), thickness=15)

                if (24 <= radius1 * 2 <= 80):
                    # print("\t-->Ball detected!")
                    ballPos.insert(0,[x1, y1, radius1])
                    cv2.circle(frame, (int(x1), int(y1)), int(radius1),
                    (255,127,80), thickness=15)
            
            end = time.time()
            time_elapsed = end - start
            if ballInCup(cupPos, ballPos):
                if time_elapsed > TIME_THRESHOLD:
                    # print("ball in cup Above")
                    # eventType, teamName, score
                    callback("BIC", "HOME", 2)
                    start = end; # update so ww wait again.

            key = cv2.waitKey(1) & 0xFF

            # if the 'q' key is pressed, stop the loop
            if key == ord("q"):
                break


    def shutdown(self):
        self.vs.release()
        cv2.destroyAllWindows()


"""
    https://stackoverflow.com/questions/33490334/check-if-a-circle-is-contained-in-another-circle
"""
def ballInCup(cupPos, ballPos):
    # print("checkBallInCup")
    if (len(cupPos) < 1 or len(ballPos) < 1):
        return
    cx, cy, cradious = cupPos[0]
    bx, by, bradious = ballPos[0]
    d = math.sqrt( (bx-cx)**2 + (by-cy)**2 )
    if (cradious > (d + bradious)):
        return True;
    else:
        return False;
