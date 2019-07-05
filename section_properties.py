import math
import numpy as np
import abc


class Section(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self):
        self.area = None
        self.centroid = (None, None)
        self.i_x = None
        self.i_y = None
        self.r_x = None
        self.r_y = None
        self.ze_x = None
        self.ze_y = None
        self.zp_x = None
        self.zp_y = None

    @abc.abstractmethod
    def __repr__(self):
        pass

    @abc.abstractmethod
    def centroid(self):
        pass

    @abc.abstractmethod
    def area(self):
        pass

    @abc.abstractmethod
    def i_x(self):
        pass

    @abc.abstractmethod
    def i_y(self):
        pass

    @abc.abstractmethod
    def r_x(self):
        pass

    @abc.abstractmethod
    def r_y(self):
        pass

    @abc.abstractmethod
    def ze_x(self):
        pass

    @abc.abstractmethod
    def ze_y(self):
        pass

    @abc.abstractmethod
    def zp_x(self):
        pass

    @abc.abstractmethod
    def zp_y(self):
        pass


class Rectangle(Section):

    def __init__(self, length, breadth):
        super(Rectangle, self).__init__()
        self.length = length
        self.breadth = breadth

    def __repr__(self):
        repr = "Rectangle\n"
        repr += "Length: {}\n".format(self.length)
        repr += "Breadth: {}\n".format(self.breadth)
        return repr

    def centroid(self):
        super(Rectangle, self).centroid = (self.length/2, self.breadth/2)
        return self.centroid

    def area(self):
        super(Rectangle, self).area = self.length * self.breadth
        return self.area

    def i_x(self):
        super(Rectangle, self).i_x = self.length * self.breadth**3 /12
        return self.i_x

    def i_y(self):
        super(Rectangle, self).i_y = self.breadth * self.length**3 /12
        return self.i_y

    def r_x(self):
        super(Rectangle, self).r_x = math.sqrt(self.i_x/self.area)
        return self.r_x

    def r_y(self):
        super(Rectangle, self).r_y = math.sqrt(self.i_y/self.area)
        return self.r_y

    def ze_x(self):
        super(Rectangle, self).ze_x = 2 * super(Rectangle, self).i_x / self.breadth
        return self.r_x

    def ze_y(self):
        super(Rectangle, self).ze_y = 2 * super(Rectangle, self).i_y / self.length
        return self.r_y

    def zp_x(self):
        #TODO
        pass

    def zp_y(self):
        #TODO
        pass