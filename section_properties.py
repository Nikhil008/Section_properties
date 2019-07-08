import math
import numpy as np
import abc


class Section(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self):
        self.Area = None
        self.Centroid = (None, None)
        self.I_x = None
        self.I_y = None
        self.R_x = None
        self.R_y = None
        self.Ze_x = None
        self.Ze_y = None
        self.Zp_x = None
        self.Zp_y = None

    @abc.abstractmethod
    def __repr__(self):
        repr = "Area: {}\n".format(self.area())
        repr += "Centroid: {}\n".format(self.centroid())
        repr += "I_x: {}\n".format(self.i_x())
        repr += "I_y: {}\n".format(self.i_y())
        repr += "R_x: {}\n".format(self.r_x())
        repr += "R_y: {}\n".format(self.r_y())
        repr += "Ze_x: {}\n".format(self.ze_x())
        repr += "Ze_y: {}\n".format(self.ze_y())
        repr += "Zp_x: {}\n".format(self.zp_x())
        repr += "Zp_y: {}\n".format(self.zp_y())
        return repr

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
        self.Length = length
        self.Breadth = breadth

    def __repr__(self):
        repr = "Rectangle\n"
        repr += "Length: {}\n".format(self.Length)
        repr += "Breadth: {}\n".format(self.Breadth)
        repr += super(Rectangle, self).__repr__()
        return repr

    def centroid(self):
        self.Centroid = (self.Length/2, self.Breadth/2)
        return self.Centroid

    def area(self):
        self.Area = self.Length * self.Breadth
        return self.Area

    def i_x(self):
        self.I_x = self.Length * self.Breadth**3 / 12
        return self.I_x

    def i_y(self):
        self.I_y = self.Breadth * self.Length**3 /12
        return self.I_y

    def r_x(self):
        self.R_x = math.sqrt(self.i_x()/self.area())
        return self.R_x

    def r_y(self):
        self.R_y = math.sqrt(self.i_y()/self.area())
        return self.R_y

    def ze_x(self):
        self.Ze_x = 2 * self.i_x() / self.Breadth
        return self.Ze_x

    def ze_y(self):
        self.Ze_y = 2 * self.i_y() / self.Length
        return self.Ze_y

    def zp_x(self):
        self.Zp_x = self.Length * self.Breadth ** 2 / 4
        return self.Zp_x

    def zp_y(self):
        self.Zp_y = self.Breadth * self.Length ** 2 / 4
        return self.Zp_y


class RH_triangle(Section):

    def __init__(self, base, height, angle):
        super(RH_triangle, self).__init__()
        self.Base = base
        self.Height = height
        self.Angle = angle

    def __repr__(self):
        repr = "RH_triangle\n"
        repr += "Base: {}\n".format(self.Base)
        repr += "Height: {}\n".format(self.Height)
        repr += "Angle: {}\n".format(self.Angle)
        repr += super(RH_triangle, self).__repr__()
        return repr

    def centroid(self):
        self.Centroid = ((self.Base + (self.Height / math.tan(self.Angle)))/3, self.Height/3)
        return self.Centroid

    def area(self):
        self.Area = self.Base * self.Height / 2
        return self.Area

    def i_x(self):
        self.I_x = self.Base * self.Height**3 / 36
        return self.I_x

    def i_y(self):
        b = self.Base
        h = self.Height
        a = self.Height / math.tan(self.Angle)
        self.I_y = (b**3 * h - b**2 * h * a + b * h * a**2)/36
        return self.I_y

    def r_x(self):
        self.R_x = math.sqrt(self.i_x()/self.area())
        return self.R_x

    def r_y(self):
        self.R_y = math.sqrt(self.i_y()/self.area())
        return self.R_y

    def ze_x(self):
        self.Ze_x = 2 * self.i_x() / self.Breadth
        return self.Ze_x

    def ze_y(self):
        self.Ze_y = 2 * self.i_y() / self.Length
        return self.Ze_y

    def zp_x(self):
        self.Zp_x = self.Length * self.Breadth ** 2 / 4
        return self.Zp_x

    def zp_y(self):
        self.Zp_y = self.Breadth * self.Length ** 2 / 4
        return self.Zp_y



