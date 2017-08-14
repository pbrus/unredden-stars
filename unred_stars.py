#!/usr/bin/env python
#-*- coding: utf-8 -*-

from argparse import ArgumentParser
from argparse import RawTextHelpFormatter as tefo

argparser = ArgumentParser(
    prog='unred_stars.py',
    description='>> Script unreddens stars on the color-color plane <<',
    epilog='Copyright (c) 2017 Przemysław Bruś', formatter_class=tefo
)
argparser.add_argument('list_with_stars', help='must contain columns with data:\n\
id(int) x_color(float) y_color(float) err_xcolor(float) err_ycolor(float)\n\n')
argparser.add_argument('unred_sequence', help='must contain columns with data:\n\
x_color(float) y_color(float)\n\n')
argparser.add_argument('red_slope', help='value of the reddening line slope\n\
defined as E(y_color)/E(x_color)\n\
for example: E(U-B)/E(B-V) = 0.72\n\n', type=float)
argparser.add_argument('R_param', help='defined as A/E(x_color)\n\
for example: Av/E(B-V) = 3.1', type=float)
argparser.add_argument('--min', help='for each star print only the minimum value of extinction',
action='store_true')
argparser.add_argument('-v', '--version', action='version', version='%(prog)s\n * Version: 2017-08-14\n \
* Licensed under the MIT license:\n   http://opensource.org/licenses/MIT\n * Copyright (c) 2017 Przemysław Bruś')
args = argparser.parse_args()

import numpy as np
from scipy.optimize import fsolve


def get_model(filename):
    with open(filename) as fd_model:
        try:
            model = np.loadtxt(fd_model, dtype={'names': ('x','y'), 'formats': ('f4','f4')})
        except ValueError as err:
            print("Unred model: %s" % err)
            exit(1)

    return model

def get_points(filename):
    with open(filename) as fd_points:
        try:
            points = np.loadtxt(fd_points, dtype={'names': ('id','x','y','xerr','yerr'), 'formats': ('i8','f4','f4','f4','f4')})
        except ValueError as err:
            print("File with stars: %s" % err)
            exit(1)

    return points

def model_slope_positions(point, model, line_slope):
    idxs = []
    for i,m in enumerate(zip(model, model[1:])):
        if point[0] < m[0][0]:
            continue
        else:
            diff_slope1 = slope_line(point, m[0]) - line_slope
            diff_slope2 = slope_line(point, m[1]) - line_slope

            if diff_slope1 * diff_slope2 < 0:
                idxs += [i]

    return idxs

def slope_line(coo1, coo2):
    return (coo2[1] - coo1[1])/(coo2[0] - coo1[0])

def y_intercept_line(slope, point):
    return point[1] - slope*point[0]

def interpolation_line_coeff(model, idxs):
    coeff = ()
    for i in idxs:
        A = slope_line(model[i+1], model[i])
        B = y_intercept_line(A, model[i])
        coeff += (A,B),

    return coeff

def line(coeff,x):
    return coeff[0]*x + coeff[1]

def find_intersection(line1_coeff, line2_coeff):
    return fsolve(lambda x: line(line1_coeff,x) - line(line2_coeff,x),0.0)


if __name__ == "__main__":
    stars = args.list_with_stars
    unred_seq = args.unred_sequence
    unred_line = args.red_slope
    r_param = args.R_param

    points = get_points(stars)
    model = get_model(unred_seq)

    print("# ID x_ci y_ci x_ci0 y_ci0 E(x_ci) E(y_ci) Av")

    for p in points:
        pid = p[0]

        for px in (p[1],p[1]-p[3],p[1]+p[3]):
            for py in (p[2],p[2]-p[4],p[2]+p[4]):
                idxs = model_slope_positions((px, py), model, unred_line)
                interpol_line_coeff = interpolation_line_coeff(model, idxs)
                parrallel_unred_coeff = unred_line, y_intercept_line(unred_line, (px,py))

                for i,idx in enumerate(idxs):
                    intersect_x0 = find_intersection(interpol_line_coeff[i], parrallel_unred_coeff)
                    intersect_y0 = line(parrallel_unred_coeff, intersect_x0)
                    Ex = px - float(intersect_x0)
                    Ey = py - float(intersect_y0)
                    Av = r_param*Ex
                    print("%4i %7.4f %7.4f %7.4f %7.4f %8.4f %7.4f %8.4f" % (pid, px, py, intersect_x0, intersect_y0, Ex, Ey, Av))
