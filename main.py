import argparse
from helper import Helper
from generators.CMDAsciiGenerator import CMDAsciiGenerator
from generators.ImageAsciiGenerator import ImageAsciiGenerator
from generators.VideoAsciiGenerator import VideoAsciiGenerator
from generators.CamToAscii import CamToAscii
from enum import Enum
from Effect import Effect


class AppMode(Enum):
    CMD = 0
    IMAGE = 1
    VIDEO = 2
    CAM = 3


def run_app(mode: int):
    if mode == AppMode.CMD.value:
        filename = Helper.get_file()
        img = Helper.load_image(filename)
        terminal_width = get_argument("Terminal width (220): ", 220, int)
        ascii_gradient = get_argument("Gradient ( .-;+=xX$█): ", " .-;+=xX$█", str)
        invert_gradient = get_argument("Invert gradient (y/n)? (False): ", False, bool)

        print("-----GENERATOR INFORMATION-----")
        print(f'File: {filename}')
        print(f'Terminal width: {terminal_width}')
        print(f'Ascii gradient: "{ascii_gradient}"')
        print(f'Invert gradient: {invert_gradient}')
        print("--------------------------------")

        generator = CMDAsciiGenerator(img, terminal_width=terminal_width, ascii_gradient=ascii_gradient,
                                      invert_gradient=invert_gradient)
        generator.convert()
        generator.show_result()
    elif mode == AppMode.IMAGE.value:
        filename = Helper.get_file()
        img = Helper.load_image(filename)
        font_size = get_argument("Font size | 8: ", 8, int)
        ascii_gradient = get_argument("Gradient | ' .-;+=xX$█': ", " .-;+=xX$█", str)
        use_contrast = get_argument("Get higher contrast (y/n)? | False: ", False, bool)
        str_bg_color = get_argument("Background color | (2, 0, 23): ", None, str)
        str_fg_color = get_argument("Foreground color | (46, 126, 255): ", None, str)
        invert_gradient = get_argument("Invert gradient (y/n)? | False: ", False, bool)
        effect = get_argument("Effect (leave empty for no effect)? ", None, int)

        # some editing of values before putting it in the generator
        bg_color = extract_color(str_bg_color, (2, 0, 23))
        fg_color = extract_color(str_fg_color, (46, 126, 255))
        try:
            effect = Effect(effect)
        except ValueError:
            effect = None

        print("-----GENERATOR INFORMATION-----")
        print(f'File: {filename}')
        print(f'Font size: {font_size}')
        print(f'Ascii gradient: "{ascii_gradient}"')
        print(f'Use contrast: {use_contrast}')
        print(f'Background color: {bg_color}')
        print(f'Foreground color: {fg_color}')
        print(f'Invert gradient: {invert_gradient}')
        print(f'Effect: {effect.value if effect is not None else None}')
        print("--------------------------------")

        generator = ImageAsciiGenerator(img, font_size=font_size, foreground_color=fg_color, background_color=bg_color,
                                        ascii_gradient=ascii_gradient, invert_gradient=invert_gradient,
                                        use_contrast=use_contrast, effect=effect)
        generator.convert()
        generator.show_result()
    elif mode == AppMode.VIDEO.value:
        filename = Helper.get_file()
        font_size = get_argument("Font size | 8: ", 8, int)
        ascii_gradient = get_argument("Gradient | ' .-;+=xX$█': ", " .-;+=xX$█", str)
        use_contrast = get_argument("Get higher contrast (y/n)? | False: ", False, bool)
        str_bg_color = get_argument("Background color | (2, 0, 23): ", None, str)
        str_fg_color = get_argument("Foreground color | (46, 126, 255): ", None, str)
        invert_gradient = get_argument("Invert gradient (y/n)? | False: ", False, bool)
        vid_start = get_argument("Timestamp of video start | 0:00: ", None, float)
        vid_end = get_argument("Timestamp of video end | end of the video: ", None, float)
        effect = get_argument("Effect (leave empty for no effect)? ", None, int)

        # some editing of values before putting it in the generator
        bg_color = extract_color(str_bg_color, (2, 0, 23))
        fg_color = extract_color(str_fg_color, (46, 126, 255))
        try:
            effect = Effect(effect)
        except ValueError:
            effect = None

        print("-----GENERATOR INFORMATION-----")
        print(f'File: {filename}')
        print(f'Font size: {font_size}')
        print(f'Ascii gradient: "{ascii_gradient}"')
        print(f'Use contrast: {use_contrast}')
        print(f'Background color: {bg_color}')
        print(f'Foreground color: {fg_color}')
        print(f'Invert gradient: {invert_gradient}')
        print(f'Video start cut: {vid_start}')
        print(f'Video end cut: {vid_end}')
        print(f'Effect: {effect.value if effect is not None else None}')
        print("--------------------------------")

        print("THE VIDEO WILL NOT BE PREVIEWED AND WILL BE SAVED INSTEAD")
        generator = VideoAsciiGenerator(filename, font_size=font_size, gradient=ascii_gradient,
                                        use_contrast=use_contrast, background_color=bg_color, foreground_color=fg_color,
                                        invert_gradient=invert_gradient, video_end=vid_end, video_start=vid_start,
                                        effect=effect)
        generator.convert()

    elif mode == AppMode.CAM.value:
        font_size = get_argument("Font size | 8: ", 8, int)
        ascii_gradient = get_argument("Gradient | ' .-;+=xX$█': ", " .-;+=xX$█", str)
        str_bg_color = get_argument("Background color | (2, 0, 23): ", None, str)
        str_fg_color = get_argument("Foreground color | (46, 126, 255): ", None, str)
        invert_gradient = get_argument("Invert gradient (y/n)? | False: ", False, bool)
        show_webcam = get_argument("Show webcam (y/n)? | False ", False, bool)

        # some editing of values before putting it in the generator
        bg_color = extract_color(str_bg_color, (2, 0, 23))
        fg_color = extract_color(str_fg_color, (46, 126, 255))

        print("-----GENERATOR INFORMATION-----")
        print(f'Font size: {font_size}')
        print(f'Ascii gradient: "{ascii_gradient}"')
        print(f'Background color: {bg_color}')
        print(f'Foreground color: {fg_color}')
        print(f'Invert gradient: {invert_gradient}')
        print(f'Show webcam: {show_webcam}')
        print("--------------------------------")

        print("PRESS 'Q' TO STOP THE CAMERA")
        generator = CamToAscii(gradient=ascii_gradient, foreground_color=fg_color, background_color=bg_color,
                               font_size=font_size, show_webcam=show_webcam, invert_gradient=invert_gradient)
        generator.convert()
    else:
        raise Exception("How did we get here!?")


def extract_color(text: str, default: tuple) -> tuple:
    try:
        split = text.split(",", 2)
    except AttributeError:
        return default
    vals = []
    for num in split:
        if num.strip().isnumeric():
            val = int(num)
            if val < 0 or val > 255:
                vals.append(None)
            else:
                vals.append(val)
        else:
            vals.append(None)
    if len(vals) != 3 or None in vals:
        return default
    else:
        return tuple(vals)


def get_argument(question: str, default_val, var_type):
    answer = input(question)
    if var_type == int:
        if answer.isnumeric():
            return int(answer)
        else:
            return default_val
    if var_type == float:
        try:
            return float(answer)
        except ValueError:
            return default_val
    if var_type == str:
        if len(answer.strip()) <= 0:
            return default_val
        else:
            return answer
    if var_type == bool:
        if answer.lower() == 'y' or answer.lower() == "yes":
            return True
        elif answer.lower() == "n" or answer.lower() == "no":
            return False
        else:
            return default_val


parser = argparse.ArgumentParser()

parser.add_argument("mode",
                    help="str or int | Chooses which mode you want to use")
args = parser.parse_args()

modes = {"cmd": AppMode.CMD.value, "image": AppMode.IMAGE.value, "video": AppMode.VIDEO.value, "cam": AppMode.CAM.value}

if not args.mode.isnumeric():
    try:
        num = modes[args.mode.lower()]
        passed = True
    except KeyError:
        passed = False
else:
    num = int(args.mode)
    if num < 0 or num > 3:
        passed = False
    else:
        passed = True

if passed:
    run_app(num)
else:
    red_text = "\x1b[31m"
    reset = "\x1b[0m"
    print(f'{red_text}Warning: Incorrect argument usage{reset}')
    print("usage: main.py [-h] mode")
    print("\n-----MODES-----")
    print("CMD: 0")
    print("Image: 1")
    print("Video: 2")
    print("Cam: 3")
    print("----------------")
