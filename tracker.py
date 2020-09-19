# python dynamic_color_tracking.py --filter HSV --webcam

import cv2
import argparse
import numpy as np
import pickle
from mainarduino import *


def callback(value):
    pass


def setup_trackbars(range_filter, filter_name):
    cv2.namedWindow(filter_name + "Trackbars", 0)

    for i in ["MIN", "MAX"]:
        v = 0 if i == "MIN" else 255

        for j in range_filter:
            cv2.createTrackbar("%s_%s_%s" %
                               (j, i, filter_name), filter_name + "Trackbars", v, 255, callback)


def get_trackbar_values(range_filter, filter_name):
    values = []

    for i in ["MIN", "MAX"]:
        for j in range_filter:
            v = cv2.getTrackbarPos("%s_%s_%s" %
                                   (j, i, filter_name), filter_name + "Trackbars")
            values.append(v)
    return values


def set_trackbar_values(last_value, filter_name):
    v1_min, v2_min, v3_min, v1_max, v2_max, v3_max = last_value
    cv2.setTrackbarPos('H_MIN_' + filter_name,
                       filter_name + "Trackbars", v1_min)
    cv2.setTrackbarPos('S_MIN_' + filter_name,
                       filter_name + "Trackbars", v2_min)
    cv2.setTrackbarPos('V_MIN_' + filter_name,
                       filter_name + "Trackbars", v3_min)
    cv2.setTrackbarPos('H_MAX_' + filter_name,
                       filter_name + "Trackbars", v1_max)
    cv2.setTrackbarPos('S_MAX_' + filter_name,
                       filter_name + "Trackbars", v2_max)
    cv2.setTrackbarPos('V_MAX_' + filter_name,
                       filter_name + "Trackbars", v3_max)


def main():

    # change camera setup here
    camera = cv2.VideoCapture(1)

    width = camera.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
    # print("width", width, "height", height)
    range_filter = 'HSV'
    setup_trackbars(range_filter, "Ball")
    cv2.createTrackbar("Focus", "BallTrackbars", 0, 255, callback)
    cv2.setTrackbarPos("Focus", "BallTrackbars", 90)

    centerX = 319
    centerY = 239
    is_ball_found = 0
    last_ball_posX = 0
    ballX = 0
    ballY = 0

    while True:
        # call kompas

        # print("Kompas = ", getKompas())

        # call kompas
        # print("Ir Sensor = ", getIR())

        focus = cv2.getTrackbarPos("Focus", "BallTrackbars")
        camera.set(28, focus)
        ret, image = camera.read()
        image = cv2.flip(image, 1)

        if not ret:
            break

        frame_to_thresh = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        kernel = np.ones((5, 5), np.uint8)

        #! find mask
        v1_min, v2_min, v3_min, v1_max, v2_max, v3_max = get_trackbar_values(
            range_filter, "Ball")

        thresh = cv2.inRange(
            frame_to_thresh, (v1_min, v2_min, v3_min), (v1_max, v2_max, v3_max))

        mask = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        #! find contours in the mask and initialize the current
        # (x, y) center of the ball
        cnts = cv2.findContours(
            mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None

        # only proceed if at least one contour was found
        if len(cnts) > 0:
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            ballX = center[0]
            ballY = center[1]

            # print("ballX = ", ballX, "ballY =", ballY)

            a = np.array((centerX, centerY))
            b = np.array((ballX, ballY))
            jarak = np.linalg.norm(a-b)
            print("jarak = " + str(int(jarak)))

            # only proceed if the radius meets a minimum size
            # print("radius :", radius)
            if radius > 5:
                is_ball_found = 1
                # draw the circle and centroid on the frame,
                # then update the list of tracked points
                cv2.circle(image, (int(x), int(y)),
                           int(radius), (0, 255, 255), 2)
                cv2.circle(image, center, 3, (0, 0, 255), -1)
                cv2.putText(
                    image, "Ball", (center[0]+10, center[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)
                cv2.putText(image, "("+str(center[0])+","+str(center[1])+")", (center[0] +
                                                                               10, center[1]+15), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)

        turn_speed = 150
        move_speed = 200
        slow_mode = 30
        is_ball_catch = getIR() is True or ballY >= 150 and ballY < 155

        # temukan ball
        # lek balé ketemu
        if is_ball_found and not is_ball_catch:
            last_ball_posX = ballX
            if (ballX > 300 and ballX < 330):
                # lek wes oleh bal mandek
                if ballY >= 150 and ballY < 155:
                    setMotor(0, 0)
                elif ballY < 150:
                    # fastmode
                    if(ballY < 150 - slow_mode):
                        setMotor(move_speed, move_speed)
                    else:
                        setMotor(move_speed / 2, move_speed / 2)

            # belok kiri
            if ballX < 300:
                # fastmode
                if(ballX < 300 - slow_mode):
                    setMotor(0, turn_speed, 20)
                else:
                    setMotor(0, 70, 20)
            # belok kanan
            elif ballX > 330:
                # fastmode
                if(ballX > 330 + slow_mode):
                    setMotor(turn_speed, 0, -20)
                else:
                    setMotor(70, 0, -20)

        if is_ball_catch and is_ball_found:
            if(getKompas() > 190 and getKompas() < 210):
                print("mandek")
                setMotor(0, 0, 0)
                tendang()
                break

            elif(getKompas() < 190):

                print("menggok kanan")

                setMotor(0, 0, -70)
            elif(getKompas() > 210):

                print("menggok kiri")

                setMotor(0, 0, 70)
            else:
                setMotor(0, 0)

                print("logic error")
        # show the frame to our screen
        cv2.imshow("Original", image)
        cv2.imshow("Mask", mask)

        # ? Ketika Tombol ditekan
        # S untuk save data
        # O untuk load data
        # esc untuk nutup program
        key = cv2.waitKey(1)
        if key == 27:
            break
        elif key == 115:
            pickle.dump(get_trackbar_values(range_filter, "Ball"),
                        open("values.dat", "wb"))
        elif key == 111:
            values = pickle.load(open("values.dat", "rb"))
            # print(values)
            set_trackbar_values(values, "Ball")


if __name__ == '__main__':
    main()
