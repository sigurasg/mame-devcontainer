#!/usr/bin/env python3


XML_HEADER = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>"""
SVG_HEADER = """<svg width="{width}mm" height="{height}mm"
  xmlns="http://www.w3.org/2000/svg">"""
SVG_TRAILER = """</svg>"""

def rr(x, y, width, height, r, stroke_width):
    TEMPL = """<rect x="{x}mm" y="{y}mm" width="{width}mm" height="{height}mm" rx="{r}mm" ry="{r}mm"
        style="fill:rgb(255,255,255);stroke-width:{stroke_width}mm;stroke:rgb(0,0,0)"/>"""


    print(TEMPL.format(
                    x = x + stroke_width / 2,
                    y = y + stroke_width / 2,
                    width = width - stroke_width,
                    height = height - stroke_width,
                    r = r,
                    stroke_width=stroke_width))


def main_bezel(width, height, stroke_width):
    # Main bezel.
    rr(x = 0, y = 0,
        width = width,
        height = height,
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
        r = 0.1,
        stroke_width = 1)

def pot(x, y, name):
    CIRCLE_TEMPL = """<circle cx="{cx}mm" cy="{cy}mm" r="{r}mm"
        style="fill:rgb(255,255,255);stroke-width:{stroke_width}mm;stroke:rgb(0,0,0)"/>"""

    print(CIRCLE_TEMPL.format(cx=x, cy=y, r=9.5 / 2, stroke_width=1))
    print(CIRCLE_TEMPL.format(cx=x, cy=y, r=5.4 / 2, stroke_width=1))


def but(x, y, name):
    TEMPL = """<rect x="{x}mm" y="{y}mm" width="{side}mm" height="{side}mm"
        style="fill:rgb(255,255,255);stroke-width:{stroke_width}mm;stroke:rgb(0,0,0)"/>"""

    side = 4.5
    stroke = 0.4
    print(TEMPL.format(x = x - side / 2 - stroke / 2,
                    y = y - side / 2 - stroke / 2,
                    side = side,
                    stroke_width = stroke))


def pow(x, y, name):
    # TODO(siggi): Render the power button properly
    pot(x, y, name)


def volts_div(x, y):
    # TODO(siggi): Render the volts/div dials properly
    pot(x, y, "")


def sec_div(x, y):
    # TODO(siggi): Render the sec/div dial properly
    pot(x, y, "")

def up_dn_switch(x, y, name):
    # TODO(siggi): Render the up_dn switches properly
    but(x, y, name)

def bnc(x, y, name):
    # TODO(siggi): Render the BNCs properly
    pot(x, y, name)

def main():
    # all dimensions in mm.
    bezel_width = 302
    bezel_height = 150

    print(XML_HEADER)
    print(SVG_HEADER.format(width = bezel_width, height = bezel_height))

    main_bezel(width = bezel_width, height = bezel_height, stroke_width = 3)

    # Pots and buttons under the CRT.
    first_pot = 4.41 + 6.2 + 5
    pot_space = 30.3
    pot(x = first_pot + 0 * pot_space, y = 134, name = "INTENSITY")
    pot(x = first_pot + 1 * pot_space, y = 134, name = "FOCUS")
    pot(x = first_pot + 2 * pot_space, y = 134, name = "READOUT INTENSITY")
    pot(x = first_pot + 3 * pot_space, y = 134, name = "SCALE ILLUM")

    but(x = first_pot + 0.5 * pot_space, y = 134, name = "BEAM\nFIND")
    pow(x = 4.41 + 6.2 + 117, y = 134, name = "POWER")

    # Pots and buttons on the main front panel.
    bezel_edge = 142.25
    first_pot = bezel_edge + 21.5
    pot_space = 25.6

    # Top row pots and buttons
    # CH1 POS
    pot(x = first_pot + 0 * pot_space, y = 20, name = "POSITION")
    # CH2 POS
    pot(x = first_pot + 1 * pot_space, y = 20, name = "POSITION")
    # VERT POS
    vert_pos_x = first_pot + 2 * pot_space
    pot(x = vert_pos_x, y = 20, name = "POSITION")
    but(x = vert_pos_x + 16, y = 20, name = "X10 MAG")

    pot(x = first_pot + 88, y = 20, name = "HOLDOFF")
    pot(x = first_pot + 120, y = 20, name = "LEVEL")

    first_but = bezel_edge + 18.5
    but_space = 29.5 / 3
    row_y = 35.8
    # Channel selectors
    but(x = first_but + 0 * but_space, y = row_y, name ="CH 1")
    but(x = first_but + 1 * but_space, y = row_y, name ="CH 2")
    but(x = first_but + 2 * but_space, y = row_y, name ="CH 3")
    but(x = first_but + 3 * but_space, y = row_y, name ="CH 4")

    # Cursor controls.
    but(x = vert_pos_x + 0 * but_space, y = row_y, name = "DV")
    but(x = vert_pos_x + 1 * but_space, y = row_y, name = "Dt")
    but(x = vert_pos_x + 2 * but_space, y = row_y, name = "TRACKING")

    # Trigger controls
    but(x = bezel_edge + 107.3 + 4.3/2, y = row_y, name = "A/B TRIG")
    but(x = bezel_edge + 107.3 + 4.3/2 + 15.3, y = row_y, name = "SLOPE")

    row_y += 18.8
    but(x = first_but + 0 * but_space, y = row_y, name ="ADD")
    but(x = first_but + 1 * but_space, y = row_y, name ="INVERT")
    but(x = first_but + 2 * but_space, y = row_y, name ="CHOP")
    but(x = first_but + 3 * but_space, y = row_y, name ="20 MHZ\nBW LIMIT")

    row_y = 46
    pot(x = bezel_edge + 72, y = row_y, name = "D REF or DLY POS")
    pot(x = bezel_edge + 72 + 22.3, y = row_y, name = "D")

    btn_width = 18.1
    first_but = bezel_edge + 7.5 + btn_width / 2
    row_y = 87.1 - btn_width / 2
    volts_div(x = first_but, y = row_y)
    volts_div(x = first_but + 31.6, y = row_y)

    sec_div(x = first_but + 86.5 - btn_width / 2 - 21.5 / 2, y = row_y)

    first_switch = bezel_edge + 110
    row_y = 83.5
    switch_space = 22.5 / 3
    up_dn_switch(x = first_switch + 0 * switch_space, y = row_y, name = "MODE")
    up_dn_switch(x = first_switch + 1 * switch_space, y = row_y, name = "SOURCE")
    up_dn_switch(x = first_switch + 2 * switch_space, y = row_y, name = "COUPLING")

    row_y = 104
    up_dn_switch(x = bezel_edge + 23, y = row_y, name = "CH1 CPL")
    up_dn_switch(x = bezel_edge + 55, y = row_y, name = "CH2_CPL")
   
    pot(x = bezel_edge + 72, y = row_y, name = "TRACE\nSEP")
    # CH3 POS
    pot(x = bezel_edge + 96, y = row_y, name = "POSITION")

    but(x = bezel_edge + 111, y = row_y, name = "VOLTS/DIV")
    but(x = bezel_edge + 121, y = row_y, name = "VOLTS/DIV")

    # CH4 POS
    pot(x = bezel_edge + 139, y = row_y, name = "POSITION")

    row_y = 130
    bnc(x = bezel_edge + 16, y = row_y, name = "CH 1")
    bnc(x = bezel_edge + 58, y = row_y, name = "CH 2")
    bnc(x = bezel_edge + 95, y = row_y, name = "CH 3")
    bnc(x = bezel_edge + 139, y = row_y, name = "CH 4")

    print(SVG_TRAILER)

if __name__ == '__main__':
    main()