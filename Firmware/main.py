from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.extensions.display import Display, Text
import board
import busio

keyboard = KMKKeyboard()

keyboard.row_pins = [
    board.GP26,   # sw1 shift
    board.GP27,   # sw2 esc
    board.GP28,   # sw3 d
    board.GP2,    # sw5 s
    board.GP1,    # sw6 w
    board.GP3,    # sw7 enter
    board.GP4,    # sw8 a
]

keyboard.diode_orientation = DiodeOrientation.COL2ROW

i2c = busio.I2C(scl=board.GP7, sda=board.GP6)
display = Display(i2c=i2c, width=128, height=32)

def center_text(t):
    l = len(t) * 6
    x = int((128 - l) / 2)
    if x < 0:
        x = 0
    return x

oled_text = Text(display, x=center_text("GoatTech"), y=10, text="GoatTech")
display.add_element(oled_text)

keyboard.extensions.append(display)

keyboard.keymap = [
    [
        KC.LSHIFT,   # sw1
        KC.ESC,      # sw2
        KC.D,        # sw3
        KC.S,        # sw5
        KC.W,        # sw6
        KC.ENTER,    # sw7
        KC.A,        # sw8
    ]
]

@keyboard.hooks.pressed
def pressed(key, kb):
    try:
        name = key.name
    except:
        name = "??"
    msg = "Pressed: " + name
    oled_text.x = center_text(msg)
    oled_text.text = msg

@keyboard.hooks.released
def released(key, kb):
    oled_text.x = center_text("GoatTech")
    oled_text.text = "GoatTech"

keyboard.go()
