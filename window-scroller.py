#!/usr/bin/python3
import time
import pyautogui
import pywinctl
import argparse
import re


def screen_coordinates_type(arg_value, pat=re.compile(r"^[0-9]+,[0-9]+$")):
    if not pat.match(arg_value):
        raise argparse.ArgumentTypeError("invalid value")
    return arg_value


def numeric_string_type(arg_value, pat=re.compile(r"^[0-9]+$")):
    if not pat.match(arg_value):
        raise argparse.ArgumentTypeError("invalid value")
    return arg_value


def search_window(title):
    x = 0
    y = 0
    matched_windows = []
    while len(matched_windows) == 0:
        matched_windows = pywinctl.getWindowsWithTitle(title)
        if len(matched_windows) == 0:
            print("WARNING: No window matched the title provided. Will keep looking for it (sleeping for 30 seconds and retrying...")
            time.sleep(30)
        elif len(matched_windows) > 1:
            print("ERROR: Too many windows matched the title provided. Cannot continue.")
            exit(1)
        else:
            matched_windows[0].activate(wait=True)
            x = matched_windows[0].centerx
            y = matched_windows[0].centery
            print("DEBUG: Found window. Moving mouse to " + str(x) + "," + str(y))

    return x, y


def main():
    parser = argparse.ArgumentParser(prog="WindowsAutoScroller", description="A bot for automatically scroll down or up a window contents")
    informative_modes_group = parser.add_mutually_exclusive_group()
    get_all_window_titles_arg = informative_modes_group.add_argument('--get-all-window-titles', help='Prints the titles of all windows on the system', action='store_true')
    get_current_mouse_position_arg = informative_modes_group.add_argument('--get-current-mouse-position', help='Prints the current mouse position to use with --screen-coordinates', action='store_true')

    modes_args_group = parser.add_mutually_exclusive_group()
    screen_coordinates_arg = modes_args_group.add_argument('--screen-coordinates', type=screen_coordinates_type, help='Define the screen coordinates for the mouse in x,y format')
    window_title_arg = modes_args_group.add_argument('--window-title', help='The title of the window to scroll its contents')

    modes_and_params_args_group = modes_args_group.add_argument_group()
    scroll_interval_arg = modes_and_params_args_group.add_argument('--scroll-interval', type=numeric_string_type, help='How frequent to scroll the window contents')
    scrolls_arg = modes_and_params_args_group.add_argument('--scrolls', type=numeric_string_type, help='How frequent to scroll the window contents')

    args = parser.parse_args()
    if (args.get_all_window_titles or args.get_current_mouse_position) and (args.screen_coordinates or args.window_title or args.scroll_interval or args.scrolls):
        print("ERROR: Informative arguments cannot be used with other arguments.")
        parser.print_help()
        exit(9)

    scrolls = 100
    scroll_interval = 60
    if args.scrolls:
        scrolls = args.scrolls
    if args.scroll_interval:
        scroll_interval = args.scroll_interval

    if args.get_all_window_titles:
        print('\n'.join(pywinctl.getAllTitles()))
        exit()

    elif args.get_current_mouse_position:
        mouse_position = pyautogui.position()
        print(str(mouse_position.x) + "," + str(mouse_position.y))
        exit()

    elif args.screen_coordinates is not None:
        x = int(args.screen_coordinates.split(',')[0])
        y = int(args.screen_coordinates.split(',')[1])
        if x > pyautogui.size().width or y > pyautogui.size().height:
            raise "ERROR: Specified screen coordinates are outside the screen. (" + str(
                pyautogui.size().width) + " X " + str(pyautogui.size().height) + ")"

    elif args.window_title is not None:
        x, y = search_window(title=args.window_title)

    else:
        print("ERROR: At least one argument must be specified. See --help for details")
        exit(9)

    while True:
        for i in range(scrolls):
            if args.window_title is not None:
                x, y = search_window(title=args.window_title)
            pyautogui.moveTo(x, y)
            pyautogui.vscroll(-2)
            time.sleep(0.1)
        time.sleep(scroll_interval)


main()


