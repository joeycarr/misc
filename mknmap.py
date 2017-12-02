#!/usr/bin/env python

# usage: mknmap.py [-h] [-d] left right top bottom output
#
# This is a convenience script for creating a normal map from photographs. The
# four input photographs should be lit along the cardinal axes. This works best
# on surfaces with a matte finish and a uniform, light color. The illumination
# should come from as low an angle as possible without causing self-shadowing.
# If you prefix your file names so they sort in left, right, top, bottom order,
# it is easier to invoke the utility with a glob, for example: `mknmap.py
# inputs*.png output.png`.
#
# positional arguments:
#   left           A readable file. Works best if this is in a linear (gamma =
#                  1.0) colorspace. The first image should be lit from the left.
#   right          The same scene lit from the right.
#   top            The same scene lit from the top.
#   bottom         The same scene lit from the bottom.
#   output         A writeable file to place the normal map into. PNG files will
#                  be truncated to 8 bits whereas TIFF files may go up to 64
#                  bits. You can use any format suported by scikit-image; the
#                  type is deduced from the suffix.
#
# optional arguments:
#   -h, --help     show this help message and exit
#   -d, --detrend  If this option is present, the utility will attempt to remove
#                  any linear bias along the horizontal and vertical. This sort
#                  of bias can result from the falloff of the light source. This
#                  option works best when the frame is filled with a relatively
#                  uniform texture. It does not work if there is an irregularly
#                  shaped object in the frame.

import argparse
import numpy as np

from scipy.stats import linregress

from skimage import img_as_float, img_as_ubyte, img_as_uint
from skimage.color import rgb2gray
from skimage.exposure import rescale_intensity
from skimage.io import imread, imsave, imshow

def import_img(name):
    img = rgb2gray(img_as_float(imread(name)))
    return img

def import_imgset(names):
    return list(map(import_img, names))

def meandetrend(img, axis=0):
    y = img.mean(axis=axis)
    x = np.arange(len(y))

    lm = linregress(x, y)
    trendline = lm.slope*x + lm.intercept

    # broadcasting only works along the last axis
    if axis == 1:
        result = np.transpose(img.T - trendline)
    else:
        result = img - trendline
    return result

def makemap(left, right, top, bottom, detrend=False):
    red = right - left
    green = top - bottom

    if detrend:
        red = meandetrend(red, axis=1)
        green = meandetrend(green, axis=0)

    # scale the red and green channels uniformly so that neither exceeds the
    # reciprocal of hte square root of 2, thus the sum of their squares will not
    # exceed 1.
    absmax = np.max(
        np.max(np.abs(red)),
        np.max(np.abs(green))
        )

    factor =  absmax * np.sqrt(2)
    red = red / factor
    green = green / factor

    # red^2 + green^2 + blue^2 = 1
    # so blue = sqrt(1 - red^2 - green^2)
    blue = np.sqrt(1.0 - (red**2 + green**2))

    result = np.stack([red, green, blue], axis=-1)
    result = rescale_intensity(result, in_range=(-1,1), out_range=(0,1))

    return result

def parse_args():
    ap = argparse.ArgumentParser(
        description='''This is a convenience script for creating a normal map
        from photographs. The four input photographs should be lit along the
        cardinal axes. This works best on surfaces with a matte finish and a
        uniform, light color. The illumination should come from as low an angle
        as possible without causing self-shadowing.

        If you prefix your file names so they sort in left, right, top, bottom
        order, it is easier to invoke the utility with a glob, for example:
        `mknmap.py inputs*.png output.png`.
        '''
    )

    ap.add_argument('-d', '--detrend',
        action='store_true',
        help='''If this option is present, the utility will attempt to remove
        any linear bias along the horizontal and vertical. This sort of bias can
        result from the falloff of the light source. This option works best when
        the frame is filled with a relatively uniform texture. It does not work
        if there is an irregularly shaped object in the frame.'''
    )

    ap.add_argument('left',
        type=argparse.FileType('r'),
        help='''A readable file. Works best if this is in a linear (gamma = 1.0)
        colorspace. The first image should be lit from the left.'''
    )

    ap.add_argument('right',
        type=argparse.FileType('r'),
        help='The same scene lit from the right.'
    )

    ap.add_argument('top',
        type=argparse.FileType('r'),
        help='The same scene lit from the top.'
    )

    ap.add_argument('bottom',
        type=argparse.FileType('r'),
        help='The same scene lit from the bottom.'
    )

    ap.add_argument('output',
        type=argparse.FileType('w'),
        help='''A writeable file to place the normal map into. PNG files will
        be truncated to 8 bits whereas TIFF files may go up to 64 bits. You can
        use any format suported by scikit-image; the type is deduced from the
        suffix.'''
    )

    return ap.parse_args()

def main():
    args = parse_args()

    imageset = import_imgset([
        args.left.name,
        args.right.name,
        args.top.name,
        args.bottom.name ])

    result = makemap(*imageset, detrend=args.detrend)

    imsave(args.output.name, result)

if __name__ == '__main__':
    main()
