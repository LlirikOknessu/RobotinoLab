import requests
import numpy as np
import math
from typing import List
import cv2
import time
import os


class ImageHandler:
    IMAGE_PATH = "/cam0/"
    INITIAL_POINT = (320, 32)

    def __init__(self, robotino_ip: str, params: dict):
        """
        Initializing image handler
        :param robotino_ip: IP address of the Robotino
        :param params:
        """
        self.robotino_ip = robotino_ip
        self.params = params
        self.image_robotino_url = self.robotino_ip + self.IMAGE_PATH

    def get_image(self):
        """
        Gets image from camera
        :return: cv2 image
        """
        r = requests.get(url=self.image_robotino_url, params=self.params, stream=True)
        image = np.asarray(bytearray(r.raw.read()), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        if r.status_code == requests.codes.ok:
            data = image
            return data
        else:
            raise RuntimeError("Error: get from %s with params %s failed", self.image_robotino_url, self.params)

    def video_capture(self):
        """
        Show filtered image with initial and output points
        :return: None
        """
        while True:
            image = self.get_image()
            cnt, th_image, adapt_thresh_image = self._find_contours(image)
            self._draw_points(cards_coordinates=self._find_coordinates(cnt), image=image)
            cv2.imshow('image', image)
            cv2.imshow('thresh_image', th_image)
            cv2.imshow('adapt_thresh_image', adapt_thresh_image)
            cv2.waitKey(1)
            time.sleep(0.2)
            if cv2.waitKey(25) == ord('q'):
                # do not close window, you want to show the frame
                cv2.destroyAllWindows()
                break

    def _find_contours(self, image):
        """
        Filter image
        :param image: Initial image
        :return: Filtered image
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.medianBlur(gray, 5)
        T, thresh_image = cv2.threshold(blurred, 90, 255,
                                        cv2.THRESH_BINARY_INV)
        adapt_thresh_image = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,
                                                   5, 15)

        (cnts, hierarchy) = cv2.findContours(adapt_thresh_image,
                                             cv2.RETR_TREE,
                                             cv2.CHAIN_APPROX_SIMPLE)
        return cnts, thresh_image, adapt_thresh_image

    def _find_coordinates(self, cnts):
        """
        Find output coordinates
        :param cnts: Calculated image contours
        :return: Initial point and output point coordinates
        """
        cards_coordinates = []
        for i in range(0, len(cnts)):
            vx, vy, x, y = cv2.fitLine(cnts[i], cv2.DIST_L2, 0, 0.2, 0.1)
            if y > 80 and y < 300 and x > 150:
                cards_coordinates.append((x, y))
                out_coords = min(cards_coordinates, key=lambda x: x[1])

        return [self.INITIAL_POINT, out_coords]

    def _draw_points(self, cards_coordinates, image):
        """
        Draw all points
        :param cards_coordinates: point coordinates
        :param image: video image
        :return: drew image
        """
        for cards_coordinate in cards_coordinates:
            cv2.circle(image, (int(cards_coordinate[0]), int(cards_coordinate[1])), 5, (255, 255, 0), -1)
        return image

    def _get_points(self, out_pix_point: tuple) -> (float, float, float):
        """
        Calculates coordinates of output point and angle of the robotino
        :param out_pix_point: output point X and Y coordinates in meters
        :return: x: x coordinate in meters,
                y: y coordinate in meters,
                theta: a numeric value between -PI/2 and PI/2 radians
        """
        out_coords = ((out_pix_point[0] * 0.0035) - 0.56, (out_pix_point[1] - 32) * 0.0011475)
        x = out_coords[0]
        y = out_coords[1]
        theta = math.atan(x / y)
        return x, y, theta

    def _parse_image(self, image) -> (float, float, float):
        cnt, th_image, adapt_thresh_image = self._find_contours(image)
        points = self._find_coordinates(cnt)
        out_pix_point = points[1]
        print(out_pix_point)
        return self._get_points(out_pix_point)

    def get_out_point_coords(self, video_show: bool = False) -> (float, float, float):
        """

        :param video_show: if True show the video with initial and output points
        :return: x: x coordinate in meters,
                y: y coordinate in meters,
                theta: a numeric value between -PI/2 and PI/2 radians
        """
        image = self.get_image()
        if video_show > 0:
            cnt, th_image, adapt_thresh_image = self._find_contours(image)
            self._draw_points(cards_coordinates=self._find_coordinates(cnt), image=image)
            cv2.imshow('image', image)
            cv2.waitKey(1)
            time.sleep(0.2)
            if cv2.waitKey(25) == ord('q'):
                # do not close window, you want to show the frame
                cv2.destroyAllWindows()
        return self._parse_image(image=image)
