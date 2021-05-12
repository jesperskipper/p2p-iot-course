import cv2
import time
import math
import logging
import chalk

TIME_THRESHOLD = 2.05

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



if __name__ == '__main__':
    away_cups = 6
    home_cups = 6   
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, 
            datefmt='%d-%b-%y %H:%M:%S'	) # datefmt="%H:%M:%S"
    logging.info("--> Main: Starting up server")
    logging.info("--> Main: Press Ctrl-C to exit")
    try:
        # vs = cv2.VideoCapture("./final140_0_white_cr.h264")
        # vs = cv2.VideoCapture("./videobeerwhite.h264")
        # vs = cv2.VideoCapture("./videobeerorange.h264")
        # vs = cv2.VideoCapture("./beerwhiteanglelow.h264")
        vs = cv2.VideoCapture("./beerwhiteangle.h264")
        # vs = cv2.VideoCapture("./beerorangeangle.h264")
        # vs = cv2.VideoCapture("./final140_0_orange_bic.h264")
        # vs = cv2.VideoCapture("./final140_0_white_bic.h264")
        # vs = cv2.VideoCapture("./final140_0_white_bic_cr.h264")
        t = 200
        cupPos = []
        ballPos = []
        time.sleep(2.0)
        start_bic = time.time()
        start_cr = time.time()
        loop_counter = 0
        while True:
            # Take each frame
            _, frame = vs.read()
            if frame is None:
                logging.info("--> Main: frame is none")
                break
            gray = cv2.cvtColor(src = frame, code = cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(src = gray, 
                ksize = (5, 5), 
                sigmaX = 0)
            (t, binary) = cv2.threshold(src = blur,
                thresh = t, 
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
                logging.info(chalk.magenta(f"--> Main.openCV.frame_i={loop_counter}: Size of contour and radious"))
                logging.info(chalk.magenta(f"--> Main.openCV.frame_i={loop_counter}: \t {i}, {len(c)}"))
                logging.info(chalk.magenta(f"--> Main.openCV.frame_i={loop_counter}: \t {i}, {radius1}"))
                # print("\tSize of contour %d: %d" % (i, len(c)))
                # print("\tRadious of contour %d: %d" % (i,radius1))

                ### OLD: 170 <= diamater <= 280
                # if (61 <= radius1 <= 83):
                if (170 <= radius1 * 2 <= 280):
                    # print("\t-->Cup detected!")
                    cupPos.insert(0,[x1, y1, radius1])

                    cv2.circle(frame, (int(x1), int(y1)), int(radius1),
                    (138,43,226), thickness=15)

                ### 24 <= radius1 * 2 <= 80
                # if (24 <= radius1 <= 48):
                if (24 <= radius1 * 2 <= 80):
                    # print("\t-->Ball detected!")
                    ballPos.insert(0,[x1, y1, radius1])
                    cv2.circle(frame, (int(x1), int(y1)), int(radius1),
                    (255,127,80), thickness=15)
            
            end_bic = time.time()
            time_elapsed_bic = end_bic - start_bic
            if ballInCup(cupPos, ballPos):
                logging.info(chalk.green(f"--> Main.openCV.frame_i={loop_counter}: Ball in cup"))
            else:
                logging.info(chalk.yellow(f"--> Main.openCV.frame_i={loop_counter}: Ball NOT in cup --------"))

            cv2.namedWindow(winname = "output", flags = cv2.WINDOW_NORMAL)
            cv2.imshow(winname = "output", mat = frame)

            
            key = cv2.waitKey(1) & 0xFF

            # if the 'q' key is pressed, stop the loop
            if key == ord("q"):
                break
            
            logging.info(chalk.red(f"--> Main.openCV.frame_i={loop_counter}: another round ended-------"))
            loop_counter += 1

            if (loop_counter >= 200):
                time.sleep(1.5)

            time.sleep(0.1)

    except KeyboardInterrupt:
        print("Stopping python server")



