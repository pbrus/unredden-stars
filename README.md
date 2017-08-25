# Unredden-stars [![GitHub release](http://www.astro.uni.wroc.pl/ludzie/brus/img/github/ver20170825.svg "download")](https://github.com/pbrus/unredden-stars/blob/master/unred_stars.py) ![Written in Python](http://www.astro.uni.wroc.pl/ludzie/brus/img/github/python.svg "language")

Aids to unredden stars on the color-color plane.

![unredden-stars](http://www.astro.uni.wroc.pl/ludzie/brus/img/github/unred-stars.gif)

## Installation

Download `unred_stars.py` wherever you want and make the script executable. I recommend to download it to any catalog pointed by the `$PATH` variable. Moreover you should have installed *Python 2.7* with the following modules:

 * *numpy*
 * *scipy*
 * *argparse*

To use the program properly you need to prepare a file with data. At the beginning call the script from the terminal window with the `-h` option:
```bash
$ unred_stars.py -h
```
This will give you a description of all options. If you need to see the program in action immediately, you can use files from the `example/` directory. Please download them from the repo to your working directory. A basic call:
```bash
$ unred_stars.py stars.dat ub_bv_dwarfs.dat 0.72 3.1
```
You can filter the data using `--min` or `--max` option:
```bash
$ unred_stars.py stars.dat ub_bv_dwarfs.dat 0.72 3.1 --min
```

I encourage to visit my website to see more detailed description of this program. The current link can be found on my [GitHub profile](https://github.com/pbrus).

## License

**Unredden-stars** is licensed under the [MIT license](http://opensource.org/licenses/MIT).
