import signal
from src.ImageHandler import ImageHandler

class Connector:
    """
    Connector class responsible for creating object for correct
    interaction between Robotino REST and Python software.
    """

    def __init__(self, robotino_ip: str = "192.168.0.1:80", params: dict = {'sid': 'default_setup'}):
        self.robotino_ip = "http://" + robotino_ip
        self.params = params
        self.run = True
        self.image_handler: ImageHandler
        self.drive_handler = None

    def signal_handler(self, sig, frame):
        """
        Initialization of signal handler which disconnect current system from Robotino REST service.
        :param sig:
        :param frame:
        :return: None
        """
        print('You pressed Ctrl+C!')
        self.run = False

    def init_signal_handler(self):
        """
        Initialization of signal handler.
        :return:
        """
        signal.signal(signal.SIGINT, self.signal_handler)

    def init_image_handler(self):
        """
        Initialization of ImageHandler class
        :return: ImageHandler class
        """
        self.image_handler = ImageHandler(robotino_ip=self.robotino_ip, params=self.params)

    @staticmethod
    def init_drive_handler():
        """
        Initialization of DriveHandler class
        :return: DriveHandler class
        """
        drive_handler = None
        return drive_handler
