import numpy as np


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
