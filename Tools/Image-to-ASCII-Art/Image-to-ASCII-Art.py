#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, random, argparse
import numpy as np
import math

from PIL import Image, ImageChops


gscale1 = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

gscale2 = '@%#*+=-:. '

def getAvarageL(image):
    im = np.array(image)

    w,h = im.shape

    return np.average(im.reshape(w*h))


def covertImageToAscii(fileName, cols, scale, moreLevels, invert):
    global gscale1, gscale2

    image = Image.open(fileName).convert('L')

    if invert:
        print("Inverting image")
        image = ImageChops.invert(image)
    
    W, H = image.size[0], image.size[1]
    print("Input image dimensions: %d x %d" % (W, H))

    w = W/cols

    h = w/scale

    rows = int(H/h)

    print("Cols: %d, Rows: %d" % (cols, rows))
    print("Tile dimensions: %d x %d" % (w, h))

    if cols > W or rows > H:
        print("Image too small for specified cols!")
        exit(0)

    aimg = []

    for j in range(rows):
        y1 = int(j*h)
        y2 = int((j+1)*h)

        if j == rows-1:
            y2 = H

        aimg.append("")

        for i in range(cols):

            x1 = int(i*w)
            x2 = int((i+1)*w)

            if i == cols-1:
                x2 = W
            
            img = image.crop((x1, y1, x2, y2))

            avg = int(getAvarageL(img))

            if moreLevels:
                gsval = gscale1[int((avg*69)/255)]
            else:
                gsval = gscale2[int((avg*9)/255)]

            aimg[j] += gsval

    return aimg


def main():

    descStr = "This sript converts an image into ASCII art."
    parser = argparse.ArgumentParser(description=descStr)

    parser.add_argument('--file', dest='imgFile', required=True)
    parser.add_argument('--scale', dest='scale', required=False)
    parser.add_argument('--out', dest='outFile', required=False)      
    parser.add_argument('--cols', dest='cols', required=False)
    parser.add_argument('--invert', dest='invert', required=False)
    parser.add_argument('--moreLevels', dest='moreLevels', action='store_true')

    args = parser.parse_args()

    imgFile = args.imgFile

    outFile = 'out.txt'
    if args.outFile:
        outFile = args.outFile
    
    scale = 0.43
    if args.scale:
        scale = float(args.scale)
    
    cols = 80
    if args.cols:
        cols = int(args.cols)

    print('Generating ASCII art...')

    aimg = covertImageToAscii(imgFile, cols, scale, args.moreLevels, args.invert)

    f = open(outFile, 'w')

    for row in aimg:
        f.write(row + '\n')
        print(row)

    f.close()
    print("ASCII art written to %s" % outFile)


if __name__ == "__main__":
    main()
