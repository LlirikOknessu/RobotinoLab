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

        return angle/self.dt

    def calc_speed(self, x_ref, y_ref, angle):
        omega = self.calc_rotation_speed(angle)

        transition_mat = np.matrix([np.sin(angle)/omega, -(1 - np.cos(angle))/omega], [(1 - np.cos(angle))/omega, np.sin(angle)/omega])
        ref_position = np.matrix([x_ref], [y_ref])
        ref_speed = np.matmul(np.linalg.inv(transition_mat), ref_position)

        return [ref_speed[0], ref_speed[1], omega]

