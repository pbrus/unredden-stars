#!/usr/bin/env python3

import numpy as np
from scipy.optimize import fsolve
from argparse import ArgumentParser
from argparse import RawTextHelpFormatter as tefo


def _read_file(filename, data_type):
    try:
        with open(filename, 'r') as file_descriptor:
            file_content = np.loadtxt(file_descriptor, data_type, ndmin=1)
    except FileNotFoundError:
        print("File {} doesn't exist!".format(filename))
        exit(1)

    return file_content

def read_unreddened_sequence(filename):
    """
    Read an unreddened sequence of stars from a text file.

    Parameters
    ----------
    filename : str
        The name (with a path if neccessary) of the file which
        contains two columns with floats. The first one represents
        X color, the second column - Y color. The data must
        be sorted by increasing temperature.

    Returns
    -------
    model : ndarray
        Data read from the text file.
    """
    data_type={'names': ('x','y'), 'formats': ('f8','f8')}
    model = _read_file(filename, data_type)

    return model

def read_reddened_stars(filename):
    """
    Read reddened stars from a text file.

    Parameters
    ----------
    filename : str
        The name (with a path if neccessary) of the file which
        has 5 five columns. The first one with integers, the rest
        with floats. Each column represents: star_id, x_color, y_color,
        x_color_error, y_color_error.

    Returns
    -------
    stars : ndarray
        Data read from the text file.
    """
    data_type={'names': ('id','x','y','xerr','yerr'),
               'formats': ('i8','f8','f8','f8','f8')}
    stars = _read_file(filename, data_type)

    return stars

def model_slope_positions(point, model, line_slope):
    idxs = []
    for i,m in enumerate(zip(model, model[1:])):
        if point[0] <= m[0][0]:
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
    argparser = ArgumentParser(
    prog='unred_stars.py',
    description='>> Script unreddens stars on the color-color plane <<',
    epilog='Copyright (c) 2017 Przemysław Bruś', formatter_class=tefo
    )
    argparser.add_argument('list_with_stars', help='must contain columns with data:\n\
    id(int) x_color(float) y_color(float) err_xcolor(float) err_ycolor(float)\n\n')
    argparser.add_argument('unred_sequence', help='must contain columns with data:\n\
    x_color(float) y_color(float)\nThe data must be sorted by INCREASING TEMPERATURE\n\n')
    argparser.add_argument('red_slope', help='value of the reddening line slope\n\
    defined as E(y_color)/E(x_color)\n\
    for example: E(U-B)/E(B-V) = 0.72\n\n', type=float)
    argparser.add_argument('R_param', help='defined as A/E(x_color)\n\
    for example: Av/E(B-V) = 3.1', type=float)
    argparser.add_argument('--min', help='for each star print only the minimum value of extinction',
    action='store_true')
    argparser.add_argument('--max', help='for each star print only the maximum value of extinction',
    action='store_true')
    argparser.add_argument('-v', '--version', action='version', version='%(prog)s\n * Version: 2017-08-25\n \
    * Licensed under the MIT license:\n   http://opensource.org/licenses/MIT\n * Copyright (c) 2017 Przemysław Bruś')
    args = argparser.parse_args()

    stars = args.list_with_stars
    unred_seq = args.unred_sequence
    unred_line = args.red_slope
    r_param = args.R_param

    points = read_reddened_stars(stars)
    model = read_unreddened_sequence(unred_seq)

    if args.min and args.max:
        print("unred_stars: choose only one option: --min or --max")
        exit()

    dtype = [('pid', int), ('px', float), ('py', float), ('x0', float), ('y0', float), ('Ex', float), ('Ey', float), ('A', float)]
    print("# ID x_ci y_ci x_ci0 y_ci0 E(x_ci) E(y_ci) A")

    for p in points:
        pid = p[0]
        output_values = []

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
                    A = r_param*Ex
                    output = (pid, px, py, intersect_x0, intersect_y0, Ex, Ey, A)
                    if args.min or args.max:
                        output_values += [output]
                    else:
                        print("%4i %7.4f %7.4f %7.4f %7.4f %8.4f %7.4f %8.4f" % (output))

        if len(output_values) > 0:
            output_array = np.array(output_values, dtype=dtype)
            if args.min:
                out = tuple(np.sort(output_array, order='A')[0])
            elif args.max:
                out = tuple(np.sort(output_array, order='A')[-1])
            print("%4i %7.4f %7.4f %7.4f %7.4f %8.4f %7.4f %8.4f" % out)
