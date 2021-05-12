import cv2
import math 
import time
from sys import exit
import numpy as np
from collections import deque



def test():
    

    cupPos = []
    ballPos = []


    t = 200
    time.sleep(2.0)

    try:
        while True:
            # Take each frame
            _, frame = vs.read()

            if frame is None:
                print("frame is none!")
                break
            gray = cv2.cvtColor(src = frame, code = cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(src = gray, 
                ksize = (5, 5), 
                sigmaX = 0)
            (t, binary) = cv2.threshold(src = blur,
                thresh = t, 
                maxval = 255, 
                type = cv2.THRESH_BINARY)


            (contours, hierarchy) = cv2.findContours(image = binary, 
                mode = cv2.RETR_TREE,
                method = cv2.CHAIN_APPROX_SIMPLE)


            # draw contours over original image
            cv2.drawContours(image = frame, 
                contours = contours, 
                contourIdx = -1, 
                color = (0, 255, 0), 
                thickness = 5)

            # print table of contours and sizes
            print("Found %d objects." % len(contours))
            for (i, c) in enumerate(contours):
                ((x1, y1), radius1) = cv2.minEnclosingCircle(c)
                # print("\tSize of contour %d: %d" % (i, len(c)))
                # print("\tRadious of contour %d: %d" % (i,radius1))

                if (170 <= radius1 * 2 <= 280):
                    print("\t-->Cup detected!")
                    cupPos.insert(0,[x1, y1, radius1])

                    cv2.circle(frame, (int(x1), int(y1)), int(radius1),
                    (138,43,226), thickness=15)

                if (24 <= radius1 * 2 <= 80):
                    print("\t-->Ball detected!")
                    ballPos.insert(0,[x1, y1, radius1])
                    cv2.circle(frame, (int(x1), int(y1)), int(radius1),
                    (255,127,80), thickness=15)

            # drawBallTracking(frame)
            checkBallInCup(cupPos, ballPos)
            # if (len(cupPos) > 1):
            #     cupPos.pop(0)
            # elif (len(ballPos) > 1):
            #     ballPos.pop(0)   
            
            
            cv2.namedWindow(winname = "output", flags = cv2.WINDOW_NORMAL)
            cv2.imshow(winname = "output", mat = frame)

            key = cv2.waitKey(1) & 0xFF

            # if the 'q' key is pressed, stop the loop
            if key == ord("q"):
                break
            #### Delay for 1 seconds ####
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("KeyboardInterrupt has been caught.")
        vs.release()
        cv2.destroyAllWindows()
        exit(0)


"""
    https://stackoverflow.com/questions/33490334/check-if-a-circle-is-contained-in-another-circle
"""
def checkBallInCup(cupPos, ballPos):
    print("checkBallInCup")
    if (len(cupPos) < 1 or len(ballPos) < 1):
        return
    cx, cy, cradious = cupPos[0]
    bx, by, bradious = ballPos[0]
    d = math.sqrt( (bx-cx)**2 + (by-cy)**2 )
    if (cradious > (d + bradious)):
        print("----- BALL IN CUP------")
        # TODO: UPDATE BOARD!!
    else:
        print("-----NOT ------")

    

if __name__ == "__main__":
    test()










# orangeBallColorLower = (4, 162,  98)		# Orange
# orangeBallColorUpper = (24, 182, 178)		# Orange
# pts = deque(maxlen=64)

# def drawBallTracking(frame):

#     blurred = cv2.GaussianBlur(frame, (11, 11), 0)
#     hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
#     mask = cv2.inRange(hsv, orangeBallColorLower, orangeBallColorUpper)
#     mask = cv2.erode(mask, None, iterations=2)
#     mask = cv2.dilate(mask, None, iterations=2)
#     cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
# 			cv2.CHAIN_APPROX_SIMPLE)
#     cnts = imutils.grab_contours(cnts)
#     center = None
#     if len(cnts) > 0:
#         # find the largest contour in the mask, then use
#         # it to compute the minimum enclosing circle and
#         # centroid
#         c = max(cnts, key=cv2.contourArea)
#         ((x, y), radius) = cv2.minEnclosingCircle(c)
#         M = cv2.moments(c)
#         center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

#         # only proceed if the radius meets a minimum size
#         if radius > 10:
#             # draw the circle and centroid on the frame,
#             # then update the list of tracked points
#             cv2.circle(frame, (int(x), int(y)), int(radius),
#                 (0, 255, 255), 2)
#             cv2.circle(frame, center, 5, (0, 0, 255), -1)
    
#     # update the points queue
#     pts.appendleft(center)
#     # loop over the set of tracked points
#     for i in range(1, len(pts)):
#         # if either of the tracked points are None, ignore
#         # them
#         if pts[i - 1] is None or pts[i] is None:
#             continue

#         # otherwise, compute the thickness of the line and
#         # draw the connecting lines
#         thickness = int(np.sqrt(64 / float(i + 1)) * 2.5)
#         cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

