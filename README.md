# Unredden-stars
[![Build Status](https://travis-ci.org/pbrus/unredden-stars.svg?branch=master)](https://travis-ci.org/pbrus/unredden-stars) [![Code](https://img.shields.io/badge/code-Python-blue.svg "Python")](https://www.python.org/) [![PyPI version](https://badge.fury.io/py/unred.svg)](https://badge.fury.io/py/unred) [![License](https://img.shields.io/badge/license-MIT-yellow.svg "MIT license")](https://github.com/pbrus/unredden-stars/blob/master/LICENSE)

This package allows to determine the interstellar extinction for stars lying on the color-color plane. Using:
1. theoretical stars sequence
2. reddening line slope
3. positions of stars

package functions calculate which part of the sequence the reddened stars come from. This allows to determine the color excess and hence the extinction of each star.

![unredden-stars](http://www.astro.uni.wroc.pl/ludzie/brus/img/github/unred-stars.gif)

## Installation

To install the package please type from the command line:
```bash
$ sudo pip3 install unred
```
or alternatively:
```bash
$ git clone https://github.com/pbrus/unredden-stars
$ cd unredden-stars
$ sudo python3 setup.py install
```

## Usage

At the beginning call the script from the terminal window with the `-h` option:
```bash
$ unred_stars.py -h
```
This will give you a description of available options. If you need to see the program in action immediately, you can use files from the `example_data/` directory:
```bash
$ unred_stars.py example_data/stars.dat example_data/ub_bv_dwarfs.dat 0.72 3.1
```
Moreover, you can filter the output (by extinction value for each star) using `--min` or `--max` option:
```bash
$ unred_stars.py example_data/stars.dat example_data/ub_bv_dwarfs.dat 0.72 3.1 --min
```

I encourage to visit my website to see more detailed description of this program. The current link can be found on my [GitHub profile](https://github.com/pbrus).

## License

**Unredden-stars** is licensed under the [MIT license](http://opensource.org/licenses/MIT).
