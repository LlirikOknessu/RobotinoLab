import time

from src.DriveHandler import DriveHandler
from src.Connector import Connector
from src.speedCalculator import SpeedCalculator
from src.ImageHandler import ImageHandler

connection = Connector()

drive = DriveHandler(connection.robotino_ip, connection.params)

imHnd = ImageHandler(connection.robotino_ip, connection.params)

motion_T = 4

spCalc = SpeedCalculator(motion_T)

elapsed_time = 0.0

dt = 0.05

t0 = time.perf_counter()
while not drive.is_stop_condition():
    [x, y, phi] = imHnd.get_out_point_coords(video_show=True)

    time.sleep(dt)
    drive.set_speed(0.1, 0.0, 0.3 * phi * phi * phi)
drive.set_speed(0, 0, 0)
print(elapsed_time)