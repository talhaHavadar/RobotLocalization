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
from collections import Counter

class ResamplingWheel(object):
    """
    A Class implementation for resampling wheel
    Creates an imaginary wheel that consist of weighted portions.
    According to these weights, you can pick an index value.
    Index with more weights has more chance to be picked up.
    """

    def __init__(self, initiate_with=None):
        self.wheel = []
        self.max_weight = None
        self.is_resampled = False
        self.beta = 0.0
        self.last_index = 0

        if initiate_with is not None and isinstance(initiate_with, list):
            self.wheel = initiate_with

        self.length = len(self.wheel)

        if self.length > 0:
            self.max_weight = max(self.wheel)
            self.last_index = int(random.random() * self.length)

    def get_pick_index(self):
        """
        Returns an index value according to given data.
        Given data's length and weights matter
        """

        if not self.is_resampled:
            self.__resample__()

        while self.beta > self.wheel[self.last_index]:
            self.beta -= self.wheel[self.last_index]
            self.last_index = (self.last_index + 1) % self.length

        self.is_resampled = False

        return self.last_index

    def __resample__(self):

        self.beta += random.random() * 2.0 * self.max_weight
        self.is_resampled = True

    def __len__(self):
        return len(self.wheel)


if __name__ == "__main__":

    DATA = [10, 11, 12, 13, 14]
    SAMPLING = ResamplingWheel([5, 2, 1, 1, 1])
    SAMPLED = []

    print("Length of the sampling wheel:", len(SAMPLING))

    for i in range(100):
        index = SAMPLING.get_pick_index()
        print(DATA[index])
        SAMPLED.append(DATA[index])

    print(Counter(SAMPLED))
