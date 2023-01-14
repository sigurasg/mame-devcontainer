#!/usr/bin/env python3


XML_HEADER = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>"""
SVG_HEADER = """<svg width="{width}mm" height="{height}mm"
  xmlns="http://www.w3.org/2000/svg">"""
SVG_TRAILER = """</svg>"""
LAY_HEADER = """<?xml version="1.0"?>
<!--
license:CC0
-->
<mamelayout version="2">
"""
LAY_TRAILER = "</mamelayout>"


def rr(x, y, width, height, r, stroke_width):
    TEMPL = """<rect x="{x}mm" y="{y}mm" width="{width}mm" height="{height}mm" rx="{r}mm" ry="{r}mm"
        style="fill:rgb(255,255,255);stroke-width:{stroke_width}mm;stroke:rgb(0,0,0)"/>"""

    return TEMPL.format(
                    x = x + stroke_width / 2,
                    y = y + stroke_width / 2,
                    width = width - stroke_width,
                    height = height - stroke_width,
                    r = r,
                    stroke_width=stroke_width)


def circle(cx, cy, r, stroke_width):
    CIRCLE_TEMPL = """<circle cx="{cx}mm" cy="{cy}mm" r="{r}mm"
        style="fill:rgb(255,255,255);stroke-width:{stroke_width}mm;stroke:rgb(0,0,0)"/>"""

    return CIRCLE_TEMPL.format(cx = cx, cy = cy, r = r - stroke_width / 2, stroke_width = stroke_width)


def center_rect(x, y, width, height, stroke_width):
    TEMPL = """<rect x="{x}mm" y="{y}mm" width="{width}mm" height="{height}mm"
        style="fill:rgb(255,255,255);stroke-width:{stroke_width}mm;stroke:rgb(0,0,0)"/>"""

    print(TEMPL.format(x = x - (width - stroke_width) / 2,
                    y = y - (height - stroke_width) / 2,
                    width = width - stroke_width,
                    height = height - stroke_width,
                    stroke_width = stroke_width))

class LayoutWriter(object):
    def __init__(self):
        self.leds = []
        self.pots = []
        self.buttons = []
        self.up_dn_switches = []
        self.bezel_edge = None


    def main_bezel(self, width, height, stroke_width):
        # Main bezel.
        strs = []
        strs.append(rr(x = 0, y = 0,
            width = width,
            height = height,
            r = 10,
            stroke_width = stroke_width))

        x = 6.25
        y = 0
        strs.append(rr(x = x, y = y,
            width = 135.6,
            height = 145,
            r = 5,
            stroke_width = stroke_width))
        x += 7.5
        y += 12.3
        strs.append(rr(x = x, y = y,
            width = 120,
            height = 105.6,
            r = 5,
            stroke_width = stroke_width))
        x += (120 - 105) / 2
        y += 10
        strs.append(rr(x = x,
            y = y,
            width = 105,
            height = 83.2,
            r = 0.1,
            stroke_width = 1))

        self.bezel_edge = 142.25

        strs.append(self.bnc(x = self.bezel_edge + 16, y = 130, name = "CH 1"))
        strs.append(self.bnc(x = self.bezel_edge + 58, y = 130, name = "CH 2"))
        strs.append(self.bnc(x = self.bezel_edge + 95, y = 130, name = "CH 3"))
        strs.append(self.bnc(x = self.bezel_edge + 139, y = 130, name = "CH 4"))
        strs.append(self.pow(x = 4.41 + 6.2 + 117, y = 134, name = "POWER"))

        return '\n'.join(strs)


    def pot(self, x, y, name):
        self.pots.append((x, y, name))
        return '\n'.join([
            circle(cx=x, cy=y, r=9.5 / 2, stroke_width=1),
            circle(cx=x, cy=y, r=5.4 / 2, stroke_width=1)])


    def but(self, x, y, name):
        self.buttons.append((x, y, name))
        side = 4.5
        stroke = 0.4
        center_rect(x = x, y = y, width = side, height = side, stroke_width = stroke)


    def pow(self, x, y, name):
        # TODO(siggi): Render the power button properly
        return circle(cx = x, cy = y, r = 10 / 2, stroke_width = 0.5)


    def volts_div(self, x, y):
        # TODO(siggi): Render the volts/div dials properly
        return '\n'.join([
            circle(cx = x, cy = y, r = 17.6 / 2, stroke_width = 0.5),
            circle(cx = x, cy = y, r = 10 / 2, stroke_width = 0.5)])


    def sec_div(self, x, y):
        # TODO(siggi): Render the sec/div dial properly
        return '\n'.join([
            circle(cx = x, cy = y, r = 28.3 / 2, stroke_width = 0.1),
            circle(cx = x, cy = y, r = 21.3 / 2, stroke_width = 0.5),
            circle(cx = x, cy = y, r = 10 / 2, stroke_width = 0.5)])


    def up_dn_switch(self, x, y, name):
        # TODO(siggi): Render the up_dn switches properly
        self.up_dn_switches.append((x, y, name))
        center_rect(x, y, 6.6, 11.5, 0.5)
        center_rect(x, y, 6.6, 3.5, 1)


    def bnc(self, x, y, name):
        return '\n'.join([
            circle(cx = x, cy = y, r = 14.8 / 2, stroke_width = 1),
            circle(cx = x, cy = y, r = 9.6 / 2, stroke_width = 0.5),
            circle(cx = x, cy = y, r = 4.7 / 2, stroke_width = 1)])


    def led(self, x, y, name):
        self.leds.append((x, y, name))
        center_rect(x = x, y = y, width = 6, height = 4, stroke_width = 0.1)


def main():
    l = LayoutWriter()

    # all dimensions in mm.
    bezel_width = 302
    bezel_height = 150

    print(XML_HEADER)
    print(SVG_HEADER.format(width = bezel_width, height = bezel_height))

    print(l.main_bezel(width = bezel_width, height = bezel_height, stroke_width = 3))

    # Pots and buttons under the CRT.
    first_pot = 4.41 + 6.2 + 5
    pot_space = 30.3
    print(l.pot(x = first_pot + 0 * pot_space, y = 134, name = "INTENSITY"))
    print(l.pot(x = first_pot + 1 * pot_space, y = 134, name = "FOCUS"))
    print(l.pot(x = first_pot + 2 * pot_space, y = 134, name = "READOUT INTENSITY"))
    print(l.pot(x = first_pot + 3 * pot_space, y = 134, name = "SCALE ILLUM"))

    l.but(x = first_pot + 0.5 * pot_space, y = 134, name = "BEAM\nFIND")

    # Pots and buttons on the main front panel.
    bezel_edge = l.bezel_edge
    first_pot = bezel_edge + 21.5
    pot_space = 25.6

    # Top row pots and buttons
    # CH1 POS
    print(l.pot(x = first_pot + 0 * pot_space, y = 20, name = "POSITION"))
    # CH2 POS
    print(l.pot(x = first_pot + 1 * pot_space, y = 20, name = "POSITION"))
    # VERT POS
    vert_pos_x = first_pot + 2 * pot_space
    print(l.pot(x = vert_pos_x, y = 20, name = "POSITION"))
    l.but(x = vert_pos_x + 16, y = 20, name = "X10 MAG")

    print(l.pot(x = first_pot + 88, y = 20, name = "HOLDOFF"))
    print(l.pot(x = first_pot + 120, y = 20, name = "LEVEL"))

    led_x = first_pot + (88 + 120) / 2
    led_space = 4
    l.led(x = led_x, y = 14 + 0 * led_space, name = "A SWP\nTRIGD")
    l.led(x = led_x, y = 14 + 1 * led_space, name = "READY")
    l.led(x = led_x, y = 14 + 2 * led_space, name = "+")
    l.led(x = led_x, y = 14 + 3 * led_space, name = "-")

    first_but = bezel_edge + 18.5
    but_space = 29.5 / 3
    row_y = 35.8
    # Channel selectors
    l.but(x = first_but + 0 * but_space, y = row_y, name ="CH 1")
    l.but(x = first_but + 1 * but_space, y = row_y, name ="CH 2")
    l.but(x = first_but + 2 * but_space, y = row_y, name ="CH 3")
    l.but(x = first_but + 3 * but_space, y = row_y, name ="CH 4")

    # Cursor controls.
    l.but(x = vert_pos_x + 0 * but_space, y = row_y, name = "DV")
    l.but(x = vert_pos_x + 1 * but_space, y = row_y, name = "Dt")
    l.but(x = vert_pos_x + 2 * but_space, y = row_y, name = "TRACKING")

    # Trigger controls
    l.but(x = bezel_edge + 107.3 + 4.3/2, y = row_y, name = "A/B TRIG")
    l.but(x = bezel_edge + 107.3 + 4.3/2 + 15.3, y = row_y, name = "SLOPE")

    row_y += 15.4
    l.but(x = first_but + 0 * but_space, y = row_y, name ="ADD")
    l.but(x = first_but + 1 * but_space, y = row_y, name ="INVERT")
    l.but(x = first_but + 2 * but_space, y = row_y, name ="CHOP")
    l.but(x = first_but + 3 * but_space, y = row_y, name ="20 MHZ\nBW LIMIT")

    row_y = 52
    print(l.pot(x = bezel_edge + 72, y = row_y, name = "D REF or DLY POS"))
    print(l.pot(x = bezel_edge + 72 + 22.3, y = row_y, name = "D"))

    btn_width = 18.1
    first_but = bezel_edge + 17
    row_y = 78
    print(l.volts_div(x = first_but, y = row_y))
    print(l.volts_div(x = first_but + 32, y = row_y))

#    print("***", first_but + 86.5 - btn_width / 2 - 21.5 / 2 - bezel_edge)

    print(l.sec_div(x = bezel_edge + 84, y = row_y))

    first_switch = bezel_edge + 110
    row_y = 83.5
    switch_space = 11.6

    led_x = x = first_switch + 0 * switch_space
    l.led(x = led_x, y = 46 + 0 * led_space, name = "AUTO LVL")
    l.led(x = led_x, y = 46 + 1 * led_space, name = "AUTO")
    l.led(x = led_x, y = 46 + 2 * led_space, name = "NORM")
    l.led(x = led_x, y = 46 + 3 * led_space, name = "SGL SEQ")
    l.led(x = led_x, y = 46 + 5 * led_space, name = "RUN")
    l.led(x = led_x, y = 46 + 6 * led_space, name = "TRIG")

    led_x = x = first_switch + 1 * switch_space
    l.led(x = led_x, y = 46 + 0 * led_space, name = "VERT")
    l.led(x = led_x, y = 46 + 1 * led_space, name = "CH 1")
    l.led(x = led_x, y = 46 + 2 * led_space, name = "CH 2")
    l.led(x = led_x, y = 46 + 3 * led_space, name = "CH 3")
    l.led(x = led_x, y = 46 + 4 * led_space, name = "CH 4")
    l.led(x = led_x, y = 46 + 5 * led_space, name = "LINE")

    led_x = x = first_switch + 2 * switch_space
    l.led(x = led_x, y = 46 + 0 * led_space, name = "DC")
    l.led(x = led_x, y = 46 + 1 * led_space, name = "NOISE")
    l.led(x = led_x, y = 46 + 2 * led_space, name = "HF")
    l.led(x = led_x, y = 46 + 3 * led_space, name = "LF")
    l.led(x = led_x, y = 46 + 4 * led_space, name = "AC")

    l.up_dn_switch(x = first_switch + 0 * switch_space, y = row_y, name = "MODE")
    l.up_dn_switch(x = first_switch + 1 * switch_space, y = row_y, name = "SOURCE")
    l.up_dn_switch(x = first_switch + 2 * switch_space, y = row_y, name = "COUPLING")

    row_y = 104
    l.up_dn_switch(x = bezel_edge + 23, y = row_y, name = "CH1 CPL")
    l.up_dn_switch(x = bezel_edge + 55, y = row_y, name = "CH2_CPL")

    led_x = bezel_edge + 12
    l.led(x = led_x, y = 94 + 0 * led_space, name = "AC")
    l.led(x = led_x, y = 94 + 1 * led_space, name = "GND")
    l.led(x = led_x, y = 94 + 2 * led_space, name = "DC")
    l.led(x = led_x, y = 94 + 3 * led_space, name = "GND")
    l.led(x = led_x, y = 94 + 4 * led_space, name = "50Ohm DC")

    led_x = bezel_edge + 44
    l.led(x = led_x, y = 94 + 0 * led_space, name = "AC")
    l.led(x = led_x, y = 94 + 1 * led_space, name = "GND")
    l.led(x = led_x, y = 94 + 2 * led_space, name = "DC")
    l.led(x = led_x, y = 94 + 3 * led_space, name = "GND")
    l.led(x = led_x, y = 94 + 4 * led_space, name = "50Ohm DC")

    print(l.pot(x = bezel_edge + 72, y = row_y, name = "TRACE\nSEP"))
    # CH3 POS
    print(l.pot(x = bezel_edge + 96, y = row_y, name = "POSITION"))

    l.but(x = bezel_edge + 111, y = row_y, name = "VOLTS/DIV")
    l.but(x = bezel_edge + 121, y = row_y, name = "VOLTS/DIV")

    # CH4 POS
    print(l.pot(x = bezel_edge + 139, y = row_y, name = "POSITION"))


    print(SVG_TRAILER)

if __name__ == '__main__':
    main()