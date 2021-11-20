import requests
import numpy as np
import cv2



class ImageHandler:
    IMAGE_PATH = "/cam0/"

    def __init__(self, robotino_ip: str, params: dict):
        self.robotino_ip = robotino_ip
        self.params = params
        self.image_robotino_url = self.robotino_ip + self.IMAGE_PATH

    def get_image(self):
        r = requests.get(url=self.image_robotino_url, params=self.params, stream=True)
        image = np.asarray(bytearray(r.raw.read()), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        if r.status_code == requests.codes.ok:
            data = image
            return data
        else:
            raise RuntimeError("Error: get from %s with params %s failed", self.image_robotino_url, self.params)

    def video_capture(self):
        while True:
            image = self.get_image()
            cv2.imshow('image', image)
            cv2.waitKey(1)
            if cv2.waitKey(25) == ord('q'):
                # do not close window, you want to show the frame
                cv2.destroyAllWindows()
                break

    def _parse_image(self):
        pass
