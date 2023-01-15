#!/usr/bin/env python3


XML_HEADER = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>"""
SVG_HEADER = """<svg width="{width}mm" height="{height}mm"
  xmlns="http://www.w3.org/2000/svg">"""
SVG_TRAILER = """</svg>"""
LAY_TEMPL = """<?xml version="1.0"?>
<!--
license:CC0
-->
<mamelayout version="2">
    <element name="LED" defstate="0">
        <rect state="0"><color red="1.0" green="1.0" blue="1.0" alpha="0.0" /></rect>
        <rect state="1"><color red="1.0" green="0.18" blue="0.20" /></rect>
    </element>
    <element name="BUTTON">
        <rect state="0">
            <bounds x="0.0" y="0.0" width="1.0" height="1.0" />
            <color red="1.0" green="1.0" blue="1.0" alpha="0.0"/>
        </rect>
        <rect state="1">
            <bounds x="0.0" y="0.0" width="1.0" height="1.0" />
            <color red="0.5" green="0.5" blue="0.5" />
        </rect>
    </element>
    <element name="Bezel">
        <image>
            <data><![CDATA[{bezel}]]>
            </data>
        </image>
    </element>
    <view name="Front Panel">
        <element ref="Bezel">
            <bounds x="0" y="0" width="302" height="150" />
        </element>

        <screen index="0">
            <bounds x="{screen_x}" y="{screen_y}" width="{screen_width}" height="{screen_height}" />
        </screen>
{buttons}
{leds}
{up_dn_switches}
    </view>
</mamelayout>"""

BUTTON_TEMPL = """\
<element ref="BUTTON" inputtag="ROW{row}" inputmask="{mask:#02x}">
    <bounds x="{x}" y="{y}" width="{width}" height="{height}" />
</element>"""

LED_TEMPL = """\
<element ref="LED" name="FP_LED{num}">
    <bounds x="{x}" y="{y}" width="{width}" height="{height}" />
</element>"""


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

    return TEMPL.format(x = x - (width - stroke_width) / 2,
                    y = y - (height - stroke_width) / 2,
                    width = width - stroke_width,
                    height = height - stroke_width,
                    stroke_width = stroke_width)


class LayoutWriter(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.leds = []
        self.pots = []
        self.buttons = []
        self.up_dn_switches = []
        self.bezel_edge = None

    def output(self):
        side = 4.5
        stroke = 0.4
        strs = []

        for x, y, name, num in self.leds:
            strs.append(center_rect(x = x, y = y, width = 6, height = 4, stroke_width = 0.1))

        for x, y, name in self.pots:
            strs.append(circle(cx=x, cy=y, r=9.5 / 2, stroke_width=1))
            strs.append(circle(cx=x, cy=y, r=5.4 / 2, stroke_width=1))

        for x, y, name, row, mask in self.buttons:
            strs.append(center_rect(x = x, y = y, width = side, height = side, stroke_width = stroke))

        for x, y, name, row, mask in self.up_dn_switches:
            strs.append(center_rect(x, y, 6.6, 11.5, 0.5))
            strs.append(center_rect(x, y, 6.6, 3.5, 1))


        return '\n'.join(strs)


    def main_bezel(self):
        # Main bezel.
        stroke_width = 3

        strs = []
        strs.append(rr(x = 0, y = 0,
            width = self.width,
            height = self.height,
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

        self.screen_x = x
        self.screen_y = y
        self.screen_width = 105
        self.screen_height = 83.2

        self.bezel_edge = 142.25

        row_y = 78
        strs.append(self.volts_div(x = self.bezel_edge + 17, y = row_y))
        strs.append(self.volts_div(x = self.bezel_edge + 49, y = row_y))
        strs.append(self.sec_div(x = self.bezel_edge + 84, y = row_y))

        strs.append(self.bnc(x = self.bezel_edge + 16, y = 130, name = "CH 1"))
        strs.append(self.bnc(x = self.bezel_edge + 58, y = 130, name = "CH 2"))
        strs.append(self.bnc(x = self.bezel_edge + 95, y = 130, name = "CH 3"))
        strs.append(self.bnc(x = self.bezel_edge + 139, y = 130, name = "CH 4"))
        strs.append(self.pow(x = 4.41 + 6.2 + 117, y = 134, name = "POWER"))

        return '\n'.join(strs)


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


    def pot(self, x, y, name):
        self.pots.append((x, y, name))


    def but(self, x, y, name, row, mask):
        self.buttons.append((x, y, name, row, mask))


    def up_dn_switch(self, x, y, name, row, mask):
        self.up_dn_switches.append((x, y, name, row, mask))


    def bnc(self, x, y, name):
        return '\n'.join([
            circle(cx = x, cy = y, r = 14.8 / 2, stroke_width = 1),
            circle(cx = x, cy = y, r = 9.6 / 2, stroke_width = 0.5),
            circle(cx = x, cy = y, r = 4.7 / 2, stroke_width = 1)])


    def led(self, x, y, name, num):
        self.leds.append((x, y, name, num))


def main():
    l = LayoutWriter(width = 302, height = 150)

    # all dimensions in mm.
    bezel_width = l.width # 302
    bezel_height = l.height #150

    bezel_svg = [XML_HEADER,
                SVG_HEADER.format(width = bezel_width, height = bezel_height),
                l.main_bezel()]


    # Pots and buttons under the CRT.
    first_pot = 4.41 + 6.2 + 5
    pot_space = 30.3
    l.pot(x = first_pot + 0 * pot_space, y = 134, name = "INTENSITY")
    l.pot(x = first_pot + 1 * pot_space, y = 134, name = "FOCUS")
    l.pot(x = first_pot + 2 * pot_space, y = 134, name = "READOUT INTENSITY")
    l.pot(x = first_pot + 3 * pot_space, y = 134, name = "SCALE ILLUM")

    l.but(x = first_pot + 0.5 * pot_space, y = 134, name = "BEAM\nFIND", row = 0, mask = 0)

    # Pots and buttons on the main front panel.
    bezel_edge = l.bezel_edge
    first_pot = bezel_edge + 21.5
    pot_space = 25.6

    # Top row pots and buttons
    # CH1 POS
    l.pot(x = first_pot + 0 * pot_space, y = 20, name = "POSITION")
    # CH2 POS
    l.pot(x = first_pot + 1 * pot_space, y = 20, name = "POSITION")
    # VERT POS
    vert_pos_x = first_pot + 2 * pot_space
    l.pot(x = vert_pos_x, y = 20, name = "POSITION")
    l.but(x = vert_pos_x + 16, y = 20, name = "X10 MAG", row = 8, mask = 0x01)

    l.pot(x = first_pot + 88, y = 20, name = "HOLDOFF")
    l.pot(x = first_pot + 120, y = 20, name = "LEVEL")

    led_x = first_pot + (88 + 120) / 2
    led_space = 4
    l.led(x = led_x, y = 14 + 0 * led_space, name = "A SWP\nTRIGD", num = -1)
    l.led(x = led_x, y = 14 + 1 * led_space, name = "READY", num = 11)
    l.led(x = led_x, y = 14 + 2 * led_space, name = "+", num = 23)
    l.led(x = led_x, y = 14 + 3 * led_space, name = "-", num = 10)

    first_but = bezel_edge + 18.5
    but_space = 29.5 / 3
    row_y = 35.8
    # Channel selectors
    l.but(x = first_but + 0 * but_space, y = row_y, name ="CH 1", row = 6, mask = 0x01)
    l.but(x = first_but + 1 * but_space, y = row_y, name ="CH 2", row = 6, mask = 0x02)
    l.but(x = first_but + 2 * but_space, y = row_y, name ="CH 3", row = 6, mask = 0x08)
    l.but(x = first_but + 3 * but_space, y = row_y, name ="CH 4", row = 6, mask = 0x10)

    # Cursor controls.
    l.but(x = vert_pos_x + 0 * but_space, y = row_y, name = "DV", row = 8, mask = 0x08)
    l.but(x = vert_pos_x + 1 * but_space, y = row_y, name = "Dt", row = 8, mask = 0x04)
    l.but(x = vert_pos_x + 2 * but_space, y = row_y, name = "TRACKING", row = 8, mask = 0x02)

    # Trigger controls
    l.but(x = bezel_edge + 107.3 + 4.3/2, y = row_y, name = "A/B TRIG", row = 9, mask = 0x10)
    l.but(x = bezel_edge + 107.3 + 4.3/2 + 15.3, y = row_y, name = "SLOPE", row = 8, mask = 0x10)

    row_y += 15.4
    l.but(x = first_but + 0 * but_space, y = row_y, name ="ADD", row = 6, mask = 0x04)
    l.but(x = first_but + 1 * but_space, y = row_y, name ="INVERT", row = 2, mask = 0x10)
    l.but(x = first_but + 2 * but_space, y = row_y, name ="CHOP", row = 7, mask = 0x08)
    l.but(x = first_but + 3 * but_space, y = row_y, name ="20 MHZ\nBW LIMIT", row = 7, mask = 0x10)

    row_y = 52
    l.pot(x = bezel_edge + 72, y = row_y, name = "D REF or DLY POS")
    l.pot(x = bezel_edge + 72 + 22.3, y = row_y, name = "D")

    first_switch = bezel_edge + 110
    row_y = 83.5
    switch_space = 11.6

    led_x = first_switch + 0 * switch_space
    l.led(x = led_x, y = 46 + 0 * led_space, name = "AUTO LVL", num = 15)
    l.led(x = led_x, y = 46 + 1 * led_space, name = "AUTO", num = 14)
    l.led(x = led_x, y = 46 + 2 * led_space, name = "NORM", num = 13)
    l.led(x = led_x, y = 46 + 3 * led_space, name = "SGL SEQ", num = 12)
    l.led(x = led_x, y = 46 + 5 * led_space, name = "RUN", num = 16)
    l.led(x = led_x, y = 46 + 6 * led_space, name = "TRIG", num = 17)

    led_x = first_switch + 1 * switch_space
    l.led(x = led_x, y = 46 + 0 * led_space, name = "VERT", num = 24)
    l.led(x = led_x, y = 46 + 1 * led_space, name = "CH 1", num = 25)
    l.led(x = led_x, y = 46 + 2 * led_space, name = "CH 2", num = 26)
    l.led(x = led_x, y = 46 + 3 * led_space, name = "CH 3", num = 27)
    l.led(x = led_x, y = 46 + 4 * led_space, name = "CH 4", num = 28)
    l.led(x = led_x, y = 46 + 5 * led_space, name = "LINE", num = 29)

    led_x = first_switch + 2 * switch_space
    l.led(x = led_x, y = 46 + 0 * led_space, name = "DC", num = 18)
    l.led(x = led_x, y = 46 + 1 * led_space, name = "NOISE", num = 19)
    l.led(x = led_x, y = 46 + 2 * led_space, name = "HF", num = 20)
    l.led(x = led_x, y = 46 + 3 * led_space, name = "LF", num = 21)
    l.led(x = led_x, y = 46 + 4 * led_space, name = "AC", num = 22)

    l.up_dn_switch(x = first_switch + 0 * switch_space, y = row_y, name = "MODE", row = 9, mask = 0x04)
    l.up_dn_switch(x = first_switch + 1 * switch_space, y = row_y, name = "SOURCE", row = 9, mask = 0x01)
    l.up_dn_switch(x = first_switch + 2 * switch_space, y = row_y, name = "COUPLING", row = 0, mask = 0x01)

    row_y = 104
    l.up_dn_switch(x = bezel_edge + 23, y = row_y, name = "CH1 CPL", row = 0, mask = 0x08)
    l.up_dn_switch(x = bezel_edge + 55, y = row_y, name = "CH2_CPL", row = 1, mask = 0x08)

    led_x = bezel_edge + 12
    l.led(x = led_x, y = 94 + 0 * led_space, name = "AC", num = 0)
    l.led(x = led_x, y = 94 + 1 * led_space, name = "GND", num = 1)
    l.led(x = led_x, y = 94 + 2 * led_space, name = "DC", num = 2)
    l.led(x = led_x, y = 94 + 3 * led_space, name = "GND", num = 3)
    l.led(x = led_x, y = 94 + 4 * led_space, name = "50Ohm DC", num = 4)

    led_x = bezel_edge + 44
    l.led(x = led_x, y = 94 + 0 * led_space, name = "AC", num = 5)
    l.led(x = led_x, y = 94 + 1 * led_space, name = "GND", num = 6)
    l.led(x = led_x, y = 94 + 2 * led_space, name = "DC", num = 7)
    l.led(x = led_x, y = 94 + 3 * led_space, name = "GND", num = 8)
    l.led(x = led_x, y = 94 + 4 * led_space, name = "50Ohm DC", num = 9)

    l.pot(x = bezel_edge + 72, y = row_y, name = "TRACE\nSEP")
    # CH3 POS
    l.pot(x = bezel_edge + 96, y = row_y, name = "POSITION")

    l.but(x = bezel_edge + 111, y = row_y, name = "VOLTS/DIV", row = 1, mask = 0x2)
    l.but(x = bezel_edge + 121, y = row_y, name = "VOLTS/DIV", row = 1, mask = 0x1)

    # CH4 POS
    l.pot(x = bezel_edge + 139, y = row_y, name = "POSITION")

    bezel_svg.append(l.output())
    bezel_svg.append(SVG_TRAILER)

    buttons = []
    for x, y, name, row, mask in l.buttons:
        side = 4.5
        if row and mask:
            buttons.append(BUTTON_TEMPL.format(x = x - side / 2, y = y - side / 2, 
                            row = row, mask = mask, width = side, height = side))

    for x, y, name, row, mask in l.up_dn_switches:
        width = 6.6
        height = 11.5
        # Start with the down button.
        buttons.append(BUTTON_TEMPL.format(x = x - width / 2, y = y,
                        row = row, mask = mask, width = width, height = height / 2))
        buttons.append(BUTTON_TEMPL.format(x = x - width / 2, y = y - height / 2,
                        row = row, mask = mask << 1, width = width, height = height / 2))


    leds = []
    for x, y, name, num in l.leds:
        height = 4
        width = 6
        leds.append(LED_TEMPL.format(x = x - width / 2, y = y - height / 2, 
                        num = num, width = width, height = height))

    print(LAY_TEMPL.format(bezel = '\n'.join(bezel_svg),
                           screen_x = l.screen_x, 
                           screen_y = l.screen_y,
                           screen_width = l.screen_width,
                           screen_height = l.screen_height,
                           buttons = '\n'.join(buttons),
                           leds = '\n'.join(leds),
                           up_dn_switches = ""))
#    print('\n'.join(bezel_svg))


if __name__ == '__main__':
    main()