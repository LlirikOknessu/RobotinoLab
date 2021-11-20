import requests


class drive_handler:

    def __init__(self, Robotino_ip, params={'sid': 'example_circle'}):
        """
        This method initialize Robot IP adress
        :param Robotino_ip: robot ip
        :param params: magic params from example on wiki.robotino.com
        """

        self.omnidrive_url = "http://" + Robotino_ip + "/data/omnidrive"
        self.bumper_url = "http://" + Robotino_ip + "/data/bumper"
        self.params = params

    def set_speed(self, vel_x, vel_y, vel_w):
        vel_vect = [vel_x, vel_y, vel_w]
        request_result = requests.post(url=self.omnidrive_url, params=self.params, json=vel_vect)
        if request_result.status_code != requests.codes.ok:
            raise RuntimeError("Error: post to %s with params %s failed", self.omnidrive_url, self.params)

    def check_bumper_state(self):
        request_result = requests.get(url=self.bumper_url, params=self.params)
        if (request_result.status_code != requests.codes.ok):
            raise RuntimeError("Error: post to %s with params %s failed", self.omnidrive_url, self.params)
        else:
            data = request_result.json()
            return data["value"]

    def is_stop_condition(self):
        return self.check_bumper_state()
    