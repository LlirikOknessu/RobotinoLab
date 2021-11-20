import requests


class drive_handler:

    def __init__(self, Robotino_ip, params = {'sid': 'example_circle'}):

        """
        This method initialize Robot IP adress
        :param Robotino_ip: robot ip
        :param params: magic params from example on wiki.robotino.com
        """

        self.omnidrive_url = "http://" + Robotino_ip + "/data/omnidrive"
        self.params = params


    def set_speed(self, vel_x, vel_y, vel_w):
        vel_vect = [vel_x, vel_y, vel_w]
        request_result = requests.post(url = self.omnidrive_url, params = self.params, json= vel_vect)
        if request_result.status_code != requests.codes.ok:
            raise RuntimeError("Error: post to %s with params %s failed", self.omnidrive_url, self.params)
