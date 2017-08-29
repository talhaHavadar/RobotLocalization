"""
MIT License

Copyright (c) 2017 Talha Can Havadar

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

@author Talha Can Havadar (talhaHavadar)
"""
import random
from math import pi, exp, sqrt, cos, sin
from resampling import ResamplingWheel

class Robot(object):
    """
    The class that helps to simulate the robot behaviours
    Sebastian Thrun's Robot implementation used as reference and improved by Talha Havadar.
    """
    world_size = 100.0
    landmarks  = [[20.0, 20.0], [80.0, 80.0], [20.0, 80.0], [80.0, 20.0]]

    def __init__(self):
        self.x = random.random() * Robot.world_size
        self.y = random.random() * Robot.world_size
        self.orientation = random.random() * 2.0 * pi
        self.forward_noise = 0.0
        self.turn_noise = 0.0
        self.sense_noise = 0.0

    @staticmethod
    def set_world_size(size):
        """
        Sets the world size of the robot
        """
        if size < 0:
            raise ValueError("World size must be greater than 0.")
        Robot.world_size = size

    @staticmethod
    def set_landmarks(lmarks):
        """
        Sets the landmarks for the world 
        """
        size = len(lmarks)
        if size <= 0 and isinstance(lmarks, list):
            raise ValueError("Landmarks size needs to be greater than zero and needs to be a list.")
        Robot.landmarks = lmarks

    def set(self, new_x, new_y, new_orientation):
        """
        Sets the position and orientation of the robot
        """
        if new_x < 0 or new_x >= Robot.world_size:
            raise ValueError('X coordinate out of bound')
        if new_y < 0 or new_y >= Robot.world_size:
            raise ValueError('Y coordinate out of bound')
        if new_orientation < 0 or new_orientation >= 2 * pi:
            raise ValueError('Orientation must be in [0..2pi]')
        self.x = float(new_x)
        self.y = float(new_y)
        self.orientation = float(new_orientation)


    def set_noise(self, new_f_noise, new_t_noise, new_s_noise):
        """
        makes it possible to change the noise parameters
        this is often useful in particle filters
        """
        self.forward_noise = float(new_f_noise)
        self.turn_noise = float(new_t_noise)
        self.sense_noise = float(new_s_noise)

    def sense(self):
        """
        Simulates the sensor behaviour and
        returns the measurement according to landmarks
        """
        z_vals = []
        for i in range(len(Robot.landmarks)):
            dist = sqrt((self.x - Robot.landmarks[i][0]) ** 2 + (self.y - Robot.landmarks[i][1]) ** 2)
            dist += random.gauss(0.0, self.sense_noise)
            z_vals.append(dist)
        return z_vals


    def move(self, turn, forward):
        if forward < 0:
            raise ValueError('Robot cant move backwards')
        
        # turn, and add randomness to the turning command
        orientation = self.orientation + float(turn) + random.gauss(0.0, self.turn_noise)
        orientation %= 2 * pi

        # move, and add randomness to the motion command
        dist = float(forward) + random.gauss(0.0, self.forward_noise)
        x = self.x + (cos(orientation) * dist)
        y = self.y + (sin(orientation) * dist)
        x %= Robot.world_size    # cyclic truncate
        y %= Robot.world_size

        # set particle
        res = Robot()
        res.set(x, y, orientation)
        res.set_noise(self.forward_noise, self.turn_noise, self.sense_noise)
        return res

    @staticmethod
    def gaussian(mu, sigma, x):
        """
        Calculates the probability of x for 1-dim Gaussian with mean mu and var. sigma
        """
        return exp(- ((mu - x) ** 2) / (sigma ** 2) / 2.0) / sqrt(2.0 * pi * (sigma ** 2))


    def measurement_prob(self, measurement):
        """
        calculates how likely a measurement should be
        """
        prob = 1.0
        for i in range(len(Robot.landmarks)):
            dist = sqrt((self.x - Robot.landmarks[i][0]) ** 2 + (self.y - Robot.landmarks[i][1]) ** 2)
            prob *= Robot.gaussian(dist, self.sense_noise, measurement[i])
        return prob

    def __repr__(self):
        return '[x=%.6s y=%.6s orient=%.6s]' % (str(self.x), str(self.y), str(self.orientation))

    def __str__(self):
        return '[x=%.6s y=%.6s orient=%.6s]' % (str(self.x), str(self.y), str(self.orientation))

def eval(r, p):
    """
    Calculates the sum of square error for the robot and particles
    """
    sum = 0.0

    for r_particle in p: # calculate mean error
        d_x = (r_particle.x - r.x + (Robot.world_size/2.0)) % Robot.world_size - (Robot.world_size/2.0)
        d_y = (r_particle.y - r.y + (Robot.world_size/2.0)) % Robot.world_size - (Robot.world_size/2.0)
        err = sqrt(d_x * d_x + d_y * d_y)
        sum += err

    return sum / float(len(p))

if __name__ == "__main__":
    from pprint import pprint as pp
    ROBOT = Robot()
    ROBOT = ROBOT.move(0.1, 5.0)
    SAMPLING = ResamplingWheel()
    Z = ROBOT.sense()
    N = 1000
    T = 10 #Leave this as 10 for grading purposes.

    p = []
    for i in range(N):
        r = Robot()
        r.set_noise(0.05, 0.05, 5.0)
        p.append(r)

    for t in range(T):
        ROBOT = ROBOT.move(0.1, 5.0)
        Z = ROBOT.sense()

        p2 = []
        for i in range(N):
            p2.append(p[i].move(0.1, 5.0))
        p = p2

        w = []
        for i in range(N):
            w.append(p[i].measurement_prob(Z))

        SAMPLING.set_wheel_data(w)

        p3 = []
        for i in range(N):
            p3.append(p[SAMPLING.get_pick_index()])
        p = p3
        #enter code here, make sure that you output 10 print statements.
        print("Time:", t)
        # pp(p)
        print("SSE:", eval(ROBOT, p))
