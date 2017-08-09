#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
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
    return (coo2[1] - coo1[1]) / (coo2[0] - coo1[0])

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
    if len(sys.argv) != 4:
        script_name = sys.argv[0].replace("./","")
        print("Usage: python %s <unred model> <reddening line> <file with stars>" % script_name)
        print(" => unred model")
        print("  Model with unreddened sequence with the structure:")
        print("  xcolor ycolor")
        print("  Note that data must be sorted by INCREASED TEMPERATURE")
        print(" => reddening line")
        print("  E(ycolor)/E(xcolor) = A")
        print(" => file with stars")
        print("  id xcolor ycolor err_xcolor err_ycolor")
        print("  Note that id must be integer")
        print("")
        print("Example: python %s white_dwarf.mdl 1.44 white_dwarfs.cand" % script_name)
        print("Przemysław Bruś, 2017-07-21")
    else:
        model = get_model(sys.argv[1])
        unred_line = float(sys.argv[2])
        points = get_points(sys.argv[3])

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
                        Av = 2.2 * Ex
                        print("%4i %7.4f %7.4f %7.4f %7.4f %8.4f %7.4f %8.4f" % (pid, px, py, intersect_x0, intersect_y0, Ex, Ey, Av))
