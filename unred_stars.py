#!/usr/bin/env python3

from argparse import ArgumentParser
from argparse import RawTextHelpFormatter as tefo
from unred.unred import *


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

res = extinction(points, model, unred_line, r_param)
res = sort_extinction(res, "max")
print_extinction(res)


