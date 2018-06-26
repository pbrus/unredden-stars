import numpy as np
from scipy.optimize import fsolve


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
    data_type = {'names': ('x','y'), 'formats': ('f8','f8')}
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
    data_type = {'names': ('id','x','y','xerr','yerr'),
                 'formats': ('i8','f8','f8','f8','f8')}
    stars = _read_file(filename, data_type)

    return stars

def unreddened_sequence_nodes(point, unreddened_sequence, reddening_line_slope):
    """
    Determine an index(es) of the n-th point(s) of the unreddened sequence
    for the given point P(x, y). n-th and n+1-th points set a segment
    which intersects with the reddening line passing through P.

    Parameters
    ----------
    point : tuple
        A tuple containing xy coordinates (float) on the color-color plane.
    unreddened_sequence : ndarray
        A model of the unreddened sequence on the color-color plane.
    reddening_line_slope : float
        A value of a slope of the reddening line.
        For example E(U-B)/E(B-V) = 0.72.

    Returns
    -------
    nodes_list : list
        A list of an index(es).
    """
    nodes_list = []

    for node, sequence_piece in (
        enumerate(zip(unreddened_sequence, unreddened_sequence[1:]))):

        if point[0] <= sequence_piece[0][0]:
            continue
        else:
            first_differential_slope = (
                slope_line(point, sequence_piece[0]) - reddening_line_slope)
            second_differential_slope = (
                slope_line(point, sequence_piece[1]) - reddening_line_slope)

            if first_differential_slope*second_differential_slope < 0:
                nodes_list += [node]

    return nodes_list

def slope_line(first_point, second_point):
    """
    Calculate a value of a line slope for the given two points.

    Parameters
    ----------
    first_point, second_point : tuple
        A tuple containing xy coordinates (float) on the color-color plane.

    Returns
    -------
    slope : float
        A value of the slope line.
    """
    slope = (second_point[1] - first_point[1])
    slope /= (second_point[0] - first_point[0])

    return slope

def y_intercept_line(slope, point):
    return point[1] - slope*point[0]

def interpolation_line_coefficients(unreddened_sequence, sequence_nodes):
    coefficients = ()

    for node in sequence_nodes:
        A = slope_line(unreddened_sequence[node+1], unreddened_sequence[node])
        B = y_intercept_line(A, unreddened_sequence[node])
        coefficients += (A,B),

    return coefficients

def line(coefficients, x):
    return coefficients[0]*x + coefficients[1]

def find_intersection(first_line, second_line):
    return fsolve(lambda x: line(first_line, x) - line(second_line, x), 0.0)
