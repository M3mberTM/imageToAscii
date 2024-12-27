import argparse
from typing import Optional
import re

"""
ARGUMENTS
type - which ascii generator to run (Cmd, Image, video)
gradient - optional (text gradient to use for the image)

additional arguments:
    if the type is not cmd line (ignore if command line is set):
        size - character size to use
        f_color - text color
        b_color - background color
        advanced_mode - boolean, increases contrast of the whole image (takes slightly longer)
    if command line:
    terminal width - the amount of characters in terminal line on a given computer
    -- defines optional arguments
"""


def string_to_rgb(text: str) -> tuple:
    rgb = text.split(",")
    if len(rgb) < 3 or len(rgb) > 3:
        raise Exception(f'Not enough numbers given to form a full RGB color')

    fg = []
    for i in rgb:
        temp = i.strip()
        if not re.search("^((1?[0-9]?[0-9])|2[0-4][0-9]|25[0-5])$", temp):
            raise Exception(f'{i} -> Number is outside the allowed range')
        fg.append(int(temp))
    return tuple(fg)


parser = argparse.ArgumentParser()

# main arguments
parser.add_argument("type",
                    help="Decides which generator to use (0 - in command line, 1 - creates an image, 2 - converts videos)",
                    type=int)
parser.add_argument("-g", "--gradient",
                    help="String | specifies text which to use to convert the image | Format: ' .-;+=xX$█'")

# side arguments
parser.add_argument("-w", "--width", help="Int | Amount of characters that fit into single line of terminal", type=int)
parser.add_argument("-s", "--size", help="Int | Size of text to use in the conversion", type=int)
parser.add_argument("-f", "--fgcolor", help="RGB Color of the text | Format: '124, 24, 38'")
parser.add_argument("-b", "--bgcolor", help="RGB Color of the background | Format: '124, 24, 38'")
parser.add_argument("-a", "--advanced",
                    help="Boolean | Uses a different algorithm to increase the contrast and color in the image (takes slightly longer to run)",
                    action="store_true")
args = parser.parse_args()

print(args)

gradient = " .-;+=xX$█"

terminal_width = 210

text_size = 8
bg_color = (33, 21, 8)
fg_color = (77, 255, 0)
advanced = False

if args.gradient:
    gradient = args.gradient

if not args.type:
    if args.width:
        terminal_width = args.width
    print("Command line")
else:
    if args.size:
        text_size = args.size
    if args.advanced:
        advanced = args.advanced
    if args.fgcolor:
        fg_color = string_to_rgb(args.fgcolor)
    if args.bgcolor:
        bg_color = string_to_rgb(args.bgcolor)

    if args.type == 1:
        print("Image conversion")
    elif args.type == 2:
        print("Video conversion")
    else:
        print("Incorrect")
