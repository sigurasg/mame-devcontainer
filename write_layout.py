#!/usr/bin/env python3


XML_HEADER = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>"""
SVG_HEADER = """<svg width="{width}mm" height="{height}mm"
  xmlns="http://www.w3.org/2000/svg">"""
SVG_TRAILER = """</svg>"""

RECT_TEMPL = """<rect x="{x}mm" y="{y}mm" width="{width}mm" height="{height}mm" rx="{r}mm" ry="{r}mm" 
    style="fill:rgb(255,255,255);stroke-width:{stroke_width}mm;stroke:rgb(0,0,0)"/>"""


def rr(x, y, width, height, r, stroke_width):
    print(RECT_TEMPL.format(
                    x = x + stroke_width / 2,
                    y = y + stroke_width / 2,
                    width = width - stroke_width,
                    height = height - stroke_width,
                    r = 10,
                    stroke_width=stroke_width))

def main():
    # all dimensions in mm.
    main_bezel = (302, 150)

    print(XML_HEADER)
    print(SVG_HEADER.format(width=main_bezel[0], height=main_bezel[1]))

    stroke_width = 3

    # Main bezel.
    rr(x = 0, y = 0,
        width = main_bezel[0],
        height = main_bezel[1],
        r = 10,
        stroke_width = stroke_width)

    x = 6.25
    y = 0
    rr(x = x, y = y,
        width = 135.6,
        height = 145,
        r = 5,
        stroke_width = stroke_width)
    x += 7.5
    y += 12.3
    rr(x = x, y = y,
        width = 120,
        height = 105.6,
        r = 5,
        stroke_width = stroke_width)
    x += (120 - 105) / 2
    y += 10
    rr(x = x,
        y = y,
        width = 105,
        height = 83.2,
        r = 2,
        stroke_width = 1)

    print(SVG_TRAILER)

if __name__ == '__main__':
    main()