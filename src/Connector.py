import signal


class Connector:
    """
    Connector class responsible for creating object for correct
    interaction between Robotino REST and Python software.
    """
    def __init__(self, robotino_ip: str = "192.168.0.1:80"):
        self.robotino_ip = robotino_ip
        self.run = True

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

    @staticmethod
    def init_image_handler():
        """
        Initialization of ImageHandler class
        :return: ImageHandler class
        """
        image_handler = None
        return image_handler

    @staticmethod
    def init_drive_handler():
        """
        Initialization of DriveHandler class
        :return: DriveHandler class
        """
        drive_handler = None
        return drive_handler
