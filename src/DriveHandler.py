import requests


class DriveHandler:

    def __init__(self, robotino_ip, params={'sid': 'example_circle'}):
        """
        This method initialize Robot IP adress
        :param Robotino_ip: robot ip
        :param params: magic params from example on wiki.robotino.com
        """

        self.OMNIDRIVE_PATH = "/data/omnidrive"
        self.BUMPER_PATH = "/data/bumper"

        self.ADDRRES_PREAMBLE = "http://"

        self.omnidrive_url = self.ADDRRES_PREAMBLE + robotino_ip + self.OMNIDRIVE_PATH
        self.bumper_url = self.ADDRRES_PREAMBLE + robotino_ip +  self.BUMPER_PATH
        self.params = params

    def set_speed(self, vel_x, vel_y, vel_w):

        """
        This function sends velocity references to robot

        :param vel_x: ref velocity in local x coordinate
        :param vel_y: ref velocity in local y coordinate
        :param vel_w: ref rotation velocity around local z axis
        :return:
        """

        vel_vect = [vel_x, vel_y, vel_w]
        request_result = requests.post(url=self.omnidrive_url, params=self.params, json=vel_vect)
        if request_result.status_code != requests.codes.ok:
            raise RuntimeError("Error: post to %s with params %s failed", self.omnidrive_url, self.params)

    def check_bumper_state(self):

        """
        This function check if bumper was pressed
        :return:
        """

        request_result = requests.get(url=self.bumper_url, params=self.params)
        if request_result.status_code != requests.codes.ok:
            raise RuntimeError("Error: post to %s with params %s failed", self.omnidrive_url, self.params)
        else:
            data = request_result.json()
            return data["value"]

    def is_stop_condition(self):

        """
        This calculates stop criterion
        :return: Is stop criterion being met
        """

        return self.check_bumper_state()
