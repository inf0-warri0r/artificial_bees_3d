"""
Author : tharindra galahena (inf0_warri0r)
Project: artificial bees simulation using neural networks - part 2
Blog   : http://www.inf0warri0r.blogspot.com
Date   : 18/01/2013
License:

     Copyright 2013 Tharindra Galahena

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version. This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
details.

* You should have received a copy of the GNU General Public License along with
This program. If not, see http://www.gnu.org/licenses/.

"""
import simulation


def header():
    print "--------------------------------------------------"
    print "       -- ARTIFICIAL BEES SIMIULATION --          "
    print "                                                  "
    print "   Author : tharindra galahena (inf0_warri0r)     "
    print "   Blog   : http://www.inf0warri0r.blogspot.com   "
    print "--------------------------------------------------"
    print ""


if __name__ == '__main__':

    header()
    w = simulation.world(40, 80, 600, 600, 600)
    w.set_bees((3, 9, 2, 10), (1, 1, 2, 0), 90, 2)
    w.simulate()
