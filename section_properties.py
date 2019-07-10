import math
import numpy as np
import abc


def parallel_axis_transform_i(i,area, d):
    return i + area * d**2


def rotational_transform_i(i_x, i_y, i_xy, phi):
    i_u = (i_x + i_y)/2 + (i_x - i_y)/2 * math.cos(2*phi) - i_xy * math.sin(2*phi)
    i_v = (i_x + i_y) / 2 - (i_x - i_y) / 2 * math.cos(2 * phi) + i_xy * math.sin(2 * phi)
    return i_u, i_v


def calc_centroid(areas, coordinates):
    areas = np.array([areas])
    coordinates = np.array([coordinates])
    return sum(areas * coordinates)

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


class Triangle(Section):

    def __init__(self, base, height, angle):
        super(Triangle, self).__init__()
        self.Base = base
        self.Height = height
        self.Angle = angle

    def __repr__(self):
        repr = "RH_triangle\n"
        repr += "Base: {}\n".format(self.Base)
        repr += "Height: {}\n".format(self.Height)
        repr += "Angle: {}\n".format(self.Angle)
        repr += super(Triangle, self).__repr__()
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
        self.Ze_x = self.i_x() / (2 * self.Height / 3)
        return self.Ze_x

    def ze_y(self):
        cx = self.centroid()[0]
        if math.tan(self.Angle) < 2*self.Height/self.Base:
            self.Ze_y = self.i_y() / cx
        else:
            self.Ze_y = self.i_y() / (self.Base - cx)
        return self.Ze_y

    def zp_x(self):
        #TODO
        return self.Zp_x

    def zp_y(self):
        #TODO
        return self.Zp_y


class Sector(Section):

    def __init__(self, radius, angle):
        super(Sector, self).__init__()
        self.Radius = radius
        self.Angle = angle

    def __repr__(self):
        repr = "Fillet\n"
        repr += "Radius: {}\n".format(self.Radius)
        repr += "Angle: {}\n".format(self.Angle)
        repr += super(Sector, self).__repr__()
        return repr

    def area(self):
        self.Area = self.Radius**2 * self.Angle / 2
        return self.Area

    def centroid(self):
        self.Centroid = (4/3 * self.Radius * math.sin(self.Angle/2)/self.Angle, 0)
        return self.Centroid

    def i_y(self):
        self.I_y = self.Radius**4 / 8 * (self.Angle + math.sin(self.Angle)) - self.area()*self.centroid()[0]**2
        return self.I_y

    def i_x(self):
        self.I_x = self.Radius**4 / 8 * (self.Angle - math.sin(self.Angle))
        return self.I_x

    def r_x(self):
        self.R_x = math.sqrt(self.i_x() / self.area())
        return self.R_x

    def r_y(self):
        self.R_y = math.sqrt(self.i_y() / self.area())
        return self.R_y

    def ze_x(self):
        return self.Ze_x

    def ze_y(self):
        return self.Ze_y

    def zp_x(self):
        return self.Zp_x

    def zp_y(self):
        return self.Zp_y

class Fillet(Section):

    def __init__(self, radius, angle):
        super(Fillet, self).__init__()  # How to use super here?
        self.Radius = radius
        self.Angle = angle
        self.Fillet_Sector = Sector(self.Radius, math.pi - self.Angle)
        self.Fillet_Triangle = Triangle(self.Radius/math.sin(self.Angle/2), self.Radius*math.cos(self.Angle/2), self.Angle/2)

    def __repr__(self):
        repr = "Fillet\n"
        repr += "Radius: {}\n".format(self.Radius)
        repr += "Angle: {}\n".format(self.Angle)
        repr += Section.__repr__()  # How to use super here?
        return repr

    def centroid(self):
        cx = 2 * self.Fillet_Triangle.area() * self.Fillet_Triangle.centroid()[0] - self.Fillet_Sector.area() * \
             (self.Fillet_Triangle.Base - self.Fillet_Sector.centroid()[0])
        self.Centroid = (cx, 0)
        return self.Centroid

    def area(self):
        self.Area = 2 * self.Fillet_Triangle.area() - self.Fillet_Sector.area()
        return self.Area

    def i_x(self):
        self.I_x = 2 * parallel_axis_transform_i(self.Fillet_Triangle.i_x(), self.Fillet_Triangle.area(), 
                                             self.Fillet_Triangle.centroid()[1]) \
                   - self.Fillet_Sector.i_x()
        return self.I_x

    def i_y(self):
        i_y_triangles_axis = 2 * parallel_axis_transform_i(self.Fillet_Triangle.i_y(), self.Fillet_Triangle.area(),
                                                      self.Fillet_Triangle.centroid()[0])
        i_y_sector_axis = parallel_axis_transform_i(self.Fillet_Sector.i_y(), self.Fillet_Sector.area(),
                                                    self.Fillet_Triangle.Base - self.Fillet_Sector.centroid()[0])
        i_y_axis = i_y_triangles_axis - i_y_sector_axis
        self.I_y = parallel_axis_transform_i(i_y_axis, -self.area(), self.centroid()[0])#note: negative area is imp
        return self.I_y

    def r_x(self):
        self.R_x = math.sqrt(self.i_x()/self.area())
        return self.R_x

    def r_y(self):
        self.R_y = math.sqrt(self.i_y()/self.area())
        return self.R_y

    def ze_x(self):
        return self.Ze_x

    def ze_y(self):
        return self.Ze_y

    def zp_x(self):
        return self.Zp_x

    def zp_y(self):
        return self.Zp_y


    """
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
    """


class ISMB_section(Section):

    def __init__(self, d, b, tf, tw, r1, r2, angle):
        super(ISMB_section, self).__init__()  # How to use super here?
        self.D = d
        self.B = b
        self.T = tf
        self.t = tw
        self.R1 = r1
        self.R2 = r2
        self.alpha = angle
        self.Fillet_1 = Fillet(self.R1, self.alpha)
        self.Fillet_2 = Fillet(self.R2, self.alpha)
        h = (self.B - self.t)/2/math.tan(math.pi - self.alpha)
        self.Rectangle_1 = Rectangle(self.t, self.D - 2*self.T - h)
        self.Rectangle_2 = Rectangle(self.B, self.T - h/2)
        self.Triangle_1 = Triangle((self.B - self.t)/2, self.T + h/2, math.pi/2)

    def __repr__(self):
        repr = "ISMB\n"
        repr += super(ISMB_section, self).__repr__()  # How to use super here?
        return repr

    def centroid(self):
        self.Centroid = (0, 0)
        return self.Centroid

    def area(self):
        self.Area = self.Rectangle_1.area() + 2 * self.Rectangle_2.area() + 4 * self.Triangle_1.area() + 4 * \
                    self.Fillet_1.area() - 4 * self.Fillet_2.area()
        return self.Area

    def i_x(self):
        h = (self.B - self.t) / 2 / math.tan(math.pi - self.alpha)
        L1 = self.D/2 - (self.T + h/2)
        L2 = self.D/2 - (self.T - h/2)
        I_rectangles = self.Rectangle_1.i_x() + 2 * parallel_axis_transform_i(self.Rectangle_2.i_x(),
                                                                          self.Rectangle_2.area(), self.D/2 -
                                                                          self.Rectangle_2.Breadth/2)
        I_triangles = 4 * parallel_axis_transform_i(self.Triangle_1.i_x(), self.Triangle_1.area(), self.D/2 -
                                                    self.Rectangle_1.Breadth - self.Triangle_1.centroid()[1])
        I_fillet1_x = parallel_axis_transform_i(self.Fillet_1.i_x(), self.Fillet_1.area(), L1 * math.sin(self.alpha/2)
                                                + self.t/2 * math.cos(self.alpha/2))
        I_fillet2_x = parallel_axis_transform_i(self.Fillet_2.i_x(), self.Fillet_2.area(), self.B/2
                                                * math.cos(self.alpha/2) + L2 * math.sin(self.alpha/2))
        I_fillet1_y = parallel_axis_transform_i(self.Fillet_1.i_y(), self.Fillet_1.area(),
                                                L1*math.cos(self.alpha/2) - self.t/2 * math.sin(self.alpha/2)
                                                - self.Fillet_1.centroid()[0])
        I_fillet2_y = parallel_axis_transform_i(self.Fillet_2.i_y(), self.Fillet_2.area(),
                                                self.B/2 * math.sin(self.alpha/2) - L2 * math.cos(self.alpha/2) -
                                                self.Fillet_2.centroid()[0])
        I_fillets_x = 4 * rotational_transform_i(I_fillet1_x, I_fillet1_y, 0, math.pi/2 - self.alpha/2)[0] - \
                      4 * rotational_transform_i(I_fillet2_x, I_fillet2_y, 0, math.pi/2 - self.alpha/2)[0]
        self.I_x = I_rectangles + I_triangles + I_fillets_x
        return self.I_x

    def i_y(self):
        h = (self.B - self.t) / 2 / math.tan(math.pi - self.alpha)
        L1 = self.D / 2 - (self.T + h / 2)
        L2 = self.D / 2 - (self.T - h / 2)
        I_rectangles = self.Rectangle_1.i_y() + 2 * self.Rectangle_2.i_y()
        I_triangles = 4 * parallel_axis_transform_i(self.Triangle_1.i_y(), self.Triangle_1.area(), self.t / 2 +
                                                    self.Triangle_1.centroid()[0])
        I_fillet1_x = parallel_axis_transform_i(self.Fillet_1.i_x(), self.Fillet_1.area(), L1 * math.sin(self.alpha / 2)
                                                + self.t / 2 * math.cos(self.alpha / 2))
        I_fillet2_x = parallel_axis_transform_i(self.Fillet_2.i_x(), self.Fillet_2.area(), self.B / 2
                                                * math.cos(self.alpha / 2) + L2 * math.sin(self.alpha / 2))
        I_fillet1_y = parallel_axis_transform_i(self.Fillet_1.i_y(), self.Fillet_1.area(),
                                                L1 * math.cos(self.alpha / 2) - self.t / 2 * math.sin(self.alpha / 2)
                                                - self.Fillet_1.centroid()[0])
        I_fillet2_y = parallel_axis_transform_i(self.Fillet_2.i_y(), self.Fillet_2.area(),
                                                self.B / 2 * math.sin(self.alpha / 2) - L2 * math.cos(self.alpha / 2) -
                                                self.Fillet_2.centroid()[0])
        I_fillets_y = 4 * rotational_transform_i(I_fillet1_x, I_fillet1_y, 0, math.pi / 2 - self.alpha / 2)[1] - \
                      4 * rotational_transform_i(I_fillet2_x, I_fillet2_y, 0, math.pi / 2 - self.alpha / 2)[1]
        self.I_y = I_rectangles + I_triangles + I_fillets_y
        return self.I_y

    def r_x(self):
        self.R_x = math.sqrt(self.i_x()/self.area())
        return self.R_x

    def r_y(self):
        self.R_y = math.sqrt(self.i_y()/self.area())
        return self.R_y

    def ze_x(self):
        return self.Ze_x

    def ze_y(self):
        return self.Ze_y

    def zp_x(self):
        return self.Zp_x

    def zp_y(self):
        return self.Zp_y
