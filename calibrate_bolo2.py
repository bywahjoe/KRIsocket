# python dynamic_color_tracking.py --filter HSV --webcam
from configku import *
import cv2
import argparse
import numpy as np
import pickle


def callback(value):
    pass


def setup_trackbars(range_filter, filter_name):
    cv2.namedWindow(filter_name + "Trackbars", 0)

    for i in ["MIN", "MAX"]:
        v = 0 if i == "MIN" else 255

        for j in range_filter:
            cv2.createTrackbar("%s_%s_%s" %
                               (j, i, filter_name), filter_name + "Trackbars", v, 255, callback)
    cv2.createTrackbar("Focus", filter_name + "Trackbars", 0, 255, callback)


def get_trackbar_values(range_filter, filter_name):
    values = []

    for i in ["MIN", "MAX"]:
        for j in range_filter:
            v = cv2.getTrackbarPos("%s_%s_%s" %
                                   (j, i, filter_name), filter_name + "Trackbars")
            values.append(v)

    values.append(cv2.getTrackbarPos("Focus", filter_name + "Trackbars"))
    return values


def set_trackbar_values(last_value, filter_name):
    v1_min, v2_min, v3_min, v1_max, v2_max, v3_max, focus = last_value
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
    cv2.setTrackbarPos("Focus", filter_name + "Trackbars", focus)


def main():
    # change camera setup here
    filter_name = "Bolo"
    camera = cv2.VideoCapture(MAIN_CAMERA,cv2.CAP_DSHOW)
    range_filter = 'HSV'
    setup_trackbars(range_filter, "Bolo")
    centerX = 319
    centerY = 239

    while True:

        focus = cv2.getTrackbarPos("Focus", filter_name + "Trackbars")
        camera.set(28, focus)
        ret, image = camera.read()
        image = cv2.flip(image, 1)

        if not ret:
            break

        frame_to_thresh = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        kernel = np.ones((5, 5), np.uint8)

        #! find mask bolo
        v1_min, v2_min, v3_min, v1_max, v2_max, v3_max, focus = get_trackbar_values(
            range_filter, "Bolo")

        thresh = cv2.inRange(
            frame_to_thresh, (v1_min, v2_min, v3_min), (v1_max, v2_max, v3_max))

        maskBolo = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        maskBolo = cv2.morphologyEx(maskBolo, cv2.MORPH_CLOSE, kernel)

        #! find contours in the mask and initialize the current
        # (x, y) center of the bolo
        cnts = cv2.findContours(
            maskBolo.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
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
            boloX = center[0]
            boloY = center[1]

            a = np.array((centerX, centerY))
            b = np.array((boloX, boloY))
            jarak_bolo = np.linalg.norm(a-b)
            jarak_bolo = int(jarak_bolo)
            print("jarak_bolo = " + str(jarak_bolo))

            # only proceed if the radius meets a minimum size
            if radius > 1:

                # draw the circle and centroid on the frame,
                # then update the list of tracked points
                cv2.circle(image, (int(x), int(y)),
                           int(radius), (0, 255, 255), 2)
                cv2.circle(image, center, 3, (0, 0, 255), -1)
                cv2.putText(
                    image, "Bolo", (center[0]+10, center[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)
                cv2.putText(image, "("+str(center[0])+","+str(center[1])+")", (center[0] +
                                                                               10, center[1]+15), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)

        # * show the frame to our screen
        cv2.imshow("Original", image)
        cv2.imshow("Mask", maskBolo)

        # * Ketika Tombol ditekan
        # S untuk save data
        # O untuk load data
        # r untuk reset
        # esc untuk nutup program
        key = cv2.waitKey(1)
        if key == 27:
            break
        elif key == 115:
            pickle.dump(get_trackbar_values(range_filter, filter_name),
                        open("data_bolo.dat", "wb"))
        elif key == 111:
            data_bolo = pickle.load(open("data_bolo.dat", "rb"))
            print(data_bolo)
            set_trackbar_values(data_bolo, filter_name)
        elif key == 114:
            # v1_min, v2_min, v3_min, v1_max, v2_max, v3_max, focus
            setValue = 0,0,0,255,255,255,80
            set_trackbar_values(setValue, filter_name)
            print('succes reset')

if __name__ == '__main__':
    main()
