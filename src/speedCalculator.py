import numpy as np

class SpeedCalculator:

    def __init__(self, sampleTime):

        """
        this function initializes speenCalc

        :param sampleTime: sysrem sample time
        """

        self.dt = sampleTime

    def __calc_rotation_speed(self, angle):

        """
        This function calculates reference speed of robot rotation atound Z axit
        :param angle: angle which robot need to turn
        :return:
        """

        return angle*angle*angle/self.dt

    def calc_speed(self, x_ref, y_ref, angle):

        if angle < 0.1 and angle > -0.1:
            vx = x_ref[0]/self.dt
            vy = 0.0
            omega = 0.0
        else:
            omega = self.__calc_rotation_speed(angle)

            transition_mat = np.matrix([[np.sin(angle)/omega, -(1 - np.cos(angle))/omega], [(1 - np.cos(angle))/omega, np.sin(angle)/omega]])
            ref_position = np.matrix([x_ref, y_ref])
            print(transition_mat)
            ref_speed = np.matmul(np.linalg.inv(transition_mat), ref_position)
            vx = ref_speed[0, 0]
            vy = ref_speed[1, 0]

        return [2*vx, 2*vy, omega]

